---
layout:     post
title:      "Resources Access Protection Using Multiple Level Limiter"
subtitle:   "How to control IP access rate limit with multiple limiter"
date:       2018-09-23
author:     SL
header-img: img/post-bg-universe.png
catalog: true
tags:
    - 
---
# What's the Problem
As an API provider, we always want our resources accessed in a safe way, i.e within the 
limit of the capability of our system.

# How to Do It
We can use a JVM-specified counter to record every IP's access activity and prohibit access then 
limit is exceeded.
## One Level Limiter
We can use a single level counter to track each IP's access within a specified period, and 
clean the records every **p** time. 
But what if we also want to restrict the access rule to an upper range of time level, e.g. 5 times per second, 50 times per minute and 1000 times per hour.

## Multiple Level Limiter
We can use multiple level counters to do this work. Each upper layer counter would increase its 
counter when the layers that is lower than it exceeds its limit. 

We use **Max**, **Period** to display the limiter's maximum access times for an single IP in a 
specified time range. Bellow is the diagram I draw to show how multiple level limiters work.
![IP Frequency Limiter Group](http://stuartlau.github.io/img/in-post/ip-frequency-limiter.jpg)