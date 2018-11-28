---
layout:     post
title:      "经常被误解的MySQL隔离级别REPEATABLE-READ"
subtitle:   "MySQL and PhantomRead Misconception"
date:       2018-11-28
author:     SL
header-img: img/post-bg-universe.jpg
catalog: true
tags: 
    - MySQL
    - PhantomRead
    - Isolation
---

# 啥是幻读
> The so-called phantom problem occurs within a transaction when the same query produces different sets of rows at different times. For example, if a SELECT is executed twice, but returns a row the second time that was not returned the first time, the row is a “phantom” row.

# MySQL解决幻读

MySQL的InnoDb存储引擎默认的隔离级别是REPEATABLE-READ
，即可重复读。那什么是可重复读呢，简单来说就是一个事务里的两个相同条件的查询查到的结果应该是一致的，即结果是「可以重复读到的」，所以就解决了「幻读」。
如果做不到可重复读，如READ-COMMITTED
隔离级别，由于一个事务执行过程中可能读到其他事务已经提交的数据，那么按照上面的描述「一个事务里的两个相同条件的查询查到的结果应该是一致的」这个就无法达到了，因为结果集合可以新增，跟之前读的结果不一样多，就幻觉读了。

OK，那是不是使用了REPEATABLE-READ隔离级别就万事大吉了呢？

# REPEATABLE-READ的误解

##误解一
> REPEATABLE-READ肯定不会读到隔壁事务已经提交的数据，即使某个数据已经由隔壁事务提交，当前事务插入不会报错，否则就是发生了幻读。

简单来说前半句话是对的，后半句有什么问题呢？可REPEATABLE-READ
其实跟「写操作」无关，当前事务读不到的数据并不一定是不存在的，如果存在，那么当前事务尝试插入的时候是可能会失败的。
而插入失败的原因可能是因为主键冲突导致数据库报异常，跟隔离级别无直接关系。任何隔离级别下插入已经存在的数据都会报错。
看不到并不代表没有，并不代表可以自以为然的插入无忧。

## 误解二
> REPEATABLE-READ的事务里查不到的数据一定是不存在的，所以我可以放心插入，100%成功。

这个观点也是错的，查不到只能说明当前事务里读不到，并不代表此时其他事务没有插入这样的数据。
如何保证判断某个数据不存在以后其他事务也不会插入成功？答案是上锁。不上锁是无法阻止其他事务插入的。
> SELECT * FROM table1 WHERE id >100

上面这个语句在事务里判断后如果不存在数据是无法保证其他事务插入符合条件的数据的，需要加锁
> SELECT * FROM table1 WHERE id >100 FOR UPDATE;

此时如果有隔壁事务尝试插入大于100的id的数据则会等待当前事务释放锁，直到超时后中断当前事务。
> (waiting for lock ...
   then timeout)
  ERROR 1205 (HY000):
  Lock wait timeout exceeded;
  try restarting transaction
  
但是如果当前事务使用的加锁的条件仅仅是某一个行锁的话最多会在前后加next-key locking，影响范围较小，但仍然可能阻塞其他事务的插入，如恰好新数据的位置被gap 
locking锁住了，那只能等待当前事务释放锁了。

说了这么多，有一点要注意，就是这个next-key locking一定是在REPEATABLE-READ下才有，READ-COMMITTED是不存在的。

> To prevent phantoms, InnoDB uses an algorithm called next-key locking that combines index-row locking with gap locking.
  You can use next-key locking to implement a uniqueness check in your application: If you read your data in share mode and do not see a duplicate for a row you are going to insert, then you can safely insert your row and know that the next-key lock set on the successor of your row during the read prevents anyone meanwhile inserting a duplicate for your row. Thus, the next-key locking enables you to “lock” the nonexistence of something in your table.
  
即InnoDb提供next-key locking机制，但是需要业务自己去加锁，如果不加锁，只是简单的select查询，是无法限制并行的插入的。


## 误解三
> 凡是REPEATABLE-READ中的读都无法读取最新的数据。

这个观点也是错误的，虽然我们读取的记录都是可重复读取的，但是如果你想读取最新的记录可以用加锁的方式读。
> If you want to see the “freshest” state of the database, you should use either the READ COMMITTED isolation level or a locking read:

以下任意一种均：
- SELECT * FROM table1 LOCK IN SHARE MODE;
- SELECT * FROM table1 FOR UPDATE;
  
  
# 参考
- https://dev.mysql.com/doc/refman/5.0/en/innodb-record-level-locks.html
- https://dev.mysql.com/doc/refman/8.0/en/innodb-next-key-locking.html

> 本文首次发布于 [ElseF's Blog](http://elsef.com), 作者 [@stuartlau](http://github.com/stuartlau) ,转载请保留原文链接.
