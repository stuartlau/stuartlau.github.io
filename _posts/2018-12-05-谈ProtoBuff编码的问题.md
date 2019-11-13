---
layout:     post
title:      "ProtoBuf3.0编码的深入分析"
subtitle:   "Details about ProtoBuf3.0 Encoding"
date:       2018-12-06
author:     S.L
header-img: img/home-bg-o.jpg
catalog: true
tags:
    - Encoding
---
    
> ProtoBuf作为服务器端RPC实现中编解码的常用选型以其编码后字节少、向后兼容性好和传输性能高著称，本文讨论一下它的编码方面的实现问题。

### 编码方法的介绍
编码中一个显然的问题是数字编码，默认情况下根据操作系统的不同基本单位占用的字节也不一样。以int32为例，默认表示一个整数，占用32个bit。也就是说无论数值有多小，如1还是最大值2^31
-1，它都会占用4个字节。很显然对于小的数字来说是一种存储浪费，而我们平常大部分使用的场景都是小数字。
所以ProtoBuf引入了Varint。

#### Varint
使用Varint进行编码则有可能缩减到1个字节。反过来，如果是比较大的数字，如已经占用了4个字节，那么则可能最后要需要占用5个字节。（其实用了10个字节）

简单看一下官网对它的定义：
> Each byte in a varint, except the last byte, has the most significant bit (msb) set – this indicates that there are further bytes to come. The lower 7 bits of each byte are used to store the two’s complement representation of the number in groups of 7 bits, least significant group first.

Varint中的每个字节的最高位bit（msb）有特殊的含义：
- 该位为1表示后续的字节也是该数字的一部分
- 该位为0则是最后一个字节
- 整个数据是按照 *least significant group first* 排列的，即little-endian

其他低位的 `7` 个bit都用来表示真实的数据，排列从最低有效字节开始。比如：
- 1的二进制表示为0000 0001，通过Varint编码后的二进制表示为**0000 0001**
- 300的二进制表示为100101100，通过Varint编码后的二进制表示为**10101100 00000010**

> 所以我们序列化之后看到的字节数组并不是真正直观意义上的数值或ASCII内容，而是首先需要通过Varint进行分析出一个完整的编码后再
重新按规则组合成真正的二进制数据。

但是这里又出现了一个问题，即因为int32里负数会占用4个字节（高位为符号位），就导致负数一定会占用5个字节，即还多了一个。

但实际测试就会发现，其实int32负数最终会使用10个字节（不解），所以对于负数的处理非常不友好。

> 从下面FAQ中的例子可以看到
>
> 当使用int32时，-2占用了10个字节（32是key）
>
> 32, -2, -1, -1, -1, -1, -1, -1, -1, -1, 1
>
> 因为int32会强制转换成uint64，在序列化时使用Varint编码，每个字节用7位，64位总共需要需要10个字节。


下面介绍Zigzag。

#### Zigzag
ZigZag编码将有符整型转化成无符的整型，其原理是将最高位的符号位放到最低位（－1除外），这样大大减少了字节占用。
> Note that the second shift – the (n » 31) part – is an arithmetic shift. So, in other words, the result of the shift is either a number that is all zero bits (if n is positive) or all one bits (if n is negative).

公式如下：
- 32位整型：(n « 1) ^ (n » 31)
- 64位整型：(n « 1) ^ (n » 63)

上面的计算非常繁琐：其中n是具体数值的补码标识，然后经过向左移动1位然后和向右带符号移63位的数值进行异或操作。很复杂，一般还真不一定能算对。
这里给出一个快速计算的方法：
- 如果是正数，直接乘以2
- 如果是负数，直接乘以2再减一
如-150的Zigzag算完之后是：150*2-1=299

### ProtoBuf的编码FAQ

#### 如何表示一个属性？
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



#### 如何做到向后兼容？
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

#### 如何处理不定长的数据？
Length-delimited Type这种变长类型在PB中wire_type为2，对应的类型包括string/repeated fields/embedded message/bytes等。
要在key后面多写入长度信息，注意该值同样要使用Varint编码。
```proto
message StringMessage{
    string name = 2;
}
```
如果name的值设为*testing*，PB编码后的十六进制字节流为**12 07 74 65 73 74 69 6e 
67**，其中key为0x12，可以算出tag number值为2（0x12>>3，0001 0010带符号右移3位是00000010，即十进制的2)，type为2 
(**0x12**取最低三位，用最低三位存储类型)。紧跟着的字节Varint表示长度，通过分析，应该是**0x07**，即7个字节，为什么呢？因为它的二进制是
*0000 0111*，即msb为0表示后面的字节已经不属于当前属性的范畴，因此后续的7个字节都为该tag number表示的value。

#### sint32的优化
我们来分析一下对于负数的优化，这里增加sint32和int32进行对比：
```java
message StringMessage{
    string name = 1;
    sint32 i = 3;
    int32 i2 = 4;
}
```
其中的属性值，name的值保持不变为*testing*，*i*和*i2*均赋值为 `-2` ，然后将字节数组打印如下（10进制）：
> [
>
>  10, 7, 116, 101, 115, 116, 105, 110, 103,
> 
>  24, 3,
> 
>  32, -2, -1, -1, -1, -1, -1, -1, -1, -1, 1
>
> ]

对于tag计算，可以通过两个属性的key值24和32分别分析出tag为3和4，这里不再做推演。

值得注意的是因为i是sint32类型使用Zigzag编码，对负数的处理是将其变为正数，这里是2*2-1=3，所以仅使用一个字节，极大优化了存储。
而*i2*因为是int32类型可以看到使用了10个字节。感兴趣还可以测试一下如果用uint32存储会使用5个字节。
#### 不同类型数值之间的兼容性问题
我们使用两个PB结构进行序列化和反序列化的测试，看我们能够解析出什么样的值。
```java
message StringMessage {
    string name = 1;
    sint32 i = 3;
    int32 i1 = 7;
    int32 i2 = 4;
    int32 i3 = 5;
    int64 i4 = 6;
    int32 i5 = 8;
}
message StringMessage2 {
    string name = 1;
    int32 i = 3;
    int64 i1 = 7;
    int64 i2 = 4;
    int64 i3 = 5;
    int32 i4 = 6;
    sint32 i5 = 8;
}
```
其中 `StringMessage` 用于序列化，并将其序列化的字节信息进行反序列化为 `StringMessage2`，用于验证：
- 1. 是否可以成功反序列化
- 2. 对应的属性值是否能够保持和之前的一致
- 3. 查看int32、int64以及sint32之间的兼容性问题

```java
public static void main(String[] args) throws InvalidProtocolBufferException {
    StringMessage sm = StringMessage.newBuilder()
            .setName("testing")
            .setI(-2) // sint32
            .setI2(-2) // int32
            .setI3(Integer.MAX_VALUE) // int32
            .setI4(Integer.MAX_VALUE+100L) // int64
            .setI1(2) // int32
            .setI5(-1) // int32
            .build();
    byte[] array = sm.toByteArray();
    System.out.println(Arrays.toString(array));
    StringMessage2 sm2 = StringMessage2.parseFrom(array);
    System.out.println(sm2.getI()); // int32
    System.out.println(sm2.getI2()); // int64
    System.out.println(sm2.getI3()); // int64
    System.out.println(sm2.getI4()); // int32
    System.out.println(sm2.getI1()); // int64
    System.out.println(sm2.getI5()); // sint32
    array = sm2.toByteArray();
    System.out.println(Arrays.toString(array));
}
```
输出结果如下：
```
[10, 7, 116, 101, 115, 116, 105, 110, 103, 24, 3, 32, -2, -1, -1, -1, -1, -1, -1, -1, -1, 1, 40, -1, -1, -1, -1, 7, 48, -29, -128, -128, -128, 8, 56, 2, 64, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1]
3
-2
2147483647
-2147483549
2
-2147483648
[10, 7, 116, 101, 115, 116, 105, 110, 103, 24, 3, 32, -2, -1, -1, -1, -1, -1, -1, -1, -1, 1, 40, -1, -1, -1, -1, 7, 48, -29, -128, -128, -128, -8, -1, -1, -1, -1, 1, 56, 2, 64, -1, -1, -1, -1, 15]
```
从上面的输出中我们可以得到如下结论：
- 1. 如果仅改变了数值相关的属性，那么前后两个PB是可以互相兼容的（反序列化成功）
- 2. 如果sint32存储的是负数，改为int32后则会解析成正数，即数据真值会丢失
- 3. 对于i2和i3，存储的都是「大数字」，一个是负数，一个是int最大值，所以用10个字节进行表示（`32, -2, -1, -1, -1, -1, -1, -1, -1, -1, 
1`），这很显然超过了Java中int只占4个字节的大小，效率变差了，所以如果存储「大数字」不要用int32，那用啥？sint32。
- 4. i4使用int64存储了一个超过int32能保存的最大值，所以用int32解析后变成了负数（长度也变为用10
个字节存储），也就是说从高纬度降维到低纬度，只能在低纬度能承受的范围之内，否则会丢失真值
- 5. i1从低维度转化为高纬度int64是没有问题的，比如这里的2

#### 如何处理负数？
ProtoBuf使用sint32/sint64类型专门用于编码负数。如果使用int32/int64来编码负数，通过Varint编码后的buffer长达5/10个字节（其实是10个）。
而sint32/sint64类型的值会先经过Zigzag编码，转换成无符号整数，再采用Varint编码，可以大大减少编码后占用的字节数。

下面摘自[官网](https://developers.google.com/protocol-buffers/docs/encoding#types)
> If you use int32 or int64 as the type for a negative number, the resulting varint is always ten bytes long – it is, effectively, treated like a very large unsigned integer. If you use one of the signed types, the resulting varint uses ZigZag encoding, which is much more efficient.

#### 如何处理嵌套结构？
Embedded Messages
```java
message Test1 {
  optional int32 a = 1;
}

message Test3 {
  optional Test1 c = 3;
}
```
如果将Test1的a设置为150，那么它序列化的结果如下：
> 08 96 01

那么Test3呢？
> 1a 03 08 96 01

可以通过1a分析出tag=3，wire_type=2，即可边长类型，所以后面的一个字节为长度，即它后面的3个字节为数据Test1的内容。

而后面的三个字节跟我们单独序列化Test1的内容一样，即从Test1的角度从新开始解析每一个field的tag、wire_type以及data。

#### 如何处理repeated结构
- 数字类型
PB对数字类型的repeated结构使用如下规则进行序列化：
> |tag|dataByteSize|data|data|..|

例子
```java
message RepeatedMessage {
    repeated int32 a = 1;
}
```
其中写入三个数字2、3、150，序列化的结果如下所示
> [10, 4, 2, 3, -106, 1]

注意都是Varint编码的二进制，tag=1，wire_type=2。

- 变长类型
而对于变长类型的repeated结构则使用了另一套规则进行序列化：
> |tag|dataByteSize|data|tag|dataByteSize|data|..|

也就是说每个元素都会按照 `|tag|dataByteSize|data|` 的规则进行序列化，tag是重复的。

例子
```java
message RepeatedMessage2 {
    repeated string a = 1;
}
```
其中写入2个字符串，分别是"aaaa"和"b"，序列化的结果如下所示
> [10, 4, 97, 97, 97, 97, 10, 1, 98]

可以看到和数字类型序列化的区别。

#### Packed修饰符
在2.0版本中对repeated类型的结构引入了一个额外packed修饰符，用于优化序列化的算法，而在3.0版本中它已经是默认的实现。

> 目前ProtoBuf只支持基本类型的packed修饰，因而如果将packed添加到非repeated字段或非基本类型的repeated字段，编译器在编译.proto文件时会报错。

为什么引入它？
有人说是因为之前的版本对于基本类型数据的repeated格式使用的序列化规则效率太低，导致tag被存储多次。
> |tag|data|tag|data|...

所以对其进行了压缩处理，这样效率更高，也就变成了我上面说的对于「数字类型的repeated」序列化的实现。这个说法并无从考证，只能证明目前使用的序列化方式确实是性能比较好的。
至于之前版本的实现方案，有兴趣的可以亲测一下，看看是不是那篇[帖子](http://www.blogjava.net/DLevin/archive/2015/04/01/424011.html)里说的那样。
  
拿官网中的例子，有一个结构定义如下，声明了是压缩的（[packed=true]）：
```java
message Test4 {
  repeated int32 d = 4 [packed=true];
}
```
写入三个数字3，270和86942，则序列化后的结果如下：
```
22        // key (field number 4, wire type 2)
06        // payload size (6 bytes)
03        // first element (varint 3)
8E 02     // second element (varint 270)
9E A7 05  // third element (varint 86942)
```
这与我上面的对于「数字类型的repeated」序列化的实现验证是一致的。

#### 可否修改老协议的tag number？
不可以，因为key是需要通过tag number来生成的，tag number变了，key就变了，找不到对应的key将会报错。

#### 可否修改老协议的某个tag number的name？
可以，PB数据的反序列化与name无关，只跟tag number和wire_type有关。

#### 为什么repeated字段的tag number最好不要超过15？
因为tag number从16开始往后的所有数值在使用Varint时都将使用2个字节来表示，所以repeated的数据类型在序列化时每个元素都将多使用1个字节。如果repeated
内数据量很多，那么对空间的浪费也是很严重的。
如一个类型为string的字段的tag number为16，那么它的key（Varint编码，注意是little-endian的编码）用的二进制表示为：**1000 0010 0000 
0001**。

计算方法：首先string的wire_type为十进制2，tag number的二进制为00010000（指16），套用公式(tag number << 3)
|wire_type来计算key，即10000000|00000010，结果为10000010，然后对这个数计算Varint，按七位截取，并且是little-endian
，即两个字节，第一个字节的最高位为1，即1000 0010，第二个字节为最后一个字节，最高为0，即0000 0001，加起来就是1000 0010 0000 0001两个字节。

> 1000 0010 0000 0001
>
> 第一个1为标记位表示后面的字节也是当前的值的一部分
>
> 此后的7个bit为数值位，因为是little-endian，所以就是计算出来的10000010的后7个bit
>
> 上面的第一个字节的分析，下面分析第二个字节
>
> 第一个0位标记位，表示这个整个数据的最后一个字节了
>
> 此后的7个bit为数值为，因为是little-endian，所以就是计算出来的10000010的抛出去最低7bit的部分，因为只有一个bit，所以高部分用0凑

### References
- [protocol-buffers-encoding](https://developers.google.com/protocol-buffers/docs/encoding)

> 本文首次发布于 [S.L's Blog](http://elsef.com), 作者 [@stuartlau](http://github.com/stuartlau) ,
转载请保留原文链接.
