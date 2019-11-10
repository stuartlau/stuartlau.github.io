---
layout:     post
title:      "把Future扔进CompletableFuture的封装里"
subtitle:   "CompletableFuture in Java"
date:       2019-11-10
author:     S.L
header-img: img/home-bg-o.jpg
catalog: true
tags:
    - Java
---
> 关于异步编程，之前一直在项目中使用Guava的ListenableFuture，对于JDK8的CompletableFuture使用较少。
>
> 注：这篇文章绝大部分内容都来自colobu.com中的《Java CompletableFuture 详解》的介绍，感谢作者。后续我会统一改成自己的内容。

### Future In JDK5
Future是JDK5添加的类，用来描述一个异步计算的结果。可以用isDone方法来检查计算是否完成，或者使用get阻塞住调用线程，直至计算完成返回结果，也可以用cancel方法来停止任务的执行。

```java
public class BasicFuture {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        ExecutorService es = Executors.newFixedThreadPool(10);
        Future<Integer> f = es.submit(() -> {
            // 长时间的异步计算
            // ...
            // 然后返回结果
            return 100;
        });
        f.get();
    }
}
```
Future以及相关使用方法提供了异步执行任务的能力，但对于结果的获取却是不方便，只能通过阻塞或轮询的方式得到任务结果。阻塞的方式与我们理解的异步编程其实是相违背的，而轮询又会耗无谓的CPU资源。而且还不能及时得到计算结果，为什么不能用观察者设计模式当计算结果完成及时通知监听者呢？

### Future in Netty
很多语言像Node.js，采用回调的方式实现异步编程。Java的一些框架像Netty，自己扩展Java的Future接口，提供了addListener等多个扩展方法：

```java
ChannelFuture future = bootstrap.connect(new InetSocketAddress(host, port));
future.addListener(new ChannelFutureListener() {
    @Override
    public void operationComplete(ChannelFuture future) throws Exception{
      if (future.isSuccess()) {
          // SUCCESS
      }
      else {
          // FAILURE
      }
    }
});
```
### CompletableFuture in JDK8
在Java 8中, 新增加了一个包含50个方法左右的类:CompletableFuture，提供了非常强大的Future的扩展功能，可以帮助我们简化异步编程的复杂性，提供了函数式编程的能力，可以通过回调的方式处理计算结果，并且提供了转换和组合CompletableFuture的方法。
#### 主动完成计算
CompletableFuture类实现了CompletionStage和Future接口，所以你还是可以像以前一样通过阻塞或者轮询的方式获得结果，尽管这种方式不推荐使用。

```java
public T    get()
public T    get(long timeout, TimeUnit unit)
public T    getNow(T valueIfAbsent)
public T    join()
```
getNow有点特殊，如果结果已经计算完则返回结果或者抛出异常，否则返回给定的valueIfAbsent值。
join返回计算的结果或者抛出一个unchecked异常(CompletionException)，它和get对抛出的异常的处理有些细微的区别，你可以运行下面的代码进行比较：
```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    int i = 1/0;
    return 100;
});
//future.join();
future.get();
```
#### 创建对象
CompletableFuture.completedFuture是一个静态辅助方法，用来返回一个已经计算好的CompletableFuture
```java
public static <U> CompletableFuture<U> completedFuture(U value)
```
而以下四个静态方法用来为一段异步执行的代码创建CompletableFuture对象：
```java
public static CompletableFuture<Void>   runAsync(Runnable runnable)
public static CompletableFuture<Void>   runAsync(Runnable runnable, Executor executor)
public static <U> CompletableFuture<U>  supplyAsync(Supplier<U> supplier)
public static <U> CompletableFuture<U>  supplyAsync(Supplier<U> supplier, Executor executor)
```
以Async结尾并且没有指定Executor的方法会使用 `ForkJoinPool.commonPool()` 作为它的线程池执行异步代码。

runAsync方法也好理解，它以Runnable函数式接口类型为参数，所以CompletableFuture的计算结果为空。

supplyAsync方法以Supplier<U>函数式接口类型为参数,CompletableFuture的计算结果类型为U。

#### 计算结果完成时的处理
当CompletableFuture的计算结果完成，或者抛出异常的时候，我们可以执行特定的Action。主要是下面的方法：
```java
public CompletableFuture<T> whenComplete(BiConsumer<? super T,? super Throwable> action)
public CompletableFuture<T> whenCompleteAsync(BiConsumer<? super T,? super Throwable> action)
public CompletableFuture<T> whenCompleteAsync(BiConsumer<? super T,? super Throwable> action, Executor executor)
public CompletableFuture<T> exceptionally(Function<Throwable,? extends T> fn)
public CompletableFuture<T> whenComplete(BiConsumer<? super T,? super Throwable> action)
public CompletableFuture<T> whenCompleteAsync(BiConsumer<? super T,? super Throwable> action)
public CompletableFuture<T> whenCompleteAsync(BiConsumer<? super T,? super Throwable> action, Executor executor)
public CompletableFuture<T>  exceptionally(Function<Throwable,? extends T> fn)
```
可以看到Action的类型是 `BiConsumer<? super T,? super Throwable>` ，它可以处理正常的计算结果，或者异常情况。

方法不以Async结尾，意味着Action使用相同的线程执行。

> 注意这几个方法都会返回CompletableFuture，当Action执行完毕后它的结果返回原始的CompletableFuture的计算结果或者返回异常。
  
#### 转换
CompletableFuture可以作为monad(单子)和functor。由于回调风格的实现，我们不必因为等待一个计算完成而阻塞着调用线程，而是告诉CompletableFuture当计算完成的时候请执行某个function。而且我们还可以将这些操作串联起来，或者将CompletableFuture组合起来。

```java
public <U> CompletableFuture<U>     thenApply(Function<? super T,? extends U> fn)
public <U> CompletableFuture<U>     thenApplyAsync(Function<? super T,? extends U> fn)
public <U> CompletableFuture<U>     thenApplyAsync(Function<? super T,? extends U> fn, Executor executor)
```
这一组函数的功能是当原来的CompletableFuture计算完后，将结果传递给函数fn，将fn的结果作为新的CompletableFuture计算结果。因此它的功能相当于将CompletableFuture<T>转换成CompletableFuture<U>。
使用例子如下：
```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    return 100;
});
CompletableFuture<String> f =  future.thenApplyAsync(i -> i * 10).thenApply(i -> i.toString());
System.out.println(f.get()); //"1000"
```
需要注意的是，这些转换并不是马上执行的，也不会阻塞，而是在前一个stage完成后继续执行。

它们与handle方法的区别在于handle方法会处理正常计算值和异常，因此它可以屏蔽异常，避免异常继续抛出。而thenApply方法只是用来处理正常值，因此一旦有异常就会抛出。

#### 纯消费(执行Action)
上面的方法是当计算完成的时候，会生成新的计算结果(thenApply, handle)，或者返回同样的计算结果whenComplete，CompletableFuture还提供了一种处理结果的方法，只对结果执行Action,而不返回新的计算值，因此计算值为Void:

```java
public CompletableFuture<Void>  thenAccept(Consumer<? super T> action)
public CompletableFuture<Void>  thenAcceptAsync(Consumer<? super T> action)
public CompletableFuture<Void>  thenAcceptAsync(Consumer<? super T> action, Executor executor)
```
例子：
```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    return 100;
});
CompletableFuture<Void> f =  future.thenAccept(System.out::println);
System.out.println(f.get());
```

thenAcceptBoth以及相关方法提供了类似的功能，当两个CompletionStage都正常完成计算的时候，就会执行提供的action，它用来组合另外一个异步的结果。
runAfterBoth是当两个CompletionStage都正常完成计算的时候,执行一个Runnable，这个Runnable并不使用计算的结果。
```java
public <U> CompletableFuture<Void> thenAcceptBoth(CompletionStage<? extends U> other, BiConsumer<? super T,? super U> action)
public <U> CompletableFuture<Void> thenAcceptBothAsync(CompletionStage<? extends U> other, BiConsumer<? super T,? super U> action)
public <U> CompletableFuture<Void> thenAcceptBothAsync(CompletionStage<? extends U> other, BiConsumer<? super T,? super U> action, Executor executor)
public     CompletableFuture<Void> runAfterBoth(CompletionStage<?> other,  Runnable action)
```
例子如下：
```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    return 100;
});
CompletableFuture<Void> f =  future.thenAcceptBoth(CompletableFuture.completedFuture(10), (x, y) -> System.out.println(x * y));
System.out.println(f.get());  // null
```
更彻底地，下面一组方法当计算完成的时候会执行一个Runnable,与thenAccept不同，Runnable并不使用CompletableFuture计算的结果。

```java
public CompletableFuture<Void> thenRun(Runnable action)
public CompletableFuture<Void> thenRunAsync(Runnable action)
public CompletableFuture<Void> thenRunAsync(Runnable action, Executor executor)
```
因此先前的CompletableFuture计算的结果被忽略了,这个方法返回CompletableFuture<Void>类型的对象。


#### 组合
```java
public <U> CompletableFuture<U> thenCompose(Function<? super T,? extends CompletionStage<U>> fn)
public <U> CompletableFuture<U> thenComposeAsync(Function<? super T,? extends CompletionStage<U>> fn)
public <U> CompletableFuture<U> thenComposeAsync(Function<? super T,? extends CompletionStage<U>> fn, Executor executor)
```
这一组方法接受一个Function作为参数，这个Function的输入是当前的CompletableFuture的计算结果值，
返回结果将是一个新的CompletableFuture，这个新的CompletableFuture会组合原来的CompletableFuture和函数返回的CompletableFuture。
因此它的功能类似:
> A +--> B +---> C

例子：
```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    return 100;
});
CompletableFuture<String> f =  future.thenCompose(i -> {
    return CompletableFuture.supplyAsync(() -> {
        return (i * 10) + "";
    });
});
System.out.println(f.get()); //1000

```
而下面的一组方法thenCombine用来复合另外一个CompletionStage的结果。它的功能类似：

A 
|
+------> B
+------> C
两个CompletionStage是并行执行的，它们之间并没有先后依赖顺序，other并不会等待先前的CompletableFuture执行完毕后再执行。
```java
public <U,V> CompletableFuture<V> thenCombine(CompletionStage<? extends U> other, BiFunction<? super T,? super U,? extends V> fn)
public <U,V> CompletableFuture<V> thenCombineAsync(CompletionStage<? extends U> other, BiFunction<? super T,? super U,? extends V> fn)
public <U,V> CompletableFuture<V> thenCombineAsync(CompletionStage<? extends U> other, BiFunction<? super T,? super U,? extends V> fn, Executor executor)
```
其实从功能上来讲,它们的功能更类似thenAcceptBoth，只不过thenAcceptBoth是纯消费，它的函数参数没有返回值，而thenCombine的函数参数fn有返回值。

```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    return 100;
});
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> {
    return "abc";
});
CompletableFuture<String> f =  future.thenCombine(future2, (x,y) -> y + "-" + x);
System.out.println(f.get()); //abc-100
```
#### Either
thenAcceptBoth和runAfterBoth是当两个CompletableFuture都计算完成，而我们下面要了解的方法是当任意一个CompletableFuture计算完成的时候就会执行。
```java
public CompletableFuture<Void>    acceptEither(CompletionStage<? extends T> other, Consumer<? super T> action)
public CompletableFuture<Void>    acceptEitherAsync(CompletionStage<? extends T> other, Consumer<? super T> action)
public CompletableFuture<Void>    acceptEitherAsync(CompletionStage<? extends T> other, Consumer<? super T> action, Executor executor)
public <U> CompletableFuture<U>     applyToEither(CompletionStage<? extends T> other, Function<? super T,U> fn)
public <U> CompletableFuture<U>     applyToEitherAsync(CompletionStage<? extends T> other, Function<? super T,U> fn)
public <U> CompletableFuture<U>     applyToEitherAsync(CompletionStage<? extends T> other, Function<? super T,U> fn, Executor executor)
```
acceptEither方法是当任意一个CompletionStage完成的时候，action这个消费者就会被执行。这个方法返回CompletableFuture<Void>

applyToEither方法是当任意一个CompletionStage完成的时候，fn会被执行，它的返回值会当作新的CompletableFuture<U>的计算结果。
#### 异常处理
如果在设置 CompletableFuture.complete(value)之前出现了异常，那么 get() 或其他回调函数像 whenComplete() 都会无限期的等待下去。
```java
public static void main(string[] args) throws ExecutionException, InterruptedException {
    CompletableFuture<Double> futurePrice = new CompletableFuture<>();
    new Thread(() -> {
        if(true) {
            throw new RuntimeExeption("");
        }
        futurePrice.complete(23.5);
    }).start();
 
    System.out.println(futurePrice.get());
}
```
java.lang.RuntimExeption(), 但是异常并不会在线程间传播，所以futurePrice.get()一直在等待。
办法一是调用get(timeout)时给定一个超时时间，如果指定时间内还没有获得结果则得到TimeoutException。另一种办法是要在线程中通过completeExceptionally(ex)来传播异常
```java
public static void main(String[] args) throws ExecutionException, InterruptedException {
    CompletableFuture<Double> futurePrice = new CompletableFuture<>();
    new Thread(() -> {
        try {
            if (true) {
                throw new RuntimeException("Something wrong");
            }
            futurePrice.complete(23.5);
        } catch (Exception ex) {
            futurePrice.completeExceptionally(ex); //捕获的异常还会由 ExecutionException 包裹一下
        }
    }).start();
 
     System.out.println(futurePrice.get());
}
```
这时候在futurePrice.get()马上就能收到java.util.concurrent.ExecutionException: java.lang.Exception: Something wrong 异常
#### 辅助方法
前面我们已经介绍了几个静态方法：completedFuture、runAsync、supplyAsync,下面介绍的这两个方法用来组合多个CompletableFuture。
```java
public static CompletableFuture<Void> allOf(CompletableFuture<?>... cfs)
public static CompletableFuture<Object> anyOf(CompletableFuture<?>... cfs)
```
allOf方法是当所有的CompletableFuture都执行完后执行计算。

anyOf方法是当任意一个CompletableFuture执行完后就会执行计算，计算的结果相同。

下面的代码运行结果有时是100，有时是"abc"。但是anyOf和applyToEither不同。anyOf接受任意多的CompletableFuture但是applyToEither
只是判断两个CompletableFuture，anyOf返回值的计算结果是参数中其中一个CompletableFuture的计算结果，applyToEither返回值的计算结果却是要经过fn
处理的。当然还有静态方法的区别，线程池的选择等。



### References
- [Java CompletableFuture 详解](https://colobu.com/2016/02/29/Java-CompletableFuture/) 
- [Java 8: Definitive guide to CompletableFuture](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwivnI-BwJ7LAhWpg4MKHRr8CB0QFggcMAA&url=http%3A%2F%2Fwww.nurkiewicz.com%2F2013%2F05%2Fjava-8-definitive-guide-to.html&usg=AFQjCNHxOcm4uRrqZGl1ognxfaTtmB5k5A&sig2=A5rXKfQuabGJMHXAhPUIgA&bvm=bv.115339255,d.eWE)
- [JDK CompletableFuture](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CompletableFuture.html)
- [JDK CompletionStage](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CompletionStage.html)

> 本文首次发布于 [S.L's Blog](http://elsef.com), 作者 [@stuartlau](http://github.com/stuartlau) ,
转载请保留原文链接.
