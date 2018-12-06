---
layout:     post
title:      "ProtoBuf3.0编码的FAQ"
subtitle:   "ProtoBuf3.0 Encoding FAQ"
date:       2018-12-06
author:     SL
header-img: img/post-bg-universe.jpg
catalog: true
tags:
    - ProtoBuf
    - FAQ
    - Encoding
---
    
> ProtoBuf作为服务器端RPC实现中编解码的常用选型以其编码后字节少、向后兼容性好和传输性能高著称，本文讨论一下它的编码方面的实现问题。

## 编码方法的介绍
编码中一个显然的问题是数字编码，默认情况下根据操作系统的不同基本单位占用的字节也不一样。以int32为例，默认表示一个整数，占用32个bit。也就是说无论数值有多小，如1还是最大值2^31
-1，它都会占用4个字节。很显然对于小的数字来说是一种存储浪费，而我们平常大部分使用的场景都是小数字。
所以ProtoBuf引入了Varint。

### Varint
使用Varint进行编码则有可能缩减到1个字节。反过来，如果是比较大的数字，如已经占用了4个字节，那么则可能最后要需要占用5个字节。

简单看一下它的定义：
> Each byte in a varint, except the last byte, has the most significant bit (msb) set – this indicates that there are further bytes to come. The lower 7 bits of each byte are used to store the two’s complement representation of the number in groups of 7 bits, least significant group first.

Varint中的每个字节的最高位bit有特殊的含义：
- 该位为1表示后续的字节也是该数字的一部分
- 该位为0则是最后一个字节

其他的 7 个bit都用来表示数字，从最低有效字节开始。如：
- 1的二进制表示为0000 0001，通过Varint编码后的二进制表示为**0000 0001**
- 300的二进制表示为100101100，通过Varint编码后的二进制表示为**10101100 00000010**

但是这里又出现了一个问题，即因为int32里负数会占用4个字节（高位为符号位），就导致负数一定会占用5个字节，即还多了一个。
下面介绍Zigzag。

### Zigzag
ZigZag编码将有符整型转化成无符的整型，其原理是将最高位的符号位放到最低位（－1除外），这样大大减少了字节占用。
> Note that the second shift – the (n » 31) part – is an arithmetic shift. So, in other words, the result of the shift is either a number that is all zero bits (if n is positive) or all one bits (if n is negative).

公式如下：
- 32位整型：(n « 1) ^ (n » 31)
- 64位整型：(n « 1) ^ (n » 63)

上面的计算非常繁琐：其中n是具体数值的补码标识，然后经过向左移动1位然后和向右带符号移63位的数值进行异或操作。一般人还真不一定能算对。
这里给出一个快速计算的方法：
- 如果是正数，直接乘以2
- 如果是负数，直接乘以2再减一
如-150的Zigzag算完之后是：150*2-1=299

好介绍完基本的算法，我们介绍原理。

## ProtoBuf的编码FAQ

### 如何表示一个属性？
在proto文件中我们用一个具体的tag number来表示属性的顺序，该值从1开始，没有上限。enum需要从0开始。
而在ProtoBuf序列化的时候将这个tag number和它对应的数据类型定义为一个key，它是一个用Varint编码后的值，表达式为：(tag number << 3)|wire_type
即key的最低三位表示字段类型，将key右移三位后的值表示tag number，字段的类型定义如下，目前使用最多的是0和2两个值。

| Type | Meaning            | Used for                                                 |
| ---- | ------------------ | -------------------------------------------------------- |
| 0    | Varint             | int32, int64, uint32, uint64, sint32, sint64, bool, enum |
| 1    | 64-bit             | fixed64, sfixed64, double                                |
| 2    | Lengthed-delimited | string, bytes, embedded messages, packed repeated fields |
| 3    | Start group        | groups (deprecated)                                      |
| 4    | End group          | groups (deprecated)                                      |
| 5    | 32-bit             | fixed32, sfixed32, float                                 |



### 如何做到向后兼容？
也就是说旧版本的解析程序是如何自动跳过新字段的呢？如
```proto
message old_message{
    int32 a = 1;
    int32 b = 2;
    int32 d = 4;
}
```
上述例子是一个proto3的一个典型的message结构，其中tag number跳过了3，是可以的只要不冲突都可以编译通过。
如果发送方升级了协议，增加了一个tag number=3的字段：
```proto
message old_message{
    int32 a = 1;
    int32 b = 2;
    int64 c = 3;
    int32 d = 4;
}
```
那么接收端在未升级的情况下是如何正确解析新版本的数据包的呢？肯定不回按顺序解析，否则就会将c值赋值到了d上。答案是它会「跳过」不认识的tag number。

ProtoBuf把tag number和其类型wire_type一起写进字节流里去，解码程序只要解析出不认识的tag number，就能知道该字段是新协议定义的，再通过其类型可以推断出该字段内容的长度，就能正确的跳过这部分 
buffer，继续解析下一个字段。
上面的例子中：当旧的解码程序解析到tag number为3时，发现在旧协议里找不到该tag number，又从其类型int64知道该tag number的值占了8个字节，于是跳过这8个字节，继续解析剩下的字节流。

### 如何处理不定长的数据？
Length-delimited Type这种变长类型在PB中wire_type为2，对应的类型包括string/repeated fields/embedded message/bytes等。
要在key后面多写入长度信息，注意该值同样要使用Varint编码。
```proto
message StringMessage{
    string name = 1;
}
```
如果name的值设为*testing*，PB编码后的十六进制字节流为**12 07 74 65 73 74 69 6e 
67**，其中key为0x12，可以算出tag number值为2（0x12>>3，00010010带符号右移3位是00000010，即十进制的2), type为2 
(**0x12**取最低三位，用最低三位存储类型)。下个字节为**0x07**，该字节表示长度，因此后续的7个字节都为该tag number表示的value。

### 如何处理负数？
ProtoBuf使用sint32/sint64类型专门用于编码负数。如果使用int32/int64来编码负数，通过Varint编码后的buffer长达5/10个字节。
而sint32/sint64类型的值会先经过Zigzag编码，转换成无符号整数，再采用Varint编码，可以大大减少编码后占用的字节数。

> If you use int32 or int64 as the type for a negative number, the resulting varint is always ten bytes long – it is, effectively, treated like a very large unsigned integer. If you use one of the signed types, the resulting varint uses ZigZag encoding, which is much more efficient.

### 可否修改老协议的tag number？
不可以，因为key是需要通过tag number来生成的，tag number变了，key就变了，找不到对应的key将会报错。

### 可否修改老协议的某个tag number的name？
可以，PB数据的反序列化与name无关，只跟tag number和wire_type有关。

### 为什么repeated字段的tag number最好不要超过15？
因为tag number从16开始往后的所有数值在使用Varint时都将使用2个字节来表示，所以repeated的数据类型在序列化时每个元素都将多使用1个字节。如果repeated
内数据量很多，那么对空间的浪费也是很严重的。
如一个类型为string的字段的tag number为16，那么它的key（Varint编码，注意是little-endian的编码）用的二进制表示为：**1000 0002 0000 
0001**


> 本文首次发布于 [ElseF's Blog](http://elsef.com), 作者 [@stuartlau](http://github.com/stuartlau) ,
转载请保留原文链接.
