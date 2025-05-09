---
layout:     post
permalink:  /blogs/2019-04-26-B+Tree-and-BTree/index.html
title:      "B+Tree和B-Tree"
subtitle:   "B+Tree/B-Tree"
date:       2019-04-26
author:     StuartLau
header-img: img/home-bg-o.jpg
catalog: true
tags:
    - MySQL
---
> 本文主要讨论和MySQL存储引擎相关的数据结构，如B+Tree和一些FAQ

开篇先介绍一个usfca提供的虚拟化可视数据结构的交互页面，可以模拟各种数据结构的各种操作的过程，效果很赞，本文讲述的两种数据结构也包含在其中，
[B-Tree](https://www.cs.usfca.edu/~galles/visualization/BTree.html)、
[B+Tree](https://www.cs.usfca.edu/~galles/visualization/BPlusTree.html)，可以边操作便理解，效果更佳。

#### 为什么数据存储要用B树？
磁盘中有两个机械运动的部分，分别是盘片旋转和磁臂移动。盘片旋转就是我们市面上所提到的多少转每分钟，而磁盘移动则是在盘片旋转到指定位置以后，移动磁臂后开始进行数据的读写。那么这就存在一个定位到磁盘中的块的过程，而定位是磁盘的存取中花费时间比较大的一块，毕竟机械运动花费的时候要远远大于电子运动的时间。当大规模数据存储到磁盘中的时候，显然定位是一个非常花费时间的过程，但是我们可以通过B树进行优化，提高磁盘读取时定位的效率。

为什么B类树可以进行优化呢？我们可以根据B类树的特点，构造一个多阶的B类树，然后在尽量多的在结点上存储相关的信息，保证层数尽量的少，在B
树中可以检查多个子结点，由于在一棵树中检查任意一个结点都需要一次磁盘访问，所以B树避免了大量的磁盘访问；而且B
类树是平衡树，每个结点到叶子结点的高度都是相同，这也保证了每个查询是稳定的，查询的时间复杂度是 `O(log2N) ` 。

总的来说就是利用平衡树的优势，保证了查询的稳定性和加快了查询的速度。如果用哈希存储，可能链表中的数据不一定存储在相同的节点里了，因为单链表不必须是连续的地址空间，这给加载数据造成一定的内存压力。

#### B+数查找到叶子节点如何取出行数据？
B+树索引并不能根据键值找到具体的行数据，B+树索引只能找到行数据锁在的页，然后通过把页读到内存，再在内存中查找到行数据。

#### 为什么不建议用UUID做主键？
和InnoDB的索引实现有关，底层使用B+Tree
，该结构最大的消耗在于频繁的改变树的节点（拆分、合并、转移位置），为了避免这种消耗较大的动作，尽可能的在插入新数据时不要对原有结构产生较大影响，如只是简单的append
到节点的数据集后面一般不会影响其他节点，或者至多产生一次分裂（大部分时候不会发生）。
所以建议使用 `单调递增 `的数据作为主键，它很好的规避了对B+Tree存储主键索引存储结构的变更操作。
#### 为什么不建议用较长的字段做主键？
因为B+Tree的Secondary Index的叶子节点保存的是主键的内容，内容过大会影响存储空间，导致辅助索引过大，进而影响对辅助索引的使用效率，如节点分配过多，范围查询检索性能降低等。
注意InnoDB不会压缩索引。

#### 聚集索引怎么理解？
Clustered Index是InnoDB存储引擎中的索引，由于该引擎的存储使用B+Tree存储主键索引，且叶子节点中包括索引和数据两部分，就像数据「聚集」在索引上一样。也就是说InnoDB
的数据文件其实就是主键的索引文件，并且InnoDB中必须要有主键（否则就没有聚集索引一说了），如果用户不设置，则系统会自动设置隐形的6字节自增主键。

而非聚集索引则对应MyISAM中对主键索引的存储形式：叶子节点只存储主键的值和数据地址，需要二次查询才可以获取数据信息。

#### 什么时候非聚集索引不需要回表查询多次？
当查询条件和查询结果都数据一个联合索引时，即「覆盖索引」，此时只需执行对索引的查询就可以获得想要的数据，无需从数据表中读取，减少I/O提高效率。

#### 同样都是使用B+Tree，InnoDB和MyISAM的实现细节有什么区别？
- 主键索引：主要区别是聚集索引和非聚集索引上，前者除了保存主键外还有数据，后者除了主索引key外只保存记录的地址address（可以理解为行号）。
- 辅助索引：前者叶节点中保存的是辅助索引key和主键索引的值PK，后者保存的是辅助索引key和对应的主键索引的地址address（可以理解为行号）。
所以MyISAM的索引文件和数据文件是彼此独立存在的，并且MyISAM的主键索引和辅助索引在存储结构上是一样的，都是在叶子节点上保存了数据的地址，唯一不同的是辅助索引的关键字是允许重复的。
对于通过辅助索引来检索记录的操作来说，由于InnoDB存储的是主键的值，还需要再次查询主键索引才可以获得记录的内容，而MyISAM
存储的也是主键行号，可以直接读取行号对应的记录内容。

#### InnoDB的辅助索引的叶子节点存储主键的值而不是地址，好处是什么？
减少了当出现行记录移动或者数据页分裂时辅助索引的维护工作，虽然使用主键值当作指针会让辅助索引占用更多空间，但好处是，Innodb在移动行时无需更新辅助索引中的主键值，而MyISAM
需要调整其辅助索引的叶子节点中保存的主键的地址。


#### B+Tree查找到非叶子节点时是否终止，B-Tree呢？
由于B-Tree的非叶子节点也存储数据，导致其左右子节点无需包含该父节点中的key数据，所以B-Tree在检索到非叶子节点时如果命中条件则不会继续查找，直接返回命中的数据。
而B+Tree由于非叶子节点不再存储数据，导致其即使是非叶子节点，最终也会在叶子节点中有一个完整（key和data）的信息，所以B+Tree
查找到非叶子节点即使命中条件，也需要继续向叶子节点处查找，一直遍历节点中的key与查询的key相同后再返回具体的数据。

#### 为什么说MyISAM的插入性能要好于InnoDB？
从底层对主键的维护角度来说，InnoDB需要为新插入的数据的主键在B+Tree中寻找合适的存放位置，该插入操作可能会造成对现有B+Tree
数据结构的变动（节点拆分、转移、合并等），产生额外的消耗，进而影响性能。
而MyISAM由于可以没有主键，所以在相同表结构前提下，一个没有主键不需要操心树结构的分裂重建问题，一个有主键需要考虑节点的分裂和重建等工作，前者性能高一些是合理的。

#### 如何加快检索磁盘？
将每一个节点的大小和磁盘页的大小`PageSize`设置相同，保证每一次I/O操作都可以加载完整的节点。
每次新建节点时，直接申请一个页的空间，这样就保证一个节点物理上也存储在一个页里，加之计算机存储分配都是按页对齐的，就实现了加载一个node只需一次I/O。

#### 为什么使用B-Tree(B+Tree)来存储索引而不用红黑树之类的?
一般来说，索引本身也很大，不可能全部存储在内存中，因此索引往往以索引文件的形式存储的磁盘上。
这样的话，索引查找过程中就要产生磁盘I/O消耗，相对于内存存取，I/O存取的消耗要高几个数量级，所以评价一个数据结构作为索引的优劣最重要的指标就是在查找过程中磁盘I/O操作次数的渐进复杂度。
换句话说，索引的结构组织要尽量减少查找过程中磁盘I/O的存取次数。

首先说明一下B-Tree的渐进度的概念：
> 例如一个度为d的B-Tree，设其索引N个key，则其树高h的上限为logd((N+1)/2)，检索一个key，其查找节点个数的渐进复杂度为O(logdN)
。从这点可以看出，B-Tree是一个非常有效率的索引数据结构。

一般实际应用中，出度d是非常大的数字，通常超过100，因此h非常小（通常不超过3）。综上所述，用B-Tree作为索引结构效率是非常高的。

而红黑树这种结构，h明显要深的多。由于逻辑上很近的节点（父子）物理上可能很远，无法利用局部性，所以红黑树的I/O渐进复杂度也为O(h)，效率明显比B-Tree差很多。

#### 为什么说B+Tree比B-Tree更适合作为外存索引的数据结构？
原因和内节点出度d有关。从上面分析可以看到，d越大索引的性能越好，而出度的上限取决于节点内key和data的大小：
dmax=floor(pagesize/(keysize+datasize+pointsize))
floor表示向下取整。由于B+Tree内节点去掉了data域，因此可以拥有更大的出度，拥有更好的性能（检索节点次数/IO次数降低）。

#### 为什么不使用二叉树进行查找？
二叉树的一个缺点是无法保证平衡性，即存在所有节点都在一侧的情况，这样就是一条线，查询效率变成了线性查找。所以就需要`平衡二叉树`，它的左子树和右子树的高度之差绝对值小于1
，这样就不会出现一条支路特别长的情况。
在这样的平衡树中进行查找时，总共比较节点的次数不超过树的高度，这就确保了查询的效率（时间复杂度为O(logn)）。
B树事实上是一种平衡的多叉查找树，也就是说最多可以开m个叉（m>=2），我们称之为m阶B树。

#### B+Tree索引和哈希索引的区别
哈希索引适合等值查询，但是无法进行范围查询，也没有办法利用索引完成排序。哈希索引不支持多列联合索引的最左匹配规则，如果有大量重复键值的情况下，哈希索引的效率会很低，因为存在哈希碰撞的问题。

#### 建立了索引就一定会被使用吗？
不一定。这个主要跟查询优化器有关，它会根据当前SQL，查询优化器会：1.根据搜索条件，找出所有可能使用的索引；2.计算全表扫描的代价；3.计算使用不同的索引执行查询的代价；4
.对比各种方案执行的代价，选择成本最低的那个

#### InnoDB一棵B+树可以存放多少行数据？
InnoDB存储引擎的最小储存单元是 `页（Page）` ，一个页的大小是默认是 `16K` 。磁盘存储数据最小单元是 `扇区` ，一个扇区的大小是 `512字节` ，
而文件系统（例如XFS/EXT4）它的最小单元是 `块` ，一个块的大小是 `4k` 。

InnoDB的所有数据文件（后缀为 *.ibd* 的文件），它的大小始终都是16384B（16k）的整数倍。 可以用以下语句进行查看：
> show variables like 'innodb_page_size';

数据表中的数据都是存储在页中的，所以一个页中能存储多少行数据呢？假设一行数据的大小是1k，那么一个页可以存放16行这样的数据。

但是除了有 `存放数据的页` 以外，还有 `存放键值+指针的页` ，即B+树中的非叶子节点，该页存放键值和指向数据页的指针，这样的页由N个（键值+指针）组成。当然它也是排好序的。
这样的数据组织形式，我们称为「索引组织表」。索引组织表通过非叶子节点的「二分查找法」以及指针确定数据在哪个页中，进而在去数据页中查找到需要的数据。

这里我们先假设B+树高为2，即存在一个根节点和若干个叶子节点，那么这棵B+树的存放总记录数为：`根节点指针数*单个叶子节点记录行数`。

那么现在我们需要计算出非叶子节点能存放多少指针？

我们假设主键ID为 `bigint` 类型，长度为8字节，而 `指针大小在InnoDB源码中设置为6字节` ，这样一共14字节。

我们一个页中能存放多少这样的单元，其实就代表有多少指针，即 16384/14=1170。

那么可以算出一棵高度为2的B+树，能存放1170*16=18720条这样的数据记录。

根据同样的原理我们可以算出一个高度为3的B+树可以存放：1170（根存的记录指针数据）*1170（下一级每个节点存的记录指针数据）*16（每个叶子阶段存的数据条数）=21902400
条这样的记录，即2100w量级。

所以在InnoDB中B+树高度一般为1-3层，它就能满足千万级的数据存储。

在查找数据时一次页的查找代表一次 `IO` ，所以通过主键索引查询通常只需要1-3次 `IO` 操作即可查找到数据，即使一个是千万量级的表，也是很快的。


#### 怎么得到InnoDB主键索引B+树的高度？

在InnoDB的表空间文件中，约定 `page number` 为 3 的代表主键索引的根页，而在根页偏移量为 64 的地方存放了该B+树的 `page level` 。

如果 `page level` 为1，树高为2， `page level` 为2，则树高为3。即`B+树的高度=page level + 1` 。
#### ORDER BY 如何使用索引?
要说 `ORDER BY` 如何利用索引进行排序，得先弄清楚 `ORDER BY` 本身是如何进行排序的。
在 MySQL 中，会给「每个线程」分配一块内存空间 buffer 用于排序，还有一个参数叫做 `max_length_for_sort_data` ，
这个参数作用是 `用来规定排序返回行的字段长度` ，默认值是 1024，最小值为 
4，如果排序返回行的字段长度没有超过这个参数的值，就会使用一次访问+排序，否则使用访问+排序+访问。

> SELECT name, age, employee_id FROM employees WHERE name='elsef' ORDER BY employee_id;

现在我要查的排序的返回字段只包括 name, age 和 employee_id，在默认情况下肯定不会超过 1024，所以会使用一次访问排序，流程如下：

- 初始化 buffer
- 根据最左匹配原则命中 name 为 'elsef' 的值，根据辅助索引找出主键 id；
- 根据主键 id 取出整行的值，然后将 name, age 和 employee_id 这三个返回列的的值存入到 buffer 中；
- 重复以上 2 和 3 的步骤，直到不再满足查询条件为止；
- 对 buffer 中的数据根据 employee_id 进行排序；
- 将排序结果返回；

那么假设我现在的 `max_length_for_sort_data` 
的值很小，要查询的返回子段长度超过了这个值，那就会变成这样的流程：精简取出字段范围（buffer不够嘛）-》按字段排序buffer内容-》回表获取其他字段，
即二次访问流程变长，流程如下：

- 初始化 buffer
- 根据最左匹配原则命中 name 为 'elsef' 的值，根据辅助索引找出主键 id；
- 根据主键 id 取出整行的值，然后将排序行 employee_id 以及 primary key 的值存入到 buffer 中；
- 重复以上 2 和 3 的步骤，直到不再满足查询条件为止；
- 对 buffer 中的数据根据 employee_id 进行排序；
- 根据排序结果中的 primary key，就会回表操作，并将最终结果返回；

以上两种排序，无非是 MySQL 认为内存够不够用，够用的话就多利用内存而避免过多的回表操作从而增加磁盘访问。那如果排序申请的内存空间不过用了怎么办？
参数 `sort_buffer_size` 就是控制排序内存空间大小的，如果内存不够用，就会使用磁盘临时文件做外部「归并排序」。

知道了以上排序操作，再结合之前覆盖索引以及 B+ Tree 索引的逻辑，是不能就有办法去优化 ORDER BY 的流程了？
首先，不管是一次访问排序还是二次访问排序，都要在 buffer 对数据做排序操作，而 B+ Tree 本身的叶子结点就是有序排列的，
所以只要能做到排序行也能按照最左匹配原则匹配到索引，就可以避免内存排序的步骤了。
另外，上述的排序步骤中还需要进行回表操作，那么只要查询的语句能命中覆盖索引，是不是就能够避免回表操作了。进一步，如何可以使用同一个索引既满足排序又用于查找行那就相当不错了。

#### 唯一索引查询不命中是什么情况？
比如表 employees 的 employee_id 字段为varchar类型且创建了唯一索引，那么下面的查询方式会使用索引吗？

> SELECT * FROM employees WHERE employee_id=11;

答案是不会，因为employee_id 是 varchar 类型，但这个查询语句中将其与数字类型做比较，这时候会触发 MySQL 的隐式类型转换，将字符串转换成数字进行比较，也就是说上述的语句相当于：

> SELECT * FROM employees WHERE CAST(employee_id AS int)=11;

也就是说，在这个查询中对索引字段做了函数操作，而这样的话会破坏索引值的有序性，于是不会命中索引，转而进行全表扫描。

#### 无法满足最左前缀的查询如何优化？
如果查询条件不是联合索引的最左字段，则无法命中索引，如下面的查询（联合索引为(name,age,gender)）：
> SELECT * FROM employees WHERE age=17;

此时可以给跳过的那个索引的列使用 `IN` 的方式让其发生「最左前缀匹配」，当然这里的例子name并不是很适合用 `IN` ，样本太大。

所以更妥善的办法是为age单独创建索引或者创建以它为前缀的联合索引。
#### 页分裂问题
InnoDB 中数据是存储在数据页中的，而数据是按照索引的顺序插入到数据页中的，所以数据是紧凑排序的，但如果随机对数据进行插入，就有可能导致数据页分裂的问题。

假设一个数据页只能存储 3 条数据，且已经有 3 条数据（100， 200， 300）了，这时候想插入一条 150 的数据，就会再申请一个新的数据页，100，150 两条数据存放在原来的数据页中，200 和 300 存放在新的数据页中，这样可能会存在数据页利用率不高的问题。

> 不仅仅是插入数据会导致上述问题，删除数据也会。这里要注意，如果删除掉了一个数据页中的某条数据，这条数据所留下的位置并不会缩小而是等待复用，如果是一整个页的数据被删除了，那这个页也是处于被复用状态。
如果相邻的两个数据页的利用率很小，系统会把这两个页的数据合到其中一个页上，另一个页就处于可被复用的状态。所以通过 delete 删除数据并不会回收表空间。

为了解决频繁删除数据导致的没有回收表空间的问题，可以通过「重建表」来解决，比如以下命令：
> alter table table_name engine=InnoDB;

这个命令的流程基本上是：

- 新建一个临时表，结果同原表相同；
- 按照主键 id 递增的顺序将数据从原表读出插入到新表中；
- 用新的表替换旧表，删除旧表；

所以我们使用 `AUTO INCREMENT` 主键的插入数据模式，正符合了递增插入的场景。每次插入一条新记录，都是追加操作，都不涉及到挪动其他记录，也不会触发叶子节点的分裂。

#### 一个SQL的执行到获取数据是怎样的过程？
![mysql-process](/images/in-post/mysql-process.jpg)
- 1.当客户端连接到MySQL服务器时，服务器对其进行认证。可以通过用户名与密码认证，也可以通过SSL证书进行认证。登录认证后，服务器还会验证客户端是否有执行某个查询的操作权限。
- 2.在正式查询之前，服务器会检查查询缓存，如果能找到对应的查询，则不必进行查询解析，优化，执行等过程，直接返回缓存中的结果集。
- 3.MySQL的解析器会根据查询语句，构造出一个解析树，主要用于根据语法规则来验证语句是否正确，比如SQL的关键字是否正确，关键字的顺序是否正确。
而预处理器主要是进一步校验，比如表名，字段名是否正确等
- 4.查询优化器将解析树转化为查询计划，一般情况下，一条查询可以有很多种执行方式，最终返回相同的结果，优化器就是根据成本找到这其中最优的执行计划
- 5.执行计划调用查询执行引擎，而查询引擎通过一系列API接口查询到数据
- 6.得到数据之后，在返回给客户端的同时，会将数据存在查询缓存中

#### 为什么一般不用查询缓存？
MYSQL的查询缓存实质上是缓存SQL的hash值和该SQL的查询结果，如果运行相同的SQL，服务器直接从缓存中去掉结果，而不再去解析、优化、寻找最低成本的执行计划等一系列操作，大大提升了查询速度。
但是它有一些弊端：
- 1) 读查询开始之前必须检查是否命中缓存，包括计算hash在高并发时性能有一定影响。
- 2) 如果读查询可以缓存，那么执行完查询操作后，会查询结果和查询语句写入缓存。
- 3) 当向某个表写入数据的时候，必须将这个表所有的缓存设置为失效，如果缓存空间很大，则消耗也会很大，可能使系统僵死一段时间，因为这个操作是靠全局锁操作来保护的。
- 4) 对InnoDB表，当修改一个表时，设置了缓存失效，但是多版本特性会暂时将这修改对其他事务屏蔽，在这个事务提交之前，所有查询都无法使用缓存，直到这个事务被提交，所以长时间的事务，会大大降低查询缓存的命中
> 可以通过 `show variables like '%query_cache%'` 来看一下默认的数据库配置，如果 `query_cache_type` 为 OFF 则证明关闭了查询缓存。

#### 如何判断一个索引建立的是否好呢？
可以用 `show index from` 指令查看 `Cardinality` 值，这个值是一个预估值，而不是一个准确值。每次对 `Cardinality` 值的统计都是随机取8个叶子节点得到的。
实际应用中，（Cardinality/行数）应该尽量接近1。如果非常小则要考虑是否需要此索引。

#### 优化器如何得出哪中扫描方式效果最佳？
我们知道每一条SQL都有不同的执行方法，要不通过索引，要不通过全表扫描的方式。MySQL是如何选择时间最短，占用内存最小的执行方法，这就是成本最小法。
关于成本：
- 1.I/O成本。数据存储在硬盘上，我们想要进行某个操作需要将其加载到内存中，这个过程的时间被称为I/O成本。默认是1。加载单位是页。
- 2.CPU成本。在内存对结果集进行排序的时间被称为CPU成本。默认是0.2，结果集大小用Rows表示。

这里介绍一下如何评估全表的成本和索引的扫描成本
我们通过 `show table status like ‘xx_tb’` 命令知道rows和data_length字段：
- rows：表示表中的记录条数，但是这个数据不准确，是个估计值。
- data_length:表示表占用的存储空间字节数。

因为，`data_length=聚簇索引的页面数量 * 每个页面的大小` ，所以我们可以反推出游多少个聚簇索引的页面，页面默认16K，得到具体的值后，
分别计算IO成本（页面数*1）和CPU成本（Rows*0.2），加和就是总成本，索引页面越多成本越高，所以全表扫描是性能很差的。

对与使用不同索引执行查询的成本计算，因为要查询出满足条件的所有字段信息，所以要考虑回表成本。
如一条通过主键进行精确查询的SQL：

I/O成本=1+1*1=2(范围区间的数量+预计二级记录索引条数)

CPU成本=1*0.2+1*0.2=0.4(读取二级索引的成本+回表聚簇索引的成本)

对于两表连接查询来说，它的查询成本由下面两个部分构成：
- 单次查询驱动表的成本
- 多次查询被驱动表的成本（具体查询多次取决于对驱动表查询的结果集有多少个记录）

#### References
- http://blog.jobbole.com/105644/
- https://zhuanlan.zhihu.com/p/78063756
- https://zhuanlan.zhihu.com/p/84493668
- https://icell.io/how-mysql-index-works/
- https://tech.meituan.com/2014/06/30/mysql-index.html
- https://juejin.im/post/5dfc846051882512327a63b6

> 本文首次发布于 [StuartLau's Blog](https://stuartlau.github.io), 
转载请保留原文链接.
