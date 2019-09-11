---
layout:     post
title:      "Java8函数式编程之Reduction"
subtitle:   "Reduction in Java8"
date:       2019-09-11
author:     SL
header-img: img/post-bg-universe.jpg
catalog: true
tags:
    - Algorithm
---
    

> Java8中引入了函数式计算以及Lambda和Stream等特性，其中的流式计算引入了收集器、组合器等规约操作用到概念，非常值得我们好好学习。
>
> 本文以「规约」为线索，先从Stream的reduce方法说起，然后延展到collect方法，以及Collectors中的groupingBy等方法。

### Stream#reduce()

`Stream` 带有一个 `reduce` 方法，通过该方法我们可以实现 `count` 、 `max` 、`min` 、 `sum` 等功能，非常强大。
规约操作可以将流的所有元素组合成一个结果，该方法有三种重载版本。

#### 1. 一个参数

> Optional<T> reduce(BinaryOperator<T> accumulator)

该方法无初始值，所以返回值使用 `Optional` 表示结果可能不存在。
使用 `Java` 代码来表述如下：

```java
T result = null; 
if (a == null) return result;
T identity = a[0];
result = identity;
for (int i = 1; i < n; i++) {
   result = accumulator.apply(result, a[i]);  
}
return result;  
```

这里的 `identity` 其实就是第一个元素，整体计算次数为 `n - 1` 。计算的顺序为，a[0]与a[1]进行二合运算，结果与a[2]做二合运算，一直到最后与a[n-1]做二合运算。

#### 2. 两个参数

> T reduce(T identity, BinaryOperator<T> accumulator)

`identity`：循环计算的初始值
`accumulator`：计算的累加器，其方法签名为`apply(T t,U u)`，在该 `reduce` 方法中第一个参数`t`为上次该函数计算的返回值，第二个参数`u`为`Stream`中的元素，这个函数把这两个值计算`apply`，得到的和会被赋值给下次执行这个方法的第一个参数。

使用`Java`代码来表述如下：

```java
T result = identity; 
for (int i = 0; i < n; i++) {
   result = accumulator.apply(result, a[i]);  
}
return result; 
```

注意区分与一个参数的 `reduce` 方法的不同：它多了一个初始化的值，因此计算的顺序是`identity` 与a[0]进行二合运算，结果与a[1]再进行二合运算...，最终与a[n-1]进行二合运算，一共计算 `n` 次。

#### 3. 三个参数

> \<U\> U reduce(U identity, BiFunction<U,? super T,U> accumulator, BinaryOperator<U> combiner)

- supplier：一个能创造目标类型实例的方法
- accumulator：一个将当元素添加到目标中的方法
- combiner：一个将中间状态的多个结果整合到一起的方法（并发的时候会用到）

乍一看与两个参数的 `reduce` 方法几乎一致，但是 `accumulator` 的类型变成了 `BiFunction` 而不是 `BinaryOperator` ，并且还多了一个 `combiner` 参数，而它的类型是第二个方法里 `accumulator` 参数的类型—— `BinaryOperator` 。
其实`BinaryOperator`接口是实现了`BiFunction`接口的，定义如下：

> public interface BinaryOperator<T> extends BiFunction<T, T ,T>

也就是说 `BiFunction` 的三个参数类型可以是一样的也可以完全不同，而 `BinaryOperator` 直接限定了三个参数类型必须相同。

OK，我们都知道`accumulator`是实现「累加」操作的，那么`combiner`的作用是什么呢？
如果你用 `串行流` 的方式来调用这个方法的话你会发现 `combiner` 并没有被调用，所有计算都在 `accumulator` 中执行，并返回结果。如下面的实例代码：

```java
Integer ageSum = persons
    .stream()
    .reduce(0,
        (sum, p) -> {
            System.out.format("accumulator: sum=%s; person=%s\n", sum, p);
            return sum += p.age;
        },
        (sum1, sum2) -> {
            System.out.format("combiner: sum1=%s; sum2=%s\n", sum1, sum2);
            return sum1 + sum2;
        });

// accumulator: sum=0; person=Max
// accumulator: sum=18; person=Peter
// accumulator: sum=41; person=Pamela
// accumulator: sum=64; person=David
```

其实这个组合器是在 `并行流` 的执行方式时被调用的，因为累加器会被并行调用，所以需要组合器用于计算各个子累加值的总和。

### Stream#collect()

该方法是负责处理可变式规约——`Mutable Reduction`的，`JavaDoc`中该定义解释如下：

> A mutable reduction operation accumulates input elements into a mutable result container,
>
> such as a Collection or StringBuilder, as it processes the elements in the stream.
>
> If we wanted to take a stream of strings and concatenate them into a single long string, we
>
> could achieve this with ordinary reduction:
>
> ```
> String concatenated = strings.reduce("", String::concat)
> ```
>
> We would get the desired result, and it would even work in parallel. However, we might not be
>
> happy about the performance! Such an implementation would do a great deal of string copying, and
>
> the run time would be O(n^2) in the number of characters. A more performant approach would be
>
> to accumulate the results into a StringBuilder, which is a mutable container for accumulating
>
> strings. We can use the same technique to parallelize mutable reduction as we do with ordinary reduction.

里面提到了一种实现拼接字符串的方法，它采用了每次创建一个新的字符串的方式（String::concat方法每次生成一个新的字符串），这样非常浪费内存空间。而`collect`方法本质上是变更了数据的状态，而不是对它进行了替换，这也就是为什么要求存储变量的容器是`a mutable result container`。
用伪代码标识上述规约过程如下，注意`result`是一个状态可变的对象，即`mutable`的：

```java
R result = supplier.get();
          for (T element : this stream)
              accumulator.accept(result, element);
          return result;
```

它的三参数方法声明如下：   

> \<R\> R collect(Supplier<R> supplier, BiConsumer<R,? super T> accumulator, BiConsumer<R,R> combiner)

- supplier：一个能创造目标类型实例的方法
- accumulator：一个将当元素添加到目标中的方法
- combiner：一个将中间状态的多个结果整合到一起的方法（并发的时候会用到）

所以对于字符串拼接来说，可以用下面的代码实现：

```java
String concat = stringStream.collect(StringBuilder::new, StringBuilder::append,
                                               StringBuilder::append).toString();
```

再举一个例子：

```java
Stream<Integer> stream = Stream.of(1, 2, 3, 4).filter(p -> p > 2);
List<Integer> result = stream.collect(() -> new ArrayList<>(), (list, item) -> list.add(item), (one, two) -> one.addAll(two));
/* 或者使用方法引用 */
result = stream.collect(ArrayList::new, List::add, List::addAll);
```

这个例子即为过滤大于2的元素，将剩余结果收集到一个新的list中。

- 第一个方法即`supplier`生成一个新的ArrayList；
- 第二个方法即`accumulator`中第一个参数是前面生成的ArrayList对象，第二个参数是stream中包含的元素，方法体就是把stream中的元素加入ArrayList对象中。第二个方法被反复调用直到原stream的元素被消费完毕；
- 第三个方法即`combiner`也是接受两个参数，这两个都是ArrayList类型的，方法体就是把第二个ArrayList全部加入到第一个中；

该方法的参数较多，代码有点繁琐，其实 `collect` 还有另外一个重载方法:

> <R, A> R collect(Collector<? super T, A, R> collector)

里面只有一个参数 `Collector` ，它是一个接口，看过它的定义就知道它暴露了几个方法，其中最重要的几个声明如下：

```java
    /**
     * A function that creates and returns a new mutable result container.
     *
     * @return a function which returns a new, mutable result container
     */
    Supplier<A> supplier();

    /**
     * A function that folds a value into a mutable result container.
     *
     * @return a function which folds a value into a mutable result container
     */
    BiConsumer<A, T> accumulator();

    /**
     * A function that accepts two partial results and merges them.  The
     * combiner function may fold state from one argument into the other and
     * return that, or may return a new result container.
     *
     * @return a function which combines two partial results into a combined
     * result
     */
    BinaryOperator<A> combiner();
```

可以看到其实它的内部三个方法跟`collect`三个参数版本的中的三个参数： `supplier` 、 `accumulator` 、 `combiner` 是一一对应的。
那么上面代码就可以变成下面这种写法：

> List<Integer> list = Stream.of(1, 2, 3, 4).filter(p -> p > 2).collect(Collectors.toList());

该方法默认返回一个 `Collector` ，让我们来看一下`toList` 方法是如何实现这个接口的：

```java
public static <T>
    Collector<T, ?, List<T>> toList() {
        return new CollectorImpl<>((Supplier<List<T>>) ArrayList::new, List::add,
                                   (left, right) -> { left.addAll(right); return left; },
                                   CH_ID);
    }
```

- `supplier`：生成了一个可变集合 new ArrayList()
- `accumulator`：将每个元素加入到可变集合中 List::add
- `combiner`：将规约中产生的子集合进行合并，主要是并行流中会使用

### 分组和分片

对具有相同特性的值进行分组是一个很常见的任务，Collectors提供了一个 `groupingBy` 方法，方法签名为：

> \<T,K,A,D\> Collector<T,?,Map<K,D>> groupingBy(Function<? super T,? extends K> classifier, Collector<? super T,A,D> downstream)

- `classifier` ：分类器是一个`Function`，负责将数据按照某一规则进行分类并生成对应的 `Key`
- `downstream` ：下行流收集器是一个`Collector`，对分类后的数据集进行收集 `reduce` 操作

假如要根据年龄来分组：

> Map<Integer, List<Person>> peopleByAge = people.stream().collect(groupingBy(p -> p.age, toList()));

假如我想要根据年龄分组，年龄对应的键值List存储的为 `Person` 的姓名:

> Map<Integer, List<String>> peopleByAge = people.stream().collect(groupingBy(p -> p.age, mapping((Person p) -> p.name, toList())));

 `mapping` 方法即为对各 `组` 进行 `投影` 操作，和 `Stream` 的 `map` 方法基本一致。

注意到方法的返回值其实也是一个`Collector`，也就是 `groupingBy` 的第二个参数一样，这说明我们可以使用多级的分组：

```java
Map<String, Map<String, List<Person>>> peopleByStateAndCity
              = personStream.collect(groupingBy(Person::getState, 		groupingBy(Person::getCity)));
            
```

假如要根据姓名分组，获取每个姓名下人的年龄总和：

```java
Map<String, Integer> sumAgeByName = people.stream().collect(groupingBy(p -> p.name, reducing(0, (Person p) -> p.age, Integer::sum)));
/* 或者使用summingInt方法 */
sumAgeByName = people.stream().collect(groupingBy(p -> p.name, summingInt((Person p) -> p.age)));

```

这里的`reducing` 方法是`Collectors` 类的，和我们上面介绍的 `Stream` 的 `reduce` 方法在三个参数定义上有些不同：

> Collector<T, ?, U> reducing(U identity, Function<? super T, ? extends U> mapper, BinaryOperator<U> op) {

`identity`：循环计算的初始值
`mapper`：类型转换器，将参数T转换为U类型，当然这两个可以一样
`op`：用于做 `reduce` 操作的 `BinaryOperator` 变量

这个方法在「多维度」的规约计算时很有用，比如`groupingBy` 或 `partitionBy`，在对一般的`Stream`进行规约时，直接用它自带的 `reduce` 方法即可，以下摘自 `JavaDoc` ：

> The reducing() collectors are most useful when used in a multi-level reduction, downstream of groupingBy or partitioningBy.
>
> To perform a simple reduction on a stream, use Stream.reduce(BinaryOperator) instead.
>
> For example, given a stream of Person, to calculate tallest person in each city:
>
> ```
>     Comparator<Person> byHeight = Comparator.comparing(Person::getHeight);
> 
>     Map<City, Person> tallestByCity
> 
>         = people.stream().collect(groupingBy(Person::getCity, reducing(BinaryOperator.maxBy(byHeight))));
> ```

### References

- https://blog.csdn.net/icarusliu/article/details/79504602
- https://my.oschina.net/voole/blog/1475737

> 本文首次发布于 [ElseF's Blog](http://elsef.com), 作者 [@stuartlau](http://github.com/stuartlau) ,
> 转载请保留原文链接.
