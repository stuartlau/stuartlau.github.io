---
layout:     post
title:      "HBase的HFile合并过程解析"
subtitle:   "HFile Compaction in HBase"
date:       2020-05-29
author:     S.L
header-img: img/home-bg-o.jpg
catalog: true
tags:
    - HBase
---

> Compaction是指一个region 的一个 store 中的多个 HFile 合为一个 HFile 的操作，HBase在执行合并时会对上层业务产生比较大的影响。
本文对其中的执行原理和过程进行一定的研究。
  
![](https://mapr.com/blog/in-depth-look-hbase-architecture/assets/blogimages/HBaseArchitecture-Blog-Fig19.png)
### 合并storefile的原因
我们知道HBase的数据默认会先写到HLog中，然后写到memstore中，当memstore写成功后就立刻返回给客户端写回成功。

当数据越来越多直到memstore占满，会将其刷新到硬盘的storefile中，
并且每次写入形成一个单独storefile，当storefile达到一定的数量后，如果不进行合并处理，会降低查询的效率，因为Hadoop
不擅长处理小文件，文件越大性能越好。

### 合并分类
HBase 根据合并规模将 Compaction 分为了两类：
- Minor Compaction是指选取一些`小的、相邻的`StoreFile将他们合并成一个更大的StoreFile，在这个过程中不会处理已经Deleted
或Expired的Cell。一次Minor Compaction的结果是更少并且更大的StoreFile。

- Major Compaction是指将`所有的`StoreFile合并成一个StoreFile，这个过程还会清理三类无意义数据：被删除的数据、TTL
过期数据、版本号超过设定版本号的数据。另外，一般情况下，Major Compaction时间会持续比较长，整个过程会消耗大量系统资源，
对上层业务有比较大的影响，比如PUT操作耗时会增加。因此线上业务都会将关闭自动触发Major Compaction功能，改为手动在业务低峰期触发。

### 合并时机
触发compaction的方式有三种：Memstore刷盘、后台线程周期性检查、手动触发。
1.Memstore Flush:

应该说compaction操作的源头就来自flush操作，Memstore Flush会产生HFile文件，文件越来越多就需要compact。
因此在每次执行完Flush操作之后，都会对当前Store中的文件数进行判断，一旦文件数大于配置，就会触发compaction。
需要说明的是，compaction都是以Store为单位进行的，而在Flush触发条件下，整个Region的所有Store都会执行compact，
所以会在短时间内执行多次compaction。

2.后台线程周期性检查：

后台线程定期触发检查是否需要执行compaction，检查周期可配置。线程先检查文件数是否大于配置，一旦大于就会触发compaction。
如果不满足，它会接着检查是否满足major compaction条件，简单来说，如果当前Store中HFile的*最早更新时间*早于某个值mcTime，
就会触发major compaction（默认7天触发一次，可配置手动触发），HBase预想通过这种机制定期删除过期数据。

3.手动触发：

一般来讲，手动触发compaction通常是为了执行Major Compaction，一般有这些情况需要手动触发合并是因为很多业务担心
自动Major Compaction影响读写性能，因此会选择低峰期手动触发；

也有可能是用户在执行完alter操作之后希望立刻生效，执行手动触发Major Compaction；或HBase管理员发现硬盘容量不够的情况
下手动触发Major Compaction删除大量过期数据；

### 如何实现合并后的排序
由于内存里memstore是在数据插入的过程中就排序的，就是数据插入的时候按照顺序插入，所以memstore里的数据是有序的。
当memstore的数据刷写到磁盘时，生成的storefile里的数据也是有序的，这样的话各个storefile里的数据就分别有序了。
合并的时候需要将各个有序的storefile合并成一个大的有序的storefile。

首先将各个需要合并的storefile封装成`StoreFileScanner`，最后形成一个List加载到内存，然后再封装成`StoreScanner`
对象，这个对象初始化的时候会对各个`StoreFileScanner`进行排序放到内部的队列里，排序是按照各个`StoreFileScanner`最小
的rowkey进行排序的。然后通过StoreScanner的next()方法可以拿到各个`StoreFileScanner`最小rowkey中的最小rowkey对应的KV对。
然后就把取出的KV对追加写入合并后的storefile。因为每次取出的都是各个storefile里最小的数据，所以追加写入合并后的storefile里的数据就是按从小到大排序的有序数据。

### 合并时的操作
在合并的过程中会抛弃删除标识的行和版本过旧的行

-（1）可以预先定义版本的个数，超过这个值就抛弃

-（2）还可以预先定义版本的时间长短，超过这个时间就抛弃，合并完后形成更大的storefile，当达到数量再次合并，
直到storefile容量超过一定阀值后会把当前的Region进行分裂为2个并由HMaster（Hbase数据库主控节点）
分配到不同的HRegionServer服务器处理实现负载均衡。

### 合并时如何处理查询请求
如果在合并过程中恰好有涉及到有关storefile的查询发生的话，先是把小storefile加载到内存中进行合并此时如有用户访问可以在
内存中检索相关数据返回给用户，我们可以想象在内存中做一个独立镜像备份专门提供被查询需求，另一个主体在另一块内存空间里进行合并，
当合并完成后释放备份的内存空间，返回到原来的状态。

### Reference
- [如何跳过es分页这个坑？](https://my.oschina.net/u/1787735/blog/3024051)
- [search-request-scroll.](https://www.elastic.co/guide/en/elasticsearch/reference/2.0/search-request-scroll.html)

> 本文首次发布于 [S.L's Blog](http://elsef.com), 作者 [@stuartlau](http://github.com/stuartlau) ,
转载请保留原文链接.
