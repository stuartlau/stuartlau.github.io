---
layout:     post
title:      "MySQL的ON-DUPLICATE-KEY语法和批量提交的问题"
subtitle:   "MySQL's ON-DUPLICATE-KEY with BatchUpdate"
date:       2018-12-18
author:     SL
header-img: img/post-bg-universe.jpg
catalog: true
tags:
    - MySQL
---
## INSERT...ON DUPLICATE KEY
这个是MySQL的一个语法，在发生主键冲突或者唯一索引冲突的时候可以对部分属性进行更新，如
```sql
INSERT INTO t1 (a,b,c) VALUES (1,2,3) 
ON DUPLICATE KEY UPDATE c=c+1;

UPDATE t1 SET c=c+1 WHERE a=1;
```
  
上面两句是一个效果。假设此时因为a为唯一索引且1已经存在则会执行*UPDATE c=c+1*的操作保证c可以被更新为新的value。

## VALUES函数
该函数在INSERT..ON DUPLICATE时有效，如VALUES(c)标识INSERT的VALUES(..)里对应的c字段的值，即待插入的值。如
```sql
INSERT INTO t1 (a,b,c) VALUES (1,2,3),(4,5,6)
ON DUPLICATE KEY UPDATE c=VALUES(a)+VALUES(b);
```

通过一条SQL完成了对两个主键或唯一索引冲突时的数据变更其他字段。
所以对于批量插入或更新的操作可以直接使用上述语法来完成功能，因为这个语法可以被MySQL driver层面进行合并成一个SQL。

## Batch提交
Batch提交是用一个Connection来对若干个SQL进行一次性、批量提交给MySQL处理。但有一个问题是，如果某个SQL
挂了而其他的并不会受影响，这样就无法保证原子性，只能再封装一层Transaction来实现。
同时，Batch处理并不是每个Server都支持的，需要看具体的产品和版本号。
  
## 代码
我们通过观察具体的客户端实现代码来了解批量提交是如何实现的
spring-jdbc-5.1.3.RELEASE中的实现如下：
```java
@Override
	public int[] batchUpdate(String sql, SqlParameterSource[] batchArgs) {
		if (batchArgs.length == 0) {
			return new int[0];
		}

		ParsedSql parsedSql = getParsedSql(sql);
		PreparedStatementCreatorFactory pscf = getPreparedStatementCreatorFactory(parsedSql, batchArgs[0]);
        // 调用另外一个batchUpdate方法
		return getJdbcOperations().batchUpdate(
				pscf.getSql(),
				new BatchPreparedStatementSetter() {
					@Override
					public void setValues(PreparedStatement ps, int i) throws SQLException {
						Object[] values = NamedParameterUtils.buildValueArray(parsedSql, batchArgs[i], null);
						pscf.newPreparedStatementSetter(values).setValues(ps);
					}
					@Override
					public int getBatchSize() {
						return batchArgs.length;
					}
				});
	}
```
第二个batchUpdate方法如下：
```java
@Override
	public int[] batchUpdate(String sql, final BatchPreparedStatementSetter pss) throws DataAccessException {
		if (logger.isDebugEnabled()) {
			logger.debug("Executing SQL batch update [" + sql + "]");
		}

		// 调用execute方法，传入sql和回调接口
		int[] result = execute(sql, (PreparedStatementCallback<int[]>) ps -> {
			try {
				int batchSize = pss.getBatchSize();
				InterruptibleBatchPreparedStatementSetter ipss =
						(pss instanceof InterruptibleBatchPreparedStatementSetter ?
						(InterruptibleBatchPreparedStatementSetter) pss : null);
				if (JdbcUtils.supportsBatchUpdates(ps.getConnection())) {
				    // 如果支持批处理操作则依次将每个SQL的参数进行填充
					for (int i = 0; i < batchSize; i++) {
						pss.setValues(ps, i);
						if (ipss != null && ipss.isBatchExhausted(i)) {
							break;
						}
						ps.addBatch();
					}
					// 执行批处理函数（底层交给jdbc driver的实现类去执行，如mysql-connector-java）
					return ps.executeBatch();
				}
				else {
					List<Integer> rowsAffected = new ArrayList<>();
					for (int i = 0; i < batchSize; i++) {
						pss.setValues(ps, i);
						if (ipss != null && ipss.isBatchExhausted(i)) {
							break;
						}
						rowsAffected.add(ps.executeUpdate());
					}
					int[] rowsAffectedArray = new int[rowsAffected.size()];
					for (int i = 0; i < rowsAffectedArray.length; i++) {
						rowsAffectedArray[i] = rowsAffected.get(i);
					}
					return rowsAffectedArray;
				}
			}
			finally {
				if (pss instanceof ParameterDisposer) {
					((ParameterDisposer) pss).cleanupParameters();
				}
			}
		});

		Assert.state(result != null, "No result array");
		return result;
	}
```
对应的execute方法如下：
```java
public <T> T execute(PreparedStatementCreator psc, PreparedStatementCallback<T> action)
			throws DataAccessException {

		Assert.notNull(psc, "PreparedStatementCreator must not be null");
		Assert.notNull(action, "Callback object must not be null");
		if (logger.isDebugEnabled()) {
			String sql = getSql(psc);
			logger.debug("Executing prepared SQL statement" + (sql != null ? " [" + sql + "]" : ""));
		}

		Connection con = DataSourceUtils.getConnection(obtainDataSource());
		PreparedStatement ps = null;
		try {
			ps = psc.createPreparedStatement(con);
			applyStatementSettings(ps);
			T result = action.doInPreparedStatement(ps);
			handleWarnings(ps);
			return result;
		}
		catch (SQLException ex) {
			// Release Connection early, to avoid potential connection pool deadlock
			// in the case when the exception translator hasn't been initialized yet.
			if (psc instanceof ParameterDisposer) {
				((ParameterDisposer) psc).cleanupParameters();
			}
			String sql = getSql(psc);
			JdbcUtils.closeStatement(ps);
			ps = null;
			DataSourceUtils.releaseConnection(con, getDataSource());
			con = null;
			throw translateException("PreparedStatementCallback", sql, ex);
		}
		finally {
			if (psc instanceof ParameterDisposer) {
				((ParameterDisposer) psc).cleanupParameters();
			}
			JdbcUtils.closeStatement(ps);
			DataSourceUtils.releaseConnection(con, getDataSource());
		}
	}
```
上面是spring-jdbc的batchUpdate逻辑的实现，但是具体的业务执行是由Server来执行的，所以不同的Server的实现机制不同可能对性能有较大影响。
以MySQL为例，在mysql-connector-java-5.1.43的实现如下：
```java
    public boolean canRewriteAsMultiValueInsertAtSqlLevel() throws SQLException {
        return this.parseInfo.canRewriteAsMultiValueInsert;
    }
    
    @Override
        protected long[] executeBatchInternal() throws SQLException {
            synchronized (checkClosed().getConnectionMutex()) {
    
                if (this.connection.isReadOnly()) {
                    throw new SQLException(Messages.getString("PreparedStatement.25") + Messages.getString("PreparedStatement.26"),
                            SQLError.SQL_STATE_ILLEGAL_ARGUMENT);
                }
    
                if (this.batchedArgs == null || this.batchedArgs.size() == 0) {
                    return new long[0];
                }
    
                // we timeout the entire batch, not individual statements
                int batchTimeout = this.timeoutInMillis;
                this.timeoutInMillis = 0;
    
                resetCancelledState();
    
                try {
                    statementBegins();
    
                    clearWarnings();
    
                    if (!this.batchHasPlainStatements && this.connection.getRewriteBatchedStatements()) {
    
                        if (canRewriteAsMultiValueInsertAtSqlLevel()) {
                            return executeBatchedInserts(batchTimeout);
                        }
    
                        if (this.connection.versionMeetsMinimum(4, 1, 0) && !this.batchHasPlainStatements && this.batchedArgs != null
                                && this.batchedArgs.size() > 3 /* cost of option setting rt-wise */) {
                            return executePreparedBatchAsMultiStatement(batchTimeout);
                        }
                    }
    
                    return executeBatchSerially(batchTimeout);
                } finally {
                    this.statementExecuting.set(false);
    
                    clearBatch();
                }
            }
        }
    
    /**
     * Rewrites the already prepared statement into a multi-value insert
     * statement of 'statementsPerBatch' values and executes the entire batch
     * using this new statement.
     * 
     * @return update counts in the same fashion as executeBatch()
     * 
     * @throws SQLException
     */
    protected long[] executeBatchedInserts(int batchTimeout) throws SQLException {
        synchronized (checkClosed().getConnectionMutex()) {
            String valuesClause = getValuesClause();

            MySQLConnection locallyScopedConn = this.connection;

            if (valuesClause == null) {
                return executeBatchSerially(batchTimeout);
            }

            int numBatchedArgs = this.batchedArgs.size();

            if (this.retrieveGeneratedKeys) {
                this.batchedGeneratedKeys = new ArrayList<ResultSetRow>(numBatchedArgs);
            }

            int numValuesPerBatch = computeBatchSize(numBatchedArgs);

            if (numBatchedArgs < numValuesPerBatch) {
                numValuesPerBatch = numBatchedArgs;
            }

            PreparedStatement batchedStatement = null;

            int batchedParamIndex = 1;
            long updateCountRunningTotal = 0;
            int numberToExecuteAsMultiValue = 0;
            int batchCounter = 0;
            CancelTask timeoutTask = null;
            SQLException sqlEx = null;

            long[] updateCounts = new long[numBatchedArgs];

            try {
                try {
                    batchedStatement = /* FIXME -if we ever care about folks proxying our MySQLConnection */
                            prepareBatchedInsertSQL(locallyScopedConn, numValuesPerBatch);

                    if (locallyScopedConn.getEnableQueryTimeouts() && batchTimeout != 0 && locallyScopedConn.versionMeetsMinimum(5, 0, 0)) {
                        timeoutTask = new CancelTask(batchedStatement);
                        locallyScopedConn.getCancelTimer().schedule(timeoutTask, batchTimeout);
                    }

                    if (numBatchedArgs < numValuesPerBatch) {
                        numberToExecuteAsMultiValue = numBatchedArgs;
                    } else {
                        numberToExecuteAsMultiValue = numBatchedArgs / numValuesPerBatch;
                    }

                    int numberArgsToExecute = numberToExecuteAsMultiValue * numValuesPerBatch;

                    for (int i = 0; i < numberArgsToExecute; i++) {
                        if (i != 0 && i % numValuesPerBatch == 0) {
                            try {
                                updateCountRunningTotal += batchedStatement.executeLargeUpdate();
                            } catch (SQLException ex) {
                                sqlEx = handleExceptionForBatch(batchCounter - 1, numValuesPerBatch, updateCounts, ex);
                            }

                            getBatchedGeneratedKeys(batchedStatement);
                            batchedStatement.clearParameters();
                            batchedParamIndex = 1;

                        }

                        batchedParamIndex = setOneBatchedParameterSet(batchedStatement, batchedParamIndex, this.batchedArgs.get(batchCounter++));
                    }

                    try {
                        updateCountRunningTotal += batchedStatement.executeLargeUpdate();
                    } catch (SQLException ex) {
                        sqlEx = handleExceptionForBatch(batchCounter - 1, numValuesPerBatch, updateCounts, ex);
                    }

                    getBatchedGeneratedKeys(batchedStatement);

                    numValuesPerBatch = numBatchedArgs - batchCounter;
                } finally {
                    if (batchedStatement != null) {
                        batchedStatement.close();
                        batchedStatement = null;
                    }
                }

                try {
                    if (numValuesPerBatch > 0) {
                        batchedStatement = prepareBatchedInsertSQL(locallyScopedConn, numValuesPerBatch);

                        if (timeoutTask != null) {
                            timeoutTask.toCancel = batchedStatement;
                        }

                        batchedParamIndex = 1;

                        while (batchCounter < numBatchedArgs) {
                            batchedParamIndex = setOneBatchedParameterSet(batchedStatement, batchedParamIndex, this.batchedArgs.get(batchCounter++));
                        }

                        try {
                            updateCountRunningTotal += batchedStatement.executeLargeUpdate();
                        } catch (SQLException ex) {
                            sqlEx = handleExceptionForBatch(batchCounter - 1, numValuesPerBatch, updateCounts, ex);
                        }

                        getBatchedGeneratedKeys(batchedStatement);
                    }

                    if (sqlEx != null) {
                        throw SQLError.createBatchUpdateException(sqlEx, updateCounts, getExceptionInterceptor());
                    }

                    if (numBatchedArgs > 1) {
                        long updCount = updateCountRunningTotal > 0 ? java.sql.Statement.SUCCESS_NO_INFO : 0;
                        for (int j = 0; j < numBatchedArgs; j++) {
                            updateCounts[j] = updCount;
                        }
                    } else {
                        updateCounts[0] = updateCountRunningTotal;
                    }
                    return updateCounts;
                } finally {
                    if (batchedStatement != null) {
                        batchedStatement.close();
                    }
                }
            } finally {
                if (timeoutTask != null) {
                    timeoutTask.cancel();
                    locallyScopedConn.getCancelTimer().purge();
                }

                resetCancelledState();
            }
        }
    }
```
## References
- https://dev.mysql.com/doc/refman/5.7/en/insert-on-duplicate.html

> 本文首次发布于 [ElseF's Blog](http://elsef.com), 作者 [@stuartlau](http://github.com/stuartlau) ,
转载请保留原文链接.
