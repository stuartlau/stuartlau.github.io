---
layout:     post
title:      "MySQL对批量提交ON-DUPLICATE-KEY的优化测试"
subtitle:   "MySQL's Optimization for ON-DUPLICATE-KEY with BatchUpdate"
date:       2018-12-20
author:     SL
header-img: img/post-bg-universe.jpg
catalog: true
tags:
    - MySQL
---
> 接上一篇对MySQL内部对批量提交的ON-DUPLICATE-KEY的优化的分析，本文通过实际测试看一下内部执行SQL时是否会做优化处理。MySQL版本：Mac 5.7.21-log。
# 正常的批量提交
如果是合法的SQL语句，则在batchUpdate提交时无论下面哪种方式都会成功执行。
SQL1
```java
private static final String INSERT_SQL1 = "INSERT INTO %s"
            + "(app_id, group_id, user_id, status, member_role, inviter_id, "
            + "group_member_setting, nickname, create_time, update_time, last_join_time) "
            + "VALUES(:app_id, :group_id, :user_id, :status, :member_role, :inviter_id, "
            + ":group_member_setting, :nickname, :create_time, :update_time, :last_join_time) "
            + "ON DUPLICATE KEY UPDATE status = VALUES(status), member_role = VALUES(member_role), "
            + "inviter_id = VALUES(inviter_id), group_member_setting = VALUES(group_member_setting), nickname = VALUES(nickname), "
            + "update_time = VALUES(update_time), last_join_time = VALUES(last_join_time)";
```
SQL2
```java
private static final String INSERT_SQL2 = "INSERT INTO %s"
            + "(`app_id`,`group_id`,`user_id`,`status`,`member_role`,`inviter_id`,`group_member_setting`,`nickname`,"
            + " `create_time`,`update_time`,`last_join_time`)"
            + " VALUES(:app_id,:group_id,:user_id,:status,:member_role,:inviter_id,:group_member_setting,:nickname,"
            + " :create_time,:update_time,:last_join_time) "
            + " ON DUPLICATE KEY UPDATE `status`=:status,`member_role` =:member_role,"
            + " `inviter_id`=:inviter_id,`group_member_setting`=:group_member_setting,`nickname`=:nickname,"
            + " `update_time`=:update_time,`last_join_time`=:last_join_time ";
```
二者的区别在于，一个使用了MySQL内置的VALUES()函数，一个通过占位符的方式，这两种方式spring-jdbc均可以正常处理。我们需要验证在MySQL内部前一种写法在批量提交时是否会被拼成一个SQL执行，而后者由于写法的限制，只能是当做多条SQL执行。

## 场景
我们模拟batchUpdate更新三条数据的case，其中包括两个已经存在的唯一索引的数据，即其中第一第二条SQL数据的唯一索引冲突，并且和数据库内已存在数据唯一索引冲突，第三条SQL只和数据库内已存在数据唯一索引冲突。

### SQL1 BINLOG
```sql
#181221 10:58:21 server id 1  end_log_pos 6058 CRC32 0x992efebc 	Query	thread_id=44	exec_time=0	error_code=0
SET TIMESTAMP=1545361101/*!*/;
BEGIN
/*!*/;
# at 6058
#181221 10:58:21 server id 1  end_log_pos 6129 CRC32 0xf744919e 	Table_map: `test`.`group_member_0` mapped to number 108
# at 6129
#181221 10:58:21 server id 1  end_log_pos 6315 CRC32 0xc2786982 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
zVYcXBMBAAAARwAAAPEXAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQAJ6RRPc=
zVYcXB8BAAAAugAAAKsYAAAAAGwAAAAAAAEAAgAM/////wDwogAAAAAAAAACAAAAbwAAAAAAAABz
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAABCnyszmcBAAAWT53OZwEAAAp8rM5nAQAAAPCiAAAA
AAAAAAIAAABvAAAAAAAAAHMAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAAILD7POZwEAABZPnc5n
AQAACw+zzmcBAACCaXjC
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545360669706 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545360669706 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=2 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545361100555 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545361100555 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 6315
#181221 10:58:21 server id 1  end_log_pos 6346 CRC32 0xfcad82a2 	Xid = 498
COMMIT/*!*/;
# at 6346
#181221 10:58:21 server id 1  end_log_pos 6411 CRC32 0x42089998 	Anonymous_GTID	last_committed=16	sequence_number=17	rbr_only=yes
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 6411
#181221 10:58:21 server id 1  end_log_pos 6483 CRC32 0x434a1aba 	Query	thread_id=44	exec_time=0	error_code=0
SET TIMESTAMP=1545361101/*!*/;
BEGIN
/*!*/;
# at 6483
#181221 10:58:21 server id 1  end_log_pos 6554 CRC32 0x38dd54f9 	Table_map: `test`.`group_member_0` mapped to number 108
# at 6554
#181221 10:58:21 server id 1  end_log_pos 6740 CRC32 0x41c5822b 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
zVYcXBMBAAAARwAAAJoZAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQAPlU3Tg=
zVYcXB8BAAAAugAAAFQaAAAAAGwAAAAAAAEAAgAM/////wDwogAAAAAAAAACAAAAbwAAAAAAAABz
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAACCw+zzmcBAAAWT53OZwEAAAsPs85nAQAAAPCiAAAA
AAAAAAIAAABvAAAAAAAAAHMAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAAEPD7POZwEAABZPnc5n
AQAADw+zzmcBAAArgsVB
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=2 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545361100555 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545361100555 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545361100559 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545361100559 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 6740
#181221 10:58:21 server id 1  end_log_pos 6771 CRC32 0xd6a86361 	Xid = 499
COMMIT/*!*/;
# at 6771
#181221 10:58:21 server id 1  end_log_pos 6836 CRC32 0x308eb1a4 	Anonymous_GTID	last_committed=17	sequence_number=18	rbr_only=yes
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 6836
#181221 10:58:21 server id 1  end_log_pos 6908 CRC32 0xff40c48c 	Query	thread_id=44	exec_time=0	error_code=0
SET TIMESTAMP=1545361101/*!*/;
BEGIN
/*!*/;
# at 6908
#181221 10:58:21 server id 1  end_log_pos 6979 CRC32 0x6800fd9d 	Table_map: `test`.`group_member_0` mapped to number 108
# at 6979
#181221 10:58:21 server id 1  end_log_pos 7165 CRC32 0x7dfa32b4 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
zVYcXBMBAAAARwAAAEMbAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQAJ39AGg=
zVYcXB8BAAAAugAAAP0bAAAAAGwAAAAAAAEAAgAM/////wDwpAAAAAAAAAACAAAAbwAAAAAAAAB0
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAABCnyszmcBAAAZT53OZwEAAAp8rM5nAQAAAPCkAAAA
AAAAAAIAAABvAAAAAAAAAHQAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAAEPD7POZwEAABlPnc5n
AQAADw+zzmcBAAC0Mvp9
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=164 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=116 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545360669706 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545360669706 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=164 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=116 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545361100559 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545361100559 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 7165
#181221 10:58:21 server id 1  end_log_pos 7196 CRC32 0xa6c18e7a 	Xid = 500
COMMIT/*!*/;
SET @@SESSION.GTID_NEXT= 'AUTOMATIC' /* added by mysqlbinlog */ /*!*/;
DELIMITER ;
# End of log file
/*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE*/;
/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=0*/;
```

### SQL2 BINLOG
```sql
#181221 10:51:10 server id 1  end_log_pos 4711 CRC32 0x8bb9a5a2 	Anonymous_GTID	last_committed=12	sequence_number=13	rbr_only=yes
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 4711
#181221 10:51:10 server id 1  end_log_pos 4783 CRC32 0x4d13dbe9 	Query	thread_id=43	exec_time=0	error_code=0
SET TIMESTAMP=1545360670/*!*/;
BEGIN
/*!*/;
# at 4783
#181221 10:51:10 server id 1  end_log_pos 4854 CRC32 0xc20ff385 	Table_map: `test`.`group_member_0` mapped to number 108
# at 4854
#181221 10:51:10 server id 1  end_log_pos 5040 CRC32 0x0ee5ae17 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
HlUcXBMBAAAARwAAAPYSAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQAIXzD8I=
HlUcXB8BAAAAugAAALATAAAAAGwAAAAAAAEAAgAM/////wDwogAAAAAAAAACAAAAbwAAAAAAAABz
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAABGU+dzmcBAAAWT53OZwEAABlPnc5nAQAAAPCiAAAA
AAAAAAIAAABvAAAAAAAAAHMAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAAICfKzOZwEAABZPnc5n
AQAAAnyszmcBAAAXruUO
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=2 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545360669698 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545360669698 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 5040
#181221 10:51:10 server id 1  end_log_pos 5071 CRC32 0xca9bfb4e 	Xid = 485
COMMIT/*!*/;
# at 5071
#181221 10:51:10 server id 1  end_log_pos 5136 CRC32 0x6dabc854 	Anonymous_GTID	last_committed=13	sequence_number=14	rbr_only=yes
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 5136
#181221 10:51:10 server id 1  end_log_pos 5208 CRC32 0x9d3f46fe 	Query	thread_id=43	exec_time=0	error_code=0
SET TIMESTAMP=1545360670/*!*/;
BEGIN
/*!*/;
# at 5208
#181221 10:51:10 server id 1  end_log_pos 5279 CRC32 0x4efaeb04 	Table_map: `test`.`group_member_0` mapped to number 108
# at 5279
#181221 10:51:10 server id 1  end_log_pos 5465 CRC32 0x2cc63690 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
HlUcXBMBAAAARwAAAJ8UAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQAATr+k4=
HlUcXB8BAAAAugAAAFkVAAAAAGwAAAAAAAEAAgAM/////wDwogAAAAAAAAACAAAAbwAAAAAAAABz
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAACAnyszmcBAAAWT53OZwEAAAJ8rM5nAQAAAPCiAAAA
AAAAAAIAAABvAAAAAAAAAHMAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAAEKfKzOZwEAABZPnc5n
AQAACnyszmcBAACQNsYs
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=2 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545360669698 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545360669698 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545360669706 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545360669706 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 5465
#181221 10:51:10 server id 1  end_log_pos 5496 CRC32 0xa99922e6 	Xid = 486
COMMIT/*!*/;
# at 5496
#181221 10:51:10 server id 1  end_log_pos 5561 CRC32 0xe8027f36 	Anonymous_GTID	last_committed=14	sequence_number=15	rbr_only=yes
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 5561
#181221 10:51:10 server id 1  end_log_pos 5633 CRC32 0xd762eacd 	Query	thread_id=43	exec_time=0	error_code=0
SET TIMESTAMP=1545360670/*!*/;
BEGIN
/*!*/;
# at 5633
#181221 10:51:10 server id 1  end_log_pos 5704 CRC32 0x16d7fa64 	Table_map: `test`.`group_member_0` mapped to number 108
# at 5704
#181221 10:51:10 server id 1  end_log_pos 5890 CRC32 0x6fc61c8c 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
HlUcXBMBAAAARwAAAEgWAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQAGT61xY=
HlUcXB8BAAAAugAAAAIXAAAAAGwAAAAAAAEAAgAM/////wDwpAAAAAAAAAACAAAAbwAAAAAAAAB0
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAABGU+dzmcBAAAZT53OZwEAABlPnc5nAQAAAPCkAAAA
AAAAAAIAAABvAAAAAAAAAHQAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAAEKfKzOZwEAABlPnc5n
AQAACnyszmcBAACMHMZv
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=164 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=116 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=164 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=116 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545360669706 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545360669706 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 5890
#181221 10:51:10 server id 1  end_log_pos 5921 CRC32 0x8c32a3ee 	Xid = 487
COMMIT/*!*/;
SET @@SESSION.GTID_NEXT= 'AUTOMATIC' /* added by mysqlbinlog */ /*!*/;
DELIMITER ;
# End of log file
/*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE*/;
/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=0*/;
```

### SQL1 general_log
```sql
2018-12-21T02:58:21.189301Z        44 Connect   root@localhost on test using TCP/IP
2018-12-21T02:58:21.204860Z        44 Query     /* mysql-connector-java-5.1.43 ( Revision: 1d14b699eff3e6112aaedb1cbe5a151ab81f98f1 ) */SELECT  @@session.auto_increment_increment AS auto_increment_increment, @@character_set_client AS character_set_client, @@character_set_connection AS character_set_connection, @@character_set_results AS character_set_results, @@character_set_server AS character_set_server, @@collation_server AS collation_server, @@init_connect AS init_connect, @@interactive_timeout AS interactive_timeout, @@license AS license, @@lower_case_table_names AS lower_case_table_names, @@max_allowed_packet AS max_allowed_packet, @@net_buffer_length AS net_buffer_length, @@net_write_timeout AS net_write_timeout, @@have_query_cache AS have_query_cache, @@sql_mode AS sql_mode, @@system_time_zone AS system_time_zone, @@time_zone AS time_zone, @@tx_isolation AS tx_isolation, @@wait_timeout AS wait_timeout
2018-12-21T02:58:21.244181Z        44 Query     SHOW WARNINGS
2018-12-21T02:58:21.246129Z        44 Query     SELECT @@query_cache_size AS query_cache_size, @@query_cache_type AS query_cache_type
2018-12-21T02:58:21.246437Z        44 Query     SHOW WARNINGS
2018-12-21T02:58:21.247406Z        44 Query     SET character_set_results = NULL
2018-12-21T02:58:21.247740Z        44 Query     SELECT @@session.autocommit
2018-12-21T02:58:21.272929Z        44 Query     select @@session.tx_read_only
2018-12-21T02:58:21.273544Z        44 Query     INSERT INTO group_member_0(app_id, group_id, user_id, status, member_role, inviter_id, group_member_setting, nickname, create_time, update_time, last_join_time) VALUES(2, 111, 115, 1, 2, 115, 0, '', 1545361100555, 1545361100555, 1545361100555) ON DUPLICATE KEY UPDATE status = VALUES(status), member_role = VALUES(member_role), inviter_id = VALUES(inviter_id), group_member_setting = VALUES(group_member_setting), nickname = VALUES(nickname), update_time = VALUES(update_time), last_join_time = VALUES(last_join_time)
2018-12-21T02:58:21.301404Z        44 Query     INSERT INTO group_member_0(app_id, group_id, user_id, status, member_role, inviter_id, group_member_setting, nickname, create_time, update_time, last_join_time) VALUES(2, 111, 115, 1, 1, 115, 0, '', 1545361100559, 1545361100559, 1545361100559) ON DUPLICATE KEY UPDATE status = VALUES(status), member_role = VALUES(member_role), inviter_id = VALUES(inviter_id), group_member_setting = VALUES(group_member_setting), nickname = VALUES(nickname), update_time = VALUES(update_time), last_join_time = VALUES(last_join_time)
2018-12-21T02:58:21.315700Z        44 Query     INSERT INTO group_member_0(app_id, group_id, user_id, status, member_role, inviter_id, group_member_setting, nickname, create_time, update_time, last_join_time) VALUES(2, 111, 116, 1, 1, 115, 0, '', 1545361100559, 1545361100559, 1545361100559) ON DUPLICATE KEY UPDATE status = VALUES(status), member_role = VALUES(member_role), inviter_id = VALUES(inviter_id), group_member_setting = VALUES(group_member_setting), nickname = VALUES(nickname), update_time = VALUES(update_time), last_join_time = VALUES(last_join_time)
2018-12-21T02:58:21.333553Z        44 Quit
```

### SQL2 general_log
```sql
2018-12-21T02:51:10.235590Z        43 Connect   root@localhost on test using TCP/IP
2018-12-21T02:51:10.242696Z        43 Query     /* mysql-connector-java-5.1.43 ( Revision: 1d14b699eff3e6112aaedb1cbe5a151ab81f98f1 ) */SELECT  @@session.auto_increment_increment AS auto_increment_increment, @@character_set_client AS character_set_client, @@character_set_connection AS character_set_connection, @@character_set_results AS character_set_results, @@character_set_server AS character_set_server, @@collation_server AS collation_server, @@init_connect AS init_connect, @@interactive_timeout AS interactive_timeout, @@license AS license, @@lower_case_table_names AS lower_case_table_names, @@max_allowed_packet AS max_allowed_packet, @@net_buffer_length AS net_buffer_length, @@net_write_timeout AS net_write_timeout, @@have_query_cache AS have_query_cache, @@sql_mode AS sql_mode, @@system_time_zone AS system_time_zone, @@time_zone AS time_zone, @@tx_isolation AS tx_isolation, @@wait_timeout AS wait_timeout
2018-12-21T02:51:10.322737Z        43 Query     SHOW WARNINGS
2018-12-21T02:51:10.325503Z        43 Query     SELECT @@query_cache_size AS query_cache_size, @@query_cache_type AS query_cache_type
2018-12-21T02:51:10.325862Z        43 Query     SHOW WARNINGS
2018-12-21T02:51:10.327032Z        43 Query     SET character_set_results = NULL
2018-12-21T02:51:10.327478Z        43 Query     SELECT @@session.autocommit
2018-12-21T02:51:10.354978Z        43 Query     select @@session.tx_read_only
2018-12-21T02:51:10.355539Z        43 Query     INSERT INTO group_member_0(`app_id`,`group_id`,`user_id`,`status`,`member_role`,`inviter_id`,`group_member_setting`,`nickname`, `create_time`,`update_time`,`last_join_time`) VALUES(2, 111,115,1,2,115,0,'', 1545360669698,1545360669698,1545360669698)  ON DUPLICATE KEY UPDATE `status`=1,`member_role` =2, `inviter_id`=115,`group_member_setting`=0,`nickname`='', `update_time`=1545360669698,`last_join_time`=1545360669698
2018-12-21T02:51:10.473833Z        43 Query     INSERT INTO group_member_0(`app_id`,`group_id`,`user_id`,`status`,`member_role`,`inviter_id`,`group_member_setting`,`nickname`, `create_time`,`update_time`,`last_join_time`) VALUES(2, 111,115,1,1,115,0,'', 1545360669706,1545360669706,1545360669706)  ON DUPLICATE KEY UPDATE `status`=1,`member_role` =1, `inviter_id`=115,`group_member_setting`=0,`nickname`='', `update_time`=1545360669706,`last_join_time`=1545360669706
2018-12-21T02:51:10.485740Z        43 Query     INSERT INTO group_member_0(`app_id`,`group_id`,`user_id`,`status`,`member_role`,`inviter_id`,`group_member_setting`,`nickname`, `create_time`,`update_time`,`last_join_time`) VALUES(2, 111,116,1,1,115,0,'', 1545360669706,1545360669706,1545360669706)  ON DUPLICATE KEY UPDATE `status`=1,`member_role` =1, `inviter_id`=115,`group_member_setting`=0,`nickname`='', `update_time`=1545360669706,`last_join_time`=1545360669706
2018-12-21T02:51:10.498312Z        43 Quit
```
### 总结
可以通过上面的BINLOG和general_log看到两个SQL在MySQL内部执行时都是分成了3条独立的事务执行，有不同的事务ID。默认情况下**SELECT @@session.autocommit**返回值为1，即开启了自动提交，而由于我们使用的是writer库，所以**select @@session.tx_read_only**返回值为0，即不是read_only模式。

### 开启事务 SQL1 BINLOG
```sql
#181221 10:58:21 server id 1  end_log_pos 7196 CRC32 0xa6c18e7a 	Xid = 500
COMMIT/*!*/;
# at 7196
#181221 11:28:30 server id 1  end_log_pos 7261 CRC32 0x4fd0d0ad 	Anonymous_GTID	last_committed=18	sequence_number=19	rbr_only=yes
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 7261
#181221 11:27:30 server id 1  end_log_pos 7333 CRC32 0x8c7eba3b 	Query	thread_id=45	exec_time=0	error_code=0
SET TIMESTAMP=1545362850/*!*/;
BEGIN
/*!*/;
# at 7333
#181221 11:27:30 server id 1  end_log_pos 7404 CRC32 0x598d7b13 	Table_map: `test`.`group_member_0` mapped to number 108
# at 7404
#181221 11:27:30 server id 1  end_log_pos 7590 CRC32 0x8d18a9bd 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
ol0cXBMBAAAARwAAAOwcAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQABN7jVk=
ol0cXB8BAAAAugAAAKYdAAAAAGwAAAAAAAEAAgAM/////wDwogAAAAAAAAACAAAAbwAAAAAAAABz
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAABDw+zzmcBAAAWT53OZwEAAA8Ps85nAQAAAPCiAAAA
AAAAAAIAAABvAAAAAAAAAHMAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAAKMnM3OZwEAABZPnc5n
AQAAjJzNzmcBAAC9qRiN
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545361100559 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545361100559 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=2 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545362840716 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545362840716 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 7590
#181221 11:27:30 server id 1  end_log_pos 7661 CRC32 0x26f062e4 	Table_map: `test`.`group_member_0` mapped to number 108
# at 7661
#181221 11:27:30 server id 1  end_log_pos 7847 CRC32 0x368d7214 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
ol0cXBMBAAAARwAAAO0dAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQAORi8CY=
ol0cXB8BAAAAugAAAKceAAAAAGwAAAAAAAEAAgAM/////wDwogAAAAAAAAACAAAAbwAAAAAAAABz
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAACjJzNzmcBAAAWT53OZwEAAIyczc5nAQAAAPCiAAAA
AAAAAAIAAABvAAAAAAAAAHMAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAAGQnM3OZwEAABZPnc5n
AQAAkJzNzmcBAAAUco02
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=2 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545362840716 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545362840716 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545362840720 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545362840720 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 7847
#181221 11:27:30 server id 1  end_log_pos 7918 CRC32 0xa77748fd 	Table_map: `test`.`group_member_0` mapped to number 108
# at 7918
#181221 11:27:30 server id 1  end_log_pos 8104 CRC32 0x3dfa7041 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
ol0cXBMBAAAARwAAAO4eAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQAP1Id6c=
ol0cXB8BAAAAugAAAKgfAAAAAGwAAAAAAAEAAgAM/////wDwpAAAAAAAAAACAAAAbwAAAAAAAAB0
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAABDw+zzmcBAAAZT53OZwEAAA8Ps85nAQAAAPCkAAAA
AAAAAAIAAABvAAAAAAAAAHQAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAAGQnM3OZwEAABlPnc5n
AQAAkJzNzmcBAABBcPo9
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=164 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=116 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545361100559 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545361100559 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=164 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=116 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545362840720 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545362840720 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 8104
#181221 11:28:30 server id 1  end_log_pos 8135 CRC32 0xb239bca4 	Xid = 514
COMMIT/*!*/;
SET @@SESSION.GTID_NEXT= 'AUTOMATIC' /* added by mysqlbinlog */ /*!*/;
DELIMITER ;
# End of log file
/*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE*/;
/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=0*/;
```
可以看到内部只启动了一个事务，Xid=514，内部是按照三条SQL分别执行的。

### 开启事务 SQL2 BINLOG
```sql
# at 8135
#181221 11:32:02 server id 1  end_log_pos 8200 CRC32 0x21ed226f 	Anonymous_GTID	last_committed=19	sequence_number=20	rbr_only=yes
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 8200
#181221 11:31:51 server id 1  end_log_pos 8272 CRC32 0x144c5146 	Query	thread_id=46	exec_time=0	error_code=0
SET TIMESTAMP=1545363111/*!*/;
BEGIN
/*!*/;
# at 8272
#181221 11:31:51 server id 1  end_log_pos 8343 CRC32 0x25b0ec31 	Table_map: `test`.`group_member_0` mapped to number 108
# at 8343
#181221 11:31:51 server id 1  end_log_pos 8529 CRC32 0x4d70c330 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
p14cXBMBAAAARwAAAJcgAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQADHssCU=
p14cXB8BAAAAugAAAFEhAAAAAGwAAAAAAAEAAgAM/////wDwogAAAAAAAAACAAAAbwAAAAAAAABz
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAABkJzNzmcBAAAWT53OZwEAAJCczc5nAQAAAPCiAAAA
AAAAAAIAAABvAAAAAAAAAHMAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAAL1utHOZwEAABZPnc5n
AQAA9brRzmcBAAAww3BN
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545362840720 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545362840720 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=2 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545363110645 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545363110645 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 8529
#181221 11:31:51 server id 1  end_log_pos 8600 CRC32 0x523d4dc2 	Table_map: `test`.`group_member_0` mapped to number 108
# at 8600
#181221 11:31:51 server id 1  end_log_pos 8786 CRC32 0x6abcfe10 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
p14cXBMBAAAARwAAAJghAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQAMJNPVI=
p14cXB8BAAAAugAAAFIiAAAAAGwAAAAAAAEAAgAM/////wDwogAAAAAAAAACAAAAbwAAAAAAAABz
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAAC9brRzmcBAAAWT53OZwEAAPW60c5nAQAAAPCiAAAA
AAAAAAIAAABvAAAAAAAAAHMAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAAH5utHOZwEAABZPnc5n
AQAA+brRzmcBAAAQ/rxq
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=2 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545363110645 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545363110645 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545363110649 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545363110649 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 8786
#181221 11:31:51 server id 1  end_log_pos 8857 CRC32 0xd0f134b7 	Table_map: `test`.`group_member_0` mapped to number 108
# at 8857
#181221 11:31:51 server id 1  end_log_pos 9043 CRC32 0x2a30b6be 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
p14cXBMBAAAARwAAAJkiAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQALc08dA=
p14cXB8BAAAAugAAAFMjAAAAAGwAAAAAAAEAAgAM/////wDwpAAAAAAAAAACAAAAbwAAAAAAAAB0
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAABkJzNzmcBAAAZT53OZwEAAJCczc5nAQAAAPCkAAAA
AAAAAAIAAABvAAAAAAAAAHQAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAAH5utHOZwEAABlPnc5n
AQAA+brRzmcBAAC+tjAq
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=164 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=116 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545362840720 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545362840720 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=164 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=116 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545363110649 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545363110649 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 9043
#181221 11:32:02 server id 1  end_log_pos 9074 CRC32 0x76f6b86f 	Xid = 532
COMMIT/*!*/;
SET @@SESSION.GTID_NEXT= 'AUTOMATIC' /* added by mysqlbinlog */ /*!*/;
DELIMITER ;
# End of log file
/*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE*/;
/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=0*/;
```
这里也是一样，执行了一次事务，内部分三个UPDATE执行。

### 开启事务SQL1 general_log
```sql
2018-12-21T03:27:21.130249Z        45 Connect   root@localhost on test using TCP/IP
2018-12-21T03:27:21.137721Z        45 Query     /* mysql-connector-java-5.1.43 ( Revision: 1d14b699eff3e6112aaedb1cbe5a151ab81f98f1 ) */SELECT  @@session.auto_increment_increment AS auto_increment_increment, @@character_set_client AS character_set_client, @@character_set_connection AS character_set_connection, @@character_set_results AS character_set_results, @@character_set_server AS character_set_server, @@collation_server AS collation_server, @@init_connect AS init_connect, @@interactive_timeout AS interactive_timeout, @@license AS license, @@lower_case_table_names AS lower_case_table_names, @@max_allowed_packet AS max_allowed_packet, @@net_buffer_length AS net_buffer_length, @@net_write_timeout AS net_write_timeout, @@have_query_cache AS have_query_cache, @@sql_mode AS sql_mode, @@system_time_zone AS system_time_zone, @@time_zone AS time_zone, @@tx_isolation AS tx_isolation, @@wait_timeout AS wait_timeout
2018-12-21T03:27:21.171067Z        45 Query     SHOW WARNINGS
2018-12-21T03:27:21.173168Z        45 Query     SELECT @@query_cache_size AS query_cache_size, @@query_cache_type AS query_cache_type
2018-12-21T03:27:21.173485Z        45 Query     SHOW WARNINGS
2018-12-21T03:27:21.174526Z        45 Query     SET character_set_results = NULL
2018-12-21T03:27:21.174896Z        45 Query     SELECT @@session.autocommit
2018-12-21T03:27:21.181111Z        45 Query     SET autocommit=0
2018-12-21T03:27:30.096848Z        45 Query     select @@session.tx_read_only
2018-12-21T03:27:30.097894Z        45 Query     INSERT INTO group_member_0(app_id, group_id, user_id, status, member_role, inviter_id, group_member_setting, nickname, create_time, update_time, last_join_time) VALUES(2, 111, 115, 1, 2, 115, 0, '', 1545362840716, 1545362840716, 1545362840716) ON DUPLICATE KEY UPDATE status = VALUES(status), member_role = VALUES(member_role), inviter_id = VALUES(inviter_id), group_member_setting = VALUES(group_member_setting), nickname = VALUES(nickname), update_time = VALUES(update_time), last_join_time = VALUES(last_join_time)
2018-12-21T03:27:30.111663Z        45 Query     INSERT INTO group_member_0(app_id, group_id, user_id, status, member_role, inviter_id, group_member_setting, nickname, create_time, update_time, last_join_time) VALUES(2, 111, 115, 1, 1, 115, 0, '', 1545362840720, 1545362840720, 1545362840720) ON DUPLICATE KEY UPDATE status = VALUES(status), member_role = VALUES(member_role), inviter_id = VALUES(inviter_id), group_member_setting = VALUES(group_member_setting), nickname = VALUES(nickname), update_time = VALUES(update_time), last_join_time = VALUES(last_join_time)
2018-12-21T03:27:30.112103Z        45 Query     INSERT INTO group_member_0(app_id, group_id, user_id, status, member_role, inviter_id, group_member_setting, nickname, create_time, update_time, last_join_time) VALUES(2, 111, 116, 1, 1, 115, 0, '', 1545362840720, 1545362840720, 1545362840720) ON DUPLICATE KEY UPDATE status = VALUES(status), member_role = VALUES(member_role), inviter_id = VALUES(inviter_id), group_member_setting = VALUES(group_member_setting), nickname = VALUES(nickname), update_time = VALUES(update_time), last_join_time = VALUES(last_join_time)
2018-12-21T03:27:53.367744Z         2 Query     select * from group_member_0
2018-12-21T03:27:54.839814Z         2 Query     select * from group_member_0
2018-12-21T03:28:30.304723Z        45 Query     commit
2018-12-21T03:28:30.324870Z        45 Query     SET autocommit=1
2018-12-21T03:28:30.333496Z        45 Query     select @@session.tx_read_only
2018-12-21T03:28:30.341584Z        45 Quit
```
可以看到内部先 **SET autocommit=0**，即关闭了自动提交，一直到全部SQL执行完毕才打开**SET autocommit=1**。

### 开启事务SQL2 general_log
```sql
2018-12-21T03:31:51.067874Z        46 Connect   root@localhost on test using TCP/IP
2018-12-21T03:31:51.073603Z        46 Query     /* mysql-connector-java-5.1.43 ( Revision: 1d14b699eff3e6112aaedb1cbe5a151ab81f98f1 ) */SELECT  @@session.auto_increment_increment AS auto_increment_increment, @@character_set_client AS character_set_client, @@character_set_connection AS character_set_connection, @@character_set_results AS character_set_results, @@character_set_server AS character_set_server, @@collation_server AS collation_server, @@init_connect AS init_connect, @@interactive_timeout AS interactive_timeout, @@license AS license, @@lower_case_table_names AS lower_case_table_names, @@max_allowed_packet AS max_allowed_packet, @@net_buffer_length AS net_buffer_length, @@net_write_timeout AS net_write_timeout, @@have_query_cache AS have_query_cache, @@sql_mode AS sql_mode, @@system_time_zone AS system_time_zone, @@time_zone AS time_zone, @@tx_isolation AS tx_isolation, @@wait_timeout AS wait_timeout
2018-12-21T03:31:51.107874Z        46 Query     SHOW WARNINGS
2018-12-21T03:31:51.110058Z        46 Query     SELECT @@query_cache_size AS query_cache_size, @@query_cache_type AS query_cache_type
2018-12-21T03:31:51.110341Z        46 Query     SHOW WARNINGS
2018-12-21T03:31:51.111389Z        46 Query     SET character_set_results = NULL
2018-12-21T03:31:51.111728Z        46 Query     SELECT @@session.autocommit
2018-12-21T03:31:51.117511Z        46 Query     SET autocommit=0
2018-12-21T03:31:51.148299Z        46 Query     select @@session.tx_read_only
2018-12-21T03:31:51.149302Z        46 Query     INSERT INTO group_member_0(`app_id`,`group_id`,`user_id`,`status`,`member_role`,`inviter_id`,`group_member_setting`,`nickname`, `create_time`,`update_time`,`last_join_time`) VALUES(2, 111,115,1,2,115,0,'', 1545363110645,1545363110645,1545363110645)  ON DUPLICATE KEY UPDATE `status`=1,`member_role` =2, `inviter_id`=115,`group_member_setting`=0,`nickname`='', `update_time`=1545363110645,`last_join_time`=1545363110645
2018-12-21T03:31:51.151461Z        46 Query     INSERT INTO group_member_0(`app_id`,`group_id`,`user_id`,`status`,`member_role`,`inviter_id`,`group_member_setting`,`nickname`, `create_time`,`update_time`,`last_join_time`) VALUES(2, 111,115,1,1,115,0,'', 1545363110649,1545363110649,1545363110649)  ON DUPLICATE KEY UPDATE `status`=1,`member_role` =1, `inviter_id`=115,`group_member_setting`=0,`nickname`='', `update_time`=1545363110649,`last_join_time`=1545363110649
2018-12-21T03:31:51.151862Z        46 Query     INSERT INTO group_member_0(`app_id`,`group_id`,`user_id`,`status`,`member_role`,`inviter_id`,`group_member_setting`,`nickname`, `create_time`,`update_time`,`last_join_time`) VALUES(2, 111,116,1,1,115,0,'', 1545363110649,1545363110649,1545363110649)  ON DUPLICATE KEY UPDATE `status`=1,`member_role` =1, `inviter_id`=115,`group_member_setting`=0,`nickname`='', `update_time`=1545363110649,`last_join_time`=1545363110649
2018-12-21T03:31:56.950142Z         2 Query     select * from group_member_0
2018-12-21T03:32:02.775309Z        46 Query     commit
2018-12-21T03:32:02.791604Z        46 Query     SET autocommit=1
2018-12-21T03:32:02.793580Z        46 Query     select @@session.tx_read_only
2018-12-21T03:32:02.799811Z        46 Quit
```
可以看到内部先 **SET autocommit=0**，即关闭了自动提交，一直到全部SQL执行完毕才打开**SET autocommit=1**。

### 总结
通过在事务中执行批量提交可以保证原子性，但是内部仍然是通过多个SQL执行的。

## 异常的批量提交
如果在一个批量提交中有部分SQL是有语法错误或者数值不符合规范的，如int类型的field却赋值了varchar，则这两种SQL的执行却是截然不同的。

### SQL1 BIN LOG
```sql
#181221 11:51:54 server id 1  end_log_pos 9989 CRC32 0xb746c10b 	Anonymous_GTID	last_committed=22	sequence_number=23	rbr_only=yes
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 9989
#181221 11:51:54 server id 1  end_log_pos 10061 CRC32 0x4fa74988 	Query	thread_id=49	exec_time=0	error_code=0
SET TIMESTAMP=1545364314/*!*/;
BEGIN
/*!*/;
# at 10061
#181221 11:51:54 server id 1  end_log_pos 10132 CRC32 0xe9bb3b1d 	Table_map: `test`.`group_member_0` mapped to number 108
# at 10132
#181221 11:51:54 server id 1  end_log_pos 10318 CRC32 0x4d4135bd 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
WmMcXBMBAAAARwAAAJQnAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQAB07u+k=
WmMcXB8BAAAAugAAAE4oAAAAAGwAAAAAAAEAAgAM/////wDwogAAAAAAAAACAAAAbwAAAAAAAABz
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAAC1nLhzmcBAAAWT53OZwEAANZy4c5nAQAAAPCiAAAA
AAAAAAIAAABvAAAAAAAAAHMAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAALXFeTOZwEAABZPnc5n
AQAA1xXkzmcBAAC9NUFN
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=2 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545364140758 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545364140758 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=2 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545364313559 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545364313559 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 10318
#181221 11:51:54 server id 1  end_log_pos 10349 CRC32 0xf019752d 	Xid = 568
COMMIT/*!*/;
# at 10349
#181221 11:51:54 server id 1  end_log_pos 10414 CRC32 0x8aebf235 	Anonymous_GTID	last_committed=23	sequence_number=24	rbr_only=yes
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 10414
#181221 11:51:54 server id 1  end_log_pos 10486 CRC32 0x3db08b55 	Query	thread_id=49	exec_time=0	error_code=0
SET TIMESTAMP=1545364314/*!*/;
BEGIN
/*!*/;
# at 10486
#181221 11:51:54 server id 1  end_log_pos 10557 CRC32 0x9ed71b96 	Table_map: `test`.`group_member_0` mapped to number 108
# at 10557
#181221 11:51:54 server id 1  end_log_pos 10743 CRC32 0xc93e4f46 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
WmMcXBMBAAAARwAAAD0pAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQAJYb154=
WmMcXB8BAAAAugAAAPcpAAAAAGwAAAAAAAEAAgAM/////wDwpAAAAAAAAAACAAAAbwAAAAAAAAB0
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAAB3HLhzmcBAAAZT53OZwEAANxy4c5nAQAAAPCkAAAA
AAAAAAIAAABvAAAAAAAAAHQAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAAHdFeTOZwEAABlPnc5n
AQAA3RXkzmcBAABGTz7J
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=164 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=116 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545364140764 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545364140764 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=164 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=116 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545364313565 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545364313565 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 10743
#181221 11:51:54 server id 1  end_log_pos 10774 CRC32 0x77374fb3 	Xid = 570
COMMIT/*!*/;
SET @@SESSION.GTID_NEXT= 'AUTOMATIC' /* added by mysqlbinlog */ /*!*/;
DELIMITER ;
# End of log file
/*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE*/;
/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=0*/;
```
该语句并非一个完整的事务，即会有部分更新成功。
### SQL1 general_log
```sql
2018-12-21T03:51:54.072184Z        49 Connect   root@localhost on test using TCP/IP
2018-12-21T03:51:54.080503Z        49 Query     /* mysql-connector-java-5.1.43 ( Revision: 1d14b699ef
f3e6112aaedb1cbe5a151ab81f98f1 ) */SELECT  @@session.auto_increment_increment AS auto_increment_incre
ment, @@character_set_client AS character_set_client, @@character_set_connection AS character_set_con
nection, @@character_set_results AS character_set_results, @@character_set_server AS character_set_se
rver, @@collation_server AS collation_server, @@init_connect AS init_connect, @@interactive_timeout A
S interactive_timeout, @@license AS license, @@lower_case_table_names AS lower_case_table_names, @@ma
x_allowed_packet AS max_allowed_packet, @@net_buffer_length AS net_buffer_length, @@net_write_timeout AS net_write_timeout, @@have_query_cache AS have_query_cache, @@sql_mode AS sql_mode, @@system_time_zone AS system_time_zone, @@time_zone AS time_zone, @@tx_isolation AS tx_isolation, @@wait_timeout AS wait_timeout
2018-12-21T03:51:54.160392Z        49 Query     SHOW WARNINGS
2018-12-21T03:51:54.163165Z        49 Query     SELECT @@query_cache_size AS query_cache_size, @@query_cache_type AS query_cache_type
2018-12-21T03:51:54.163470Z        49 Query     SHOW WARNINGS
2018-12-21T03:51:54.164777Z        49 Query     SET character_set_results = NULL
2018-12-21T03:51:54.165158Z        49 Query     SELECT @@session.autocommit
2018-12-21T03:51:54.189926Z        49 Query     select @@session.tx_read_only
2018-12-21T03:51:54.190448Z        49 Query     INSERT INTO group_member_0(app_id, group_id, user_id, status, member_role, inviter_id, group_member_setting, nickname, create_time, update_time, last_join_time) VALUES(2, 111, 115, 1, 2, 115, 0, '', 1545364313559, 1545364313559, 1545364313559) ON DUPLICATE KEY UPDATE status = VALUES(status), member_role = VALUES(member_role), inviter_id = VALUES(inviter_id), group_member_setting = VALUES(group_member_setting), nickname = VALUES(nickname), update_time = VALUES(update_time), last_join_time = VALUES(last_join_time)
2018-12-21T03:51:54.219802Z        49 Query     INSERT INTO group_member_0(app_id, group_id, user_id, status, member_role, inviter_id, group_member_setting, nickname, create_time, update_time, last_join_time) VALUES(2, 111, 115, 'a', 1, 115, 0, '', 1545364313565, 1545364313565, 1545364313565) ON DUPLICATE KEY UPDATE status = VALUES(status), member_role = VALUES(member_role), inviter_id = VALUES(inviter_id), group_member_setting = VALUES(group_member_setting), nickname = VALUES(nickname), update_time = VALUES(update_time), last_join_time = VALUES(last_join_time)
2018-12-21T03:51:54.223840Z        49 Query     INSERT INTO group_member_0(app_id, group_id, user_id, status, member_role, inviter_id, group_member_setting, nickname, create_time, update_time, last_join_time) VALUES(2, 111, 116, 1, 1, 115, 0, '', 1545364313565, 1545364313565, 1545364313565) ON DUPLICATE KEY UPDATE status = VALUES(status), member_role = VALUES(member_role), inviter_id = VALUES(inviter_id), group_member_setting = VALUES(group_member_setting), nickname = VALUES(nickname), update_time = VALUES(update_time), last_join_time = VALUES(last_join_time)
2018-12-21T03:51:54.235727Z        49 Quit
2018-12-21T03:51:54.549703Z        50 Connect   root@localhost on test using TCP/IP
2018-12-21T03:51:54.550165Z        50 Query     /* mysql-connector-java-5.1.43 ( Revision: 1d14b699eff3e6112aaedb1cbe5a151ab81f98f1 ) */SELECT  @@session.auto_increment_increment AS auto_increment_increment, @@character_set_client AS character_set_client, @@character_set_connection AS character_set_connection, @@character_set_results AS character_set_results, @@character_set_server AS character_set_server, @@collation_server AS collation_server, @@init_connect AS init_connect, @@interactive_timeout AS interactive_timeout, @@license AS license, @@lower_case_table_names AS lower_case_table_names, @@max_allowed_packet AS max_allowed_packet, @@net_buffer_length AS net_buffer_length, @@net_write_timeout AS net_write_timeout, @@have_query_cache AS have_query_cache, @@sql_mode AS sql_mode, @@system_time_zone AS system_time_zone, @@time_zone AS time_zone, @@tx_isolation AS tx_isolation, @@wait_timeout AS wait_timeout
2018-12-21T03:51:54.550622Z        50 Query     SHOW WARNINGS
2018-12-21T03:51:54.551145Z        50 Query     SELECT @@query_cache_size AS query_cache_size, @@query_cache_type AS query_cache_type
2018-12-21T03:51:54.551450Z        50 Query     SHOW WARNINGS
2018-12-21T03:51:54.551801Z        50 Query     SET character_set_results = NULL
2018-12-21T03:51:54.552470Z        50 Query     SELECT @@session.autocommit
2018-12-21T03:51:54.554391Z        50 Quit
```

### SQL2 BIN LOG
```sql
#181221 11:49:01 server id 1  end_log_pos 9139 CRC32 0xa772b006 	Anonymous_GTID	last_committed=20	sequence_number=21	rbr_only=yes
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 9139
#181221 11:49:01 server id 1  end_log_pos 9211 CRC32 0x03cc8206 	Query	thread_id=47	exec_time=0	error_code=0
SET TIMESTAMP=1545364141/*!*/;
BEGIN
/*!*/;
# at 9211
#181221 11:49:01 server id 1  end_log_pos 9282 CRC32 0xc3636cd1 	Table_map: `test`.`group_member_0` mapped to number 108
# at 9282
#181221 11:49:01 server id 1  end_log_pos 9468 CRC32 0x4d419909 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
rWIcXBMBAAAARwAAAEIkAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQANFsY8M=
rWIcXB8BAAAAugAAAPwkAAAAAGwAAAAAAAEAAgAM/////wDwogAAAAAAAAACAAAAbwAAAAAAAABz
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAAB+brRzmcBAAAWT53OZwEAAPm60c5nAQAAAPCiAAAA
AAAAAAIAAABvAAAAAAAAAHMAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAALWcuHOZwEAABZPnc5n
AQAA1nLhzmcBAAAJmUFN
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545363110649 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545363110649 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=2 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545364140758 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545364140758 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 9468
#181221 11:49:01 server id 1  end_log_pos 9499 CRC32 0xa9e62fca 	Xid = 549
COMMIT/*!*/;
# at 9499
#181221 11:49:01 server id 1  end_log_pos 9564 CRC32 0xc3667a81 	Anonymous_GTID	last_committed=21	sequence_number=22	rbr_only=yes
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 9564
#181221 11:49:01 server id 1  end_log_pos 9636 CRC32 0x830e228d 	Query	thread_id=47	exec_time=0	error_code=0
SET TIMESTAMP=1545364141/*!*/;
BEGIN
/*!*/;
# at 9636
#181221 11:49:01 server id 1  end_log_pos 9707 CRC32 0x5752d556 	Table_map: `test`.`group_member_0` mapped to number 108
# at 9707
#181221 11:49:01 server id 1  end_log_pos 9893 CRC32 0xb5c8c739 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
rWIcXBMBAAAARwAAAOslAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQAFbVUlc=
rWIcXB8BAAAAugAAAKUmAAAAAGwAAAAAAAEAAgAM/////wDwpAAAAAAAAAACAAAAbwAAAAAAAAB0
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAAB+brRzmcBAAAZT53OZwEAAPm60c5nAQAAAPCkAAAA
AAAAAAIAAABvAAAAAAAAAHQAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAAHccuHOZwEAABlPnc5n
AQAA3HLhzmcBAAA5x8i1
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=164 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=116 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545363110649 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545363110649 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=164 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=116 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545364140764 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545364140764 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 9893
#181221 11:49:01 server id 1  end_log_pos 9924 CRC32 0xa4e5d4f0 	Xid = 551
COMMIT/*!*/;
```
该语句可以保证一旦中间有一个错误的SQL，将会回滚所有已经提交的执行结果，即该执行是原子的。

### SQL2 general_log 
```sql
2018-12-21T03:49:01.291402Z        47 Connect   root@localhost on test using TCP/IP
2018-12-21T03:49:01.298845Z        47 Query     /* mysql-connector-java-5.1.43 ( Revision: 1d14b699ef
f3e6112aaedb1cbe5a151ab81f98f1 ) */SELECT  @@session.auto_increment_increment AS auto_increment_incre
ment, @@character_set_client AS character_set_client, @@character_set_connection AS character_set_con
nection, @@character_set_results AS character_set_results, @@character_set_server AS character_set_server, @@collation_server AS collation_server, @@init_connect AS init_connect, @@interactive_timeout AS interactive_timeout, @@license AS license, @@lower_case_table_names AS lower_case_table_names, @@max_allowed_packet AS max_allowed_packet, @@net_buffer_length AS net_buffer_length, @@net_write_timeout AS net_write_timeout, @@have_query_cache AS have_query_cache, @@sql_mode AS sql_mode, @@system_time_zone AS system_time_zone, @@time_zone AS time_zone, @@tx_isolation AS tx_isolation, @@wait_timeout AS wait_timeout
2018-12-21T03:49:01.389097Z        47 Query     SHOW WARNINGS
2018-12-21T03:49:01.392389Z        47 Query     SELECT @@query_cache_size AS query_cache_size, @@query_cache_type AS query_cache_type
2018-12-21T03:49:01.398313Z        47 Query     SHOW WARNINGS
2018-12-21T03:49:01.399602Z        47 Query     SET character_set_results = NULL
2018-12-21T03:49:01.399975Z        47 Query     SELECT @@session.autocommit
2018-12-21T03:49:01.428655Z        47 Query     select @@session.tx_read_only
2018-12-21T03:49:01.429274Z        47 Query     INSERT INTO group_member_0(`app_id`,`group_id`,`user_id`,`status`,`member_role`,`inviter_id`,`group_member_setting`,`nickname`, `create_time`,`update_time`,`last_join_time`) VALUES(2, 111,115,1,2,115,0,'', 1545364140758,1545364140758,1545364140758)  ON DUPLICATE KEY UPDATE `status`=1,`member_role` =2, `inviter_id`=115,`group_member_setting`=0,`nickname`='', `update_time`=1545364140758,`last_join_time`=1545364140758
2018-12-21T03:49:01.477710Z        47 Query     INSERT INTO group_member_0(`app_id`,`group_id`,`user_id`,`status`,`member_role`,`inviter_id`,`group_member_setting`,`nickname`, `create_time`,`update_time`,`last_join_time`) VALUES(2, 111,115,'a',1,115,0,'', 1545364140764,1545364140764,1545364140764)  ON DUPLICATE KEY UPDATE `status`='a',`member_role` =1, `inviter_id`=115,`group_member_setting`=0,`nickname`='', `update_time`=1545364140764,`last_join_time`=1545364140764
2018-12-21T03:49:01.481333Z        47 Query     INSERT INTO group_member_0(`app_id`,`group_id`,`user_id`,`status`,`member_role`,`inviter_id`,`group_member_setting`,`nickname`, `create_time`,`update_time`,`last_join_time`) VALUES(2, 111,116,1,1,115,0,'', 1545364140764,1545364140764,1545364140764)  ON DUPLICATE KEY UPDATE `status`=1,`member_role` =1, `inviter_id`=115,`group_member_setting`=0,`nickname`='', `update_time`=1545364140764,`last_join_time`=1545364140764
2018-12-21T03:49:01.492665Z        47 Quit
2018-12-21T03:49:01.794483Z        48 Connect   root@localhost on test using TCP/IP
2018-12-21T03:49:01.795094Z        48 Query     /* mysql-connector-java-5.1.43 ( Revision: 1d14b699eff3e6112aaedb1cbe5a151ab81f98f1 ) */SELECT  @@session.auto_increment_increment AS auto_increment_increment, @@character_set_client AS character_set_client, @@character_set_connection AS character_set_connection, @@character_set_results AS character_set_results, @@character_set_server AS character_set_server, @@collation_server AS collation_server, @@init_connect AS init_connect, @@interactive_timeout AS interactive_timeout, @@license AS license, @@lower_case_table_names AS lower_case_table_names, @@max_allowed_packet AS max_allowed_packet, @@net_buffer_length AS net_buffer_length, @@net_write_timeout AS net_write_timeout, @@have_query_cache AS have_query_cache, @@sql_mode AS sql_mode, @@system_time_zone AS system_time_zone, @@time_zone AS time_zone, @@tx_isolation AS tx_isolation, @@wait_timeout AS wait_timeout
2018-12-21T03:49:01.795769Z        48 Query     SHOW WARNINGS
2018-12-21T03:49:01.796414Z        48 Query     SELECT @@query_cache_size AS query_cache_size, @@query_cache_type AS query_cache_type
2018-12-21T03:49:01.796713Z        48 Query     SHOW WARNINGS
2018-12-21T03:49:01.797187Z        48 Query     SET character_set_results = NULL
2018-12-21T03:49:01.797559Z        48 Query     SELECT @@session.autocommit
2018-12-21T03:49:01.798166Z        48 Quit
```
## 原子插入
```sql
mysql> INSERT INTO group_member_0(app_id, group_id, user_id, status, member_role, inviter_id, group_member_setting, nickname, create_time, update_time, last_join_time) VALUES(2, 111, 115, 1, 1, 101, 0, '', 1545189948076, 1545189948076, 1545189948076), (2, 111, 115, 1, 1, 101, 0, '', 1545189948078, 1545189948076, 1545189948078), (2, 111, 116, 1, 1, 101, 0, '', 1545189948079, 1545189948079, 1545189948079) ON DUPLICATE KEY UPDATE status = VALUES(status), member_role = VALUES(member_role), inviter_id = VALUES(inviter_id), group_member_setting = VALUES(group_member_setting), nickname = VALUES(nickname), update_time = VALUES(update_time), last_join_time = VALUES(last_join_time);
```
### BINLOG
```sql
#181221 11:59:33 server id 1  end_log_pos 12539 CRC32 0x0ea661dd 	Anonymous_GTID	last_committed=28	sequence_number=29	rbr_only=yes
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 12539
#181221 11:59:33 server id 1  end_log_pos 12611 CRC32 0x5e5088d8 	Query	thread_id=2	exec_time=0	error_code=0
SET TIMESTAMP=1545364773/*!*/;
BEGIN
/*!*/;
# at 12611
#181221 11:59:33 server id 1  end_log_pos 12682 CRC32 0xf5fcda04 	Table_map: `test`.`group_member_0` mapped to number 108
# at 12682
#181221 11:59:33 server id 1  end_log_pos 13164 CRC32 0x9ca09cf3 	Update_rows: table id 108 flags: STMT_END_F

BINLOG '
JWUcXBMBAAAARwAAAIoxAAAAAGwAAAAAAAEABHRlc3QADmdyb3VwX21lbWJlcl8wAAwIAwgIDwgB
CAEICAgCAAQQAATa/PU=
JWUcXB8BAAAA4gEAAGwzAAAAAGwAAAAAAAEAAgAM/////wDwogAAAAAAAAACAAAAbwAAAAAAAABz
AAAAAAAAAAAAAAAAAAAAAAABcwAAAAAAAAABXyzpzmcBAAAWT53OZwEAAF8s6c5nAQAAAPCiAAAA
AAAAAAIAAABvAAAAAAAAAHMAAAAAAAAAAAAAAAAAAAAAAAFlAAAAAAAAAAGsen/EZwEAABZPnc5n
AQAArHp/xGcBAAAA8KIAAAAAAAAAAgAAAG8AAAAAAAAAcwAAAAAAAAAAAAAAAAAAAAAAAWUAAAAA
AAAAAax6f8RnAQAAFk+dzmcBAACsen/EZwEAAADwogAAAAAAAAACAAAAbwAAAAAAAABzAAAAAAAA
AAAAAAAAAAAAAAABZQAAAAAAAAABrnp/xGcBAAAWT53OZwEAAKx6f8RnAQAAAPCkAAAAAAAAAAIA
AABvAAAAAAAAAHQAAAAAAAAAAAAAAAAAAAAAAAFzAAAAAAAAAAHCg+jOZwEAABlPnc5nAQAAwoPo
zmcBAAAA8KQAAAAAAAAAAgAAAG8AAAAAAAAAdAAAAAAAAAAAAAAAAAAAAAAAAWUAAAAAAAAAAa96
f8RnAQAAGU+dzmcBAACven/EZwEAAPOcoJw=
'/*!*/;
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545364647007 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545364647007 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=101 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545189948076 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545189948076 /* LONGINT meta=0 nullable=0 is_null=0 */
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=101 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545189948076 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545189948076 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=162 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=101 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545189948078 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675158 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545189948076 /* LONGINT meta=0 nullable=0 is_null=0 */
### UPDATE `test`.`group_member_0`
### WHERE
###   @1=164 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=116 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=115 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545364603842 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545364603842 /* LONGINT meta=0 nullable=0 is_null=0 */
### SET
###   @1=164 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2=2 /* INT meta=0 nullable=0 is_null=0 */
###   @3=111 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @4=116 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @5='' /* VARSTRING(1024) meta=1024 nullable=1 is_null=0 */
###   @6=0 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @7=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @8=101 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @9=1 /* TINYINT meta=0 nullable=0 is_null=0 */
###   @10=1545189948079 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @11=1545359675161 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @12=1545189948079 /* LONGINT meta=0 nullable=0 is_null=0 */
# at 13164
#181221 11:59:33 server id 1  end_log_pos 13195 CRC32 0xea60a142 	Xid = 620
COMMIT/*!*/;
SET @@SESSION.GTID_NEXT= 'AUTOMATIC' /* added by mysqlbinlog */ /*!*/;
DELIMITER ;
# End of log file
/*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE*/;
/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=0*/;
```
### general_log
```sql
2018-12-21T03:57:27.994727Z        54 Connect   root@localhost on test using TCP/IP
2018-12-21T03:57:27.995177Z        54 Query     /* mysql-connector-java-5.1.43 ( Revision: 1d14b699eff3e6112aaedb1cbe5a151ab81f98f1 ) */SELECT  @@session.auto_increment_increment AS auto_increment_increment, @@character_set_client AS character_set_client, @@character_set_connection AS character_set_connection, @@character_set_results AS character_set_results, @@character_set_server AS character_set_server, @@collation_server AS collation_server, @@init_connect AS init_connect, @@interactive_timeout AS interactive_timeout, @@license AS license, @@lower_case_table_names AS lower_case_table_names, @@max_allowed_packet AS max_allowed_packet, @@net_buffer_length AS net_buffer_length, @@net_write_timeout AS net_write_timeout, @@have_query_cache AS have_query_cache, @@sql_mode AS sql_mode, @@system_time_zone AS system_time_zone, @@time_zone AS time_zone, @@tx_isolation AS tx_isolation, @@wait_timeout AS wait_timeout
2018-12-21T03:57:27.995774Z        54 Query     SHOW WARNINGS
2018-12-21T03:57:27.996547Z        54 Query     SELECT @@query_cache_size AS query_cache_size, @@query_cache_type AS query_cache_type
2018-12-21T03:57:27.996876Z        54 Query     SHOW WARNINGS
2018-12-21T03:57:27.997381Z        54 Query     SET character_set_results = NULL
2018-12-21T03:57:27.997711Z        54 Query     SELECT @@session.autocommit
2018-12-21T03:57:27.999450Z        54 Quit
2018-12-21T03:57:32.374133Z         2 Query     select * from group_member_0
2018-12-21T03:59:33.365923Z         2 Query     INSERT INTO group_member_0(app_id, group_id, user_id, status, member_role, inviter_id, group_member_setting, nickname, create_time, update_time, last_join_time) VALUES(2, 111, 115, 1, 1, 101, 0, '', 1545189948076, 1545189948076, 1545189948076), (2, 111, 115, 1, 1, 101, 0, '', 1545189948078, 1545189948076, 1545189948078), (2, 111, 116, 1, 1, 101, 0, '', 1545189948079, 1545189948079, 1545189948079) ON DUPLICATE KEY UPDATE status = VALUES(status), member_role = VALUES(member_role), inviter_id = VALUES(inviter_id), group_member_setting = VALUES(group_member_setting), nickname = VALUES(nickname), update_time = VALUES(update_time), last_join_time = VALUES(last_join_time)
```

> 本文首次发布于 [ElseF's Blog](http://elsef.com), 作者 [@stuartlau](http://github.com/stuartlau) ,
转载请保留原文链接.
