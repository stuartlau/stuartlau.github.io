# 社交关系系统设计详解

>本文档基于现有业务场景，深入分析了社交关系系统的核心架构选择、数据库设计规范、业务逻辑处理流程以及高并发场景下的性能优化策略。

## 1. 核心架构选型：数据存储模式

在社交关系系统的设计中，最核心的决策在于底层数据的存储模式。主流方案主要有两种：**双向存储（2-rows）** 与 **单向存储（Single-row）**。

### 1.1 方案对比

| 方案 | 描述 | 优点 | 缺点 |
| :--- | :--- | :--- | :--- |
| **Double-Rows (双向存储)** | A 关注 B，数据库中同时存储 `(A, B)` 和 `(B, A)` 两条记录。 | **查询极其高效**：无需复杂的索引或联合查询，直接查 A 的记录即可得 A 的关注列表，查 B 的记录即可得 B 的粉丝列表。<br>**逻辑简单**：符合直觉，易于维护。 | **数据冗余**：存储空间占用翻倍。<br>**一致性挑战**：写入时需要保证两个维度的事务一致性（通常通过事务或分布式事务解决）。 |
| **Single-Row (单向存储)** | A 关注 B，仅存储一条 `(A, B)` 记录，通过状态位区分关系。 | **存储节省**：无冗余数据。<br>**写入快**：仅需写一次。 | **反向查询困难**：查询“谁关注了我”（粉丝列表）时，需要对 `target_id` 建立高效索引，数据量大时分库分表策略变得复杂。<br>**扩展性差**：难以表达复杂的非对称关系。 |

### 1.2 选型结论
考虑到社交场景中“我的关注”和“我的粉丝”均为最高频的查询操作，且为了逻辑层（Logic）处理的统一性（类似于 IM 的会话模型），本系统最终采用 **2-rows（双向存储）** 方案。这意味着用户的每一次关系变更，底层数据库都会对应两条记录的变动，以空间换取查询效率和逻辑的清晰性。

---

## 2. 核心查询场景支持

系统设计需优先满足以下高频业务查询：

1.  **增量同步 (Incremental Sync)**
    *   **场景**：客户端冷启动或断线重连。
    *   **实现**：基于 `update_time` 时间戳，拉取 `last_sync_time` 之后的所有变动（新增关注/取消关注）。
2.  **列表分页查询 (Pagination)**
    *   **场景**：查看好友列表、粉丝列表。
    *   **实现**：标准的分页获取，支持按时间倒序。
3.  **水位线同步 (Watermark)**
    *   **场景**：判断客户端数据是否陈旧。
    *   **实现**：轻量级接口，仅返回当前用户关系列表的最后 `update_time`。

---

## 3. 数据库架构设计

本方案采用 MySQL 作为持久化存储（配合 Redis 缓存），核心表结构设计如下：

### 3.1 别名表 (`alias_setting`)
用于存储用户对他人的备注信息。

```sql
CREATE TABLE `alias_setting_104_0` (
  `id`          BIGINT(20) UNSIGNED AUTO_INCREMENT COMMENT '主键ID',
  `kpn`         VARCHAR(64) NOT NULL COMMENT '产品线标识(Key Product Name)',
  `user_id`     BIGINT(20) NOT NULL COMMENT '当前用户ID',
  `target_id`   BIGINT(20) NOT NULL COMMENT '目标用户ID',
  `alias_name`  VARCHAR(32) COMMENT '备注名称',
  `create_time` BIGINT      NOT NULL COMMENT '创建时间戳(ms)',
  `update_time` BIGINT      NOT NULL COMMENT '更新时间戳(ms)',
  PRIMARY KEY (`id`),
  UNIQUE KEY uniq_alias_key(`user_id`, `target_id`),
  KEY idx_alias_update(`user_id`, `update_time`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT='用户备注表';
```

### 3.2 验证设置表 (`verify_setting`)
用于控制被添加时的验证策略（如：允许任何人添加、需要验证消息、禁止添加等）。

```sql
CREATE TABLE `verify_setting_104_0` (
  `id`            BIGINT(20) UNSIGNED AUTO_INCREMENT COMMENT '主键ID',
  `kpn`           VARCHAR(64) NOT NULL,
  `user_id`       BIGINT(20) NOT NULL COMMENT '用户ID',
  `verify_type`   TINYINT NOT NULL COMMENT '验证方式: 0-无须验证, 1-需审批, 2-拒绝所有',
  `relation_type` TINYINT NOT NULL COMMENT '针对的关系类型',
  `sub_biz_id`    INT(11) NOT NULL DEFAULT 0 COMMENT '子业务ID区分',
  `create_time`   BIGINT(20) NOT NULL,
  `update_time`   BIGINT(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY uniq_verify_key(`user_id`, `relation_type`, `sub_biz_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT='好友验证设置表';
```

### 3.3 关系申请表 (`relation_request`)
处理好友申请的中间状态。由于采用 2-rows 思想，申请也是有方向的。
*   **A -> B**：A 的表中记录“我发出了申请”，B 的表中记录“我收到了申请”。

```sql
CREATE TABLE `relation_request_104_0` (
  `id`             BIGINT(20) UNSIGNED AUTO_INCREMENT,
  `user_id`        BIGINT(20) NOT NULL,
  `target_id`      BIGINT(20) NOT NULL,
  `status`         TINYINT    NOT NULL COMMENT '状态: 1-已发送, 2-待处理, 3-已接受, 4-已拒绝',
  `find_way`       INT(11)    NOT NULL COMMENT '来源渠道: 搜索/群组/二维码',
  `relation_type`  TINYINT    NOT NULL,
  `deleted`        BOOLEAN    NOT NULL DEFAULT FALSE COMMENT '软删除',
  `create_time`    BIGINT(20) NOT NULL,
  `update_time`    BIGINT(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY uniq_request_key(`user_id`, `target_id`, `relation_type`),
  KEY idx_user_update(`user_id`, `update_time`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT='关系申请记录表';
```

### 3.4 关系主表 (`relation`)
存储最终确立的社交关系。

```sql
CREATE TABLE `relation_104_0` (
  `id`            BIGINT(20) UNSIGNED AUTO_INCREMENT,
  `user_id`       BIGINT(20) NOT NULL,
  `target_id`     BIGINT(20) NOT NULL,
  `relation_type` TINYINT NOT NULL COMMENT '关系类型: 1-关注, 2-粉丝, 3-好友, 4-黑名单',
  `group_id`      BIGINT(20) NOT NULL DEFAULT 0 COMMENT '好友分组ID',
  `deleted`       BOOLEAN NOT NULL DEFAULT FALSE,
  `update_time`   BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY uniq_relation_key(`user_id`, `target_id`, `relation_type`),
  KEY idx_relation_sync(`user_id`, `relation_type`, `update_time`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT='用户关系表';
```

---

## 4. 关键业务逻辑

### 4.1 关系类型定义
系统设计了通用的 `RelationType` 枚举以支持多种业务场景：
*   **强关系**：`FRIEND` (互为好友)
*   **弱关系**：`FOLLOW` (关注) / `FANS` (粉丝)
*   **屏蔽关系**：`BLACK` (拉黑) / `BLOCKED` (被拉黑)

### 4.2 自动化关系达成 (Auto-Match)
当用户 A 向用户 B 发起好友请求时，系统会自动检查“反向意图”：
1.  **检查 B -> A 的记录**：查询 B 是否之前也向 A 发起过请求。
2.  **双向匹配**：如果 B 也有待处理的请求，则**立即达成好友关系** (Make Friends)，无需人工介入。
3.  **单向挂起**：若无，则在 A 侧写入 `MY_REQUEST`，在 B 侧写入 `RECEIVED_REQUEST`，等待 B 处理。

### 4.3 黑名单逻辑 (Blacklist)
拉黑是一个高优先级的覆盖操作：
*   **拉黑时**：若 A 拉黑 B，则 A 和 B 之间原有的任何正向关系（好友、关注）都应被逻辑删除或置为无效。
*   **解除时**：**不应**自动恢复原有关系。解除拉黑仅意味着“不再屏蔽”，之前的关注或好友关系需要重新建立。因此，查询关系时需联合校验 `status` 和 `deleted` 字段。

---

## 5. 高性能优化：大V场景 (Influencer Strategy)

在社交网络中，"大V"（拥有百万级以上粉丝的用户）是系统性能的瓶颈点。查询“我是否关注了某大V”或“某大V是否关注了我”需要区别对待。

### 优化策略：基于数据量的分级查询
假设我们要判断 **用户 A 是否是 用户 B (大V) 的粉丝**：

1.  **普通用户场景 (B 的粉丝数 < 500)**
    *   **策略**：直接加载 B 的粉丝列表。
    *   **操作**：从 Cache/DB 拉取 B 的全量粉丝 ID，在内存中判断 `A in B.fansList`。
    
2.  **中等规模场景 (500 < B 的粉丝数 < 2000)**
    *   **策略**：利用 Redis 有序集合 (ZSet)。
    *   **操作**：使用 Redis Pipeline 批量调用 `ZSCORE` 或 `ZRANK` 进行判定，避免全量拉取带来网络 IO 压力。

3.  **大V场景 (B 的粉丝数 > 2000)**
    *   **策略**：**反向查询 (Reverse Lookup)**。
    *   **操作**：不查 B 的粉丝列表（太大了），改为查 **A 的关注列表**。
    *   **原理**：虽然 B 有几百万粉丝，但 A（普通用户）的关注人数通常有限（几百个）。判断 `B in A.followingList` 的代价远小于处理 B 的粉丝数据。

---

## 6. 即时通讯与推送 (Push & SDK)

为了保证多端数据一致性，系统集成了实时推送机制：
*   **协议**：使用 Protobuf 定义精简的二进制消息体。
*   **触发**：
    *   **关系变更** (`RelationChangedPush`)：关注、加好友成功时触发，SDK 收到后静默更新本地 DB。
    *   **请求到达** (`RelationRequestPush`)：收到好友申请时触发，SDK 弹窗或显示红点。

## 7. 总结与分析

本系统设计体现了典型的**读多写少**互联网架构思想。

*   **优点**：
    *   **查询极快**：2-rows 设计使得最频繁的列表查询复杂度降为 O(1)（索引扫描）。
    *   **大V优化**：巧妙的反向查询策略解决了热点账户的查询性能问题。
    *   **扩展性**：通过 `RelationType` 字段，同一套表结构可以复用于关注、好友、群组等多种社交模型。

*   **潜在风险**：
    *   **存储成本**：随着用户量过亿，关系表数据量会翻倍增长，需提前规划分库分表（Sharding）策略，建议按 `user_id` 进行 Hash 取模分片。
    *   **数据一致性**：双写操作必须依赖可靠的事务机制，建议在应用层封装统一的 `RelationService` 事务模板，防止出现“A关注了B，但B没多粉丝”的脏数据。
