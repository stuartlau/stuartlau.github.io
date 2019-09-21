---
layout:     post
title:      "Stream和BaseStream"
subtitle:   "Stream and BaseStream"
date:       2019-09-16
author:     SL
header-img: img/post-bg-universe.jpg
catalog: true
tags:
    - Algorithm
---
   
> Java 8 API添加了一个新的抽象称为流Stream，可以让你以一种声明的方式处理数据。
>  
> Stream 使用一种类似用 SQL 语句从数据库查询数据的直观方式来提供一种对 Java 集合运算和表达的高阶抽象。
>  
> Stream API可以极大提高Java程序员的生产力，让程序员写出高效率、干净、简洁的代码。
>
> 本文会对Stream的实现原理进行剖析。

### Stream的组成与特点
要想实现计算，所有对流的操作都会被放入一个 `pipeline` 当中（类似linux）中的操作。

而一个流管道（pipeline）包含：
- source(源)： 数组，集合，迭代器，I/O 操作等等
- 0个或者多个中间操作（intermediate operation）： 将一个流转成另外一个流
- 1个终止操作(terminal operation) : 产生一个结果 or 修改传入对象的属性。

注意：流是`Lazy`的，不加「终止操作」流的操作，该流计算就不会被执行。

### 集合和Stream的区别
- 集合： 注重「存储」，主要考虑元素的「访问」与「管理」。
- Stream ：注重「计算」，主要考虑以一种「描述性」的语言来对「源」进行一系列的操作，并将操作「聚合」起来。

### BaseStream
`BaseStream`是所有流实现的顶层接口，它的定义如下：
```java
public interface BaseStream<T, S extends BaseStream<T, S>>
        extends AutoCloseable {
    Iterator<T> iterator();

    Spliterator<T> spliterator();

    boolean isParallel();

    S sequential();

    S parallel();

    S unordered();

    S onClose(Runnable closeHandler);

    void close();
}

```
其中，`T`为流中元素的类型，`S`为一个`BaseStream`的实现类，它里面的元素也是`T`并且`S`同样是自己。

是不是有点晕？

其实很好理解，我们看一下接口中对`S`的使用就知道了：如`sequential()`、`parallel()
`这两个方法，它们都返回了`S
`实例，也就是说它们分别支持对当前流进行`串行`或者`并行`的操作，同时返回「改变」后的流对象。

> 如果是`并行`一定涉及到对当前流的拆分，即将一个流拆分成多个子流，子流肯定和父流的类型是一致的。子流可以继续拆分子流，一直拆分下去...

也就是说这里的`S`是`BaseStream`的一个实现类，它同样是一个流，比如`Stream`、`IntStream`、`LongStream`等。

### Stream
再来看一下我们经常使用的`Stream`的类声明：
```java
public interface Stream<T> extends BaseStream<T, Stream<T>> 
```
参考上面的解释，这里不难理解，即`Stream<T>`可以继续拆分为`Stream<T>`，我们可以通过它的一些方法来证实：
```java
    Stream<T> filter(Predicate<? super T> predicate);
    <R> Stream<R> map(Function<? super T, ? extends R> mapper);
    <R> Stream<R> flatMap(Function<? super T, ? extends Stream<? extends R>> mapper);
    Stream<T> sorted();
    Stream<T> peek(Consumer<? super T> action);
    Stream<T> limit(long maxSize);
    Stream<T> skip(long n);
    ...
```
这些都是操作流的`中间操作`，它们的返回结果一定并且必须是流对象本身。

### 关闭流
BaseStream 实现了 `AutoCloseable` 接口，也就是 `close()` 方法会在流关闭时被调用。同时，`BaseStream` 中还给我们提供了`onClose()`方法：
```java
/**
 * Returns an equivalent stream with an additional close handler.  Close
 * handlers are run when the {@link #close()} method
 * is called on the stream, and are executed in the order they were
 * added.  All close handlers are run, even if earlier close handlers throw
 * exceptions.  If any close handler throws an exception, the first
 * exception thrown will be relayed to the caller of {@code close()}, with
 * any remaining exceptions added to that exception as suppressed exceptions
 * (unless one of the remaining exceptions is the same exception as the
 * first exception, since an exception cannot suppress itself.)  May
 * return itself.
 *
 * <p>This is an <a href="package-summary.html#StreamOps">intermediate
 * operation</a>.
 *
 * @param closeHandler A task to execute when the stream is closed
 * @return a stream with a handler that is run if the stream is closed
 */
S onClose(Runnable closeHandler);
```
当`AutoCloseable`的`close()`接口被调用的时候会触发调用流对象的`onClose()`方法，但有几点需要注意：
- `onClose()` 方法会返回流对象本身，也就是说可以对改对象进行多次调用
- 如果调用了多个`onClose()` 方法，它会按照调用的顺序触发，但是如果某个方法有异常则只会向上抛出第一个异常
- 前一个 `onClose()` 方法抛出了异常不会影响后续 `onClose()` 方法的使用
- 如果多个 `onClose()` 方法都抛出异常，只展示第一个异常的堆栈，而其他异常会被压缩，只展示部分信息

### 并行流和串行流
`BaseStream`接口中分别提供了`并行流`和`串行流`两个方法，这两个方法可以任意调用若干次，也可以混合调用，但最终只会以最后一次方法调用的返回结果为准。

参考`parallel()`方法的说明：
> Returns an equivalent stream that is parallel.  May return
>
> itself, either because the stream was already parallel, or because
>
> the underlying stream state was modified to be parallel.

所以多次调用同样的方法并不会生成新的流，而是直接复用当前的流对象。

> Stream的底层实现是怎样的？将通过下一篇文章继续讲解——Spliterator(分割迭代器)

### References
- http://movingon.cn/2017/05/02/jdk8-Stream-BaseStream-%E6%BA%90%E7%A0%81%E9%9A%BE%E7%82%B9%E6%B5%85%E6%9E%901/
> 本文首次发布于 [ElseF's Blog](http://elsef.com), 作者 [@stuartlau](http://github.com/stuartlau) ,
转载请保留原文链接.
