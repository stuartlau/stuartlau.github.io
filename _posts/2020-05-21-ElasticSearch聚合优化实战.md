---
layout:     post
title:      "ElasticSearch聚合实战"
subtitle:   "Aggregation in ES"
date:       2020-05-21
author:     S.L
header-img: img/home-bg-o.jpg
catalog: true
tags:
    - Search
---

> 线上使用ES做消息相关的检索，如何针对某一个消息关键字进行会话级别的top N条聚合查询？

### 按时间聚合
从官网找一个[例子](https://www.elastic.co/guide/cn/elasticsearch/guide/current/_returning_empty_buckets.html)，最基本的按照时间进行聚合的：
```
{
   "size" : 0,
   "aggs": {
      "sales": {
         "date_histogram": {
            "field": "sold",
            "interval": "month",
            "format": "yyyy-MM-dd",
            "min_doc_count" : 0, 
            "extended_bounds" : { 
                "min" : "2014-01-01",
                "max" : "2014-12-31"
            }
         }
      }
   }
}
```
如根据`sole`字段来进行按日期的聚合，其中每个桶都是按照一个`month`的维度进行，另外我们还对具体的结果进行了格式化以便于阅读。
同时考虑到可能某些月份的结果为空，也需要返回来只做完整的报表，即`min_doc_count : 0`，最关键的，date_histogram （和 histogram 一样）默认只会返回文档数目非零的 buckets。
所以需要使用`extended_bounds`来控制上下界限，防止被默认过滤掉空结果的部分。

### 多层聚合
一个双层聚合的[例子](https://www.elastic.co/guide/cn/elasticsearch/guide/current/_extended_example.html)：
```json
{
   "size" : 0,
   "aggs": {
      "sales": {
         "date_histogram": {
            "field": "sold",
            "interval": "quarter", 
            "format": "yyyy-MM-dd",
            "min_doc_count" : 0,
            "extended_bounds" : {
                "min" : "2014-01-01",
                "max" : "2014-12-31"
            }
         },
         "aggs": {
            "per_make_sum": {
               "terms": {
                  "field": "make"
               },
               "aggs": {
                  "sum_price": {
                     "sum": { "field": "price" } 
                  }
               }
            },
            "total_sum": {
               "sum": { "field": "price" } 
            }
         }
      }
   }
}
```
最终按照每个季度再按照生产商的维度计算了每个生产商的销售额`per_make_sum`，同时还有一个所有生产商的总销售额`total_sum`，
注意这两个聚合的结果都是在第一个聚合结果下，即每个季度的`sales`下的。
![](https://www.elastic.co/guide/cn/elasticsearch/guide/current/images/elas_29in02.png)
如果有了具体的聚合结果，生成报表就方便多了，我们可以对不同的聚合结果用不同的样式展示，如上图的柱状图和折线图，
用类似Kibana和Grafana这种工具很方便生成。

```json
{
    "size" : 0,
    "query" : {
        "constant_score": {
            "filter": {
                "range": {
                    "price": {
                        "gte": 10000
                    }
                }
            }
        }
    },
    "aggs" : {
        "single_avg_price": {
            "avg" : { "field" : "price" }
        }
    }
}
```
这里使用了constant_score 查询和 filter 约束：从根本上讲，使用 non-scoring 查询和使用 match 
查询没有任何区别。查询（包括了一个过滤器）返回一组文档的子集，聚合正是操作这些文档。使用 filtering query 会忽略评分，并有可能会缓存结果数据等等。

### Filter Bucket
我们可以指定一个过滤桶，当文档满足过滤桶的条件时，我们将其加入到桶内，[例子](https://www.elastic.co/guide/cn/elasticsearch/guide/current/_filter_bucket.html)：
```json
{
   "size" : 0,
   "query":{
      "match": {
         "make": "ford"
      }
   },
   "aggs":{
      "recent_sales": {
         "filter": { 
            "range": {
               "sold": {
                  "from": "now-1M"
               }
            }
         },
         "aggs": {
            "average_price":{
               "avg": {
                  "field": "price" 
               }
            }
         }
      }
   }
}
```
使用过滤桶在查询范围基础上应用过滤器，avg 度量只会对 ford 和上个月售出的文档计算平均售价。
> 因为 filter 桶和其他桶的操作方式一样，所以可以随意将其他桶和度量嵌入其中。所有嵌套的组件都会 "继承" 这个过滤，这使我们可以按需针对聚合过滤出选择部分。

### 全局桶
```json
{
    "size" : 0,
    "query" : {
        "match" : {
            "make" : "ford"
        }
    },
    "aggs" : {
        "single_avg_price": {
            "avg" : { "field" : "price" } 
        },
        "all": {
            "global" : {}, 
            "aggs" : {
                "avg_price": {
                    "avg" : { "field" : "price" } 
                }

            }
        }
    }
}
```
single_avg_price 度量计算是基于查询范围内所有文档，即所有 福特 汽车。avg_price 度量是嵌套在 全局 桶下的，这意味着它完全忽略了范围并对所有文档进行计算。聚合返回的平均值是所有汽车的平均售价。
### 实战
下面的例子来自线上，做了一定的脱敏，这是一个`scoping aggregation`的例子：
```json
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "msgText": "hi"
          }
        },
        {
          "bool": {
            "should": [
              {
                "bool": {
                  "filter": [
                    {
                      "term": {
                        "to": "22222222"
                      }
                    },
                    {
                      "range": {
                        "timestamp": {
                          "from": 1589795975534,
                          "to": null,
                          "include_lower": true,
                          "include_upper": true
                        }
                      }
                    }
                  ]
                }
              },
              {
                "bool": {
                  "filter": [
                    {
                      "term": {
                        "to": "11111111"
                      }
                    },
                    {
                      "range": {
                        "timestamp": {
                          "from": 1589771519612,
                          "to": null,
                          "include_lower": true,
                          "include_upper": true
                        }
                      }
                    }
                  ]
                }
              }
            ]
          }
        }
      ]
    }
  },
  "from": 0,
  "aggs": {
    "sessions": {
      "terms": {
        "field": "sessionId",
        "execution_hint": "map",
        "size": 100
      },
      "aggs": {
        "top_ten_hits": {
          "top_hits": {
            "size": 10,
            "sort": {
              "timestamp": {
                "order": "desc"
              }
            }
          }
        }
      }
    }
  }
}
```

结果如下：
```json
{
  "took": 4117,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "failed": 0
  },
  "hits": {
    "total": 3659354,
    "max_score": 0.0,
    "hits": [
      
    ]
  },
  "aggregations": {
    "sessions": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "102162",
          "doc_count": 1606188,
          "top_ten_hits": {
            "hits": {
              "total": 1606188,
              "max_score": null,
              "hits": [
                {
                  "_index": "message_v2",
                  "_type": "message",
                  "_id": "id4",
                  "_score": null,
                  "sort": [
                    1577615548758
                  ]
                },
                {
                  "_index": "message_v2",
                  "_type": "message",
                  "_id": "id3",
                  "_score": null,
                  "sort": [
                    1577615548690
                  ]
                }
              ]
            }
          }
        },
        {
          "key": "102273",
          "doc_count": 47396,
          "top_ten_hits": {
            "hits": {
              "total": 47396,
              "max_score": null,
              "hits": [
                {
                  "_index": "message_v2",
                  "_type": "message",
                  "_id": "id2",
                  "_score": null,
                  "sort": [
                    1578917789916
                  ]
                }
              ]
            }
          }
        }
      ]
    }
  }
}

```
由于我们的mapping设置禁止掉了`_source`，所以结果中没有展示`hits`（不是`aggregations`里的）的内容。

### References
- [聚合](https://www.elastic.co/guide/cn/elasticsearch/guide/current/aggregations.html)
- [elasticsearch 深入 —— Top Hits Aggregation](https://blog.csdn.net/ctwy291314/article/details/82773180)


> 本文首次发布于 [S.L's Blog](http://elsef.com), 作者 [@stuartlau](http://github.com/stuartlau) ,
转载请保留原文链接.
