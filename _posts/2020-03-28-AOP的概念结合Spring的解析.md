---
layout:     post
title:      "AOP的概念结合Spring的解析"
subtitle:   "AOP"
date:       2020-03-28
author:     S.L
header-img: img/home-bg-o.jpg
catalog: true
tags:
    - Java
---
    
> AOP是编程中常用的一种方式，以Spring为例我们经常使用spring-aop组件和aspectJ的注解或者配置文件来完成对接口或类中的
某些方法的执行的拦截，本文对用到的一些概念术语进行解读，方便理解。

![](https://i.stack.imgur.com/J7Hrh.png)
### 概念
#### JoinPoint
> A joinpoint is a candidate point in the Program Execution of the application where an aspect can 
be plugged in. This point could be a method being called, an exception being thrown, or even a field 
being modified. These are the points where your aspect’s code can be inserted into the normal flow 
of your application to add new behavior.

注意JoinPoint并不一定只是方法的执行点，还可以是一个异常的抛出点或者一个属性的变更点，在这些变动上我们都可以进行拦截。

下面用一个餐馆的例子来比喻：
> Join points are the options on the menu and pointcuts are the items you select. A joinpoint is an 
opportunity within code for you to apply an aspect…just an opportunity. Once you take that 
opportunity and select one or more joinpoints and apply an aspect to them, you’ve got a pointcut.
  
`Joinpoint` 就是菜单上的选项，`Pointcut` 就是你选的菜。`Joinpoint` 只是你切面中可以切的那些方法，一旦你选择了要切哪些方法，
那就是 `Pointcut` 了。

也就是说，所有在你程序中可以被调用的方法都是 `JoinPoint` 。 使用 `Pointcut` 表达式，那些匹配了的方法，才叫 `Pointcut`。
所以你根本不用关心 `JoinPoint` 。

再通俗一点，比如你有10个方法，你只想切2个方法，那么那10个方法就是 `Joinpoint` ， 2个方法就是 `PointCut` 。

下面是spring-aop中对 `Jointpoint` 接口的定义：
```java
public interface Joinpoint {

	/**
	 * Proceed to the next interceptor in the chain.
	 * <p>The implementation and the semantics of this method depends
	 * on the actual joinpoint type (see the children interfaces).
	 * @return see the children interfaces' proceed definition
	 * @throws Throwable if the joinpoint throws an exception
	 */
	Object proceed() throws Throwable;

	/**
	 * Return the object that holds the current joinpoint's static part.
	 * <p>For instance, the target object for an invocation.
	 * @return the object (can be null if the accessible object is static)
	 */
	Object getThis();

	/**
	 * Return the static part of this joinpoint.
	 * <p>The static part is an accessible object on which a chain of
	 * interceptors are installed.
	 */
	AccessibleObject getStaticPart();

}

```
> This interface represents a generic runtime joinpoint (in the AOP terminology). A runtime joinpoint 
is an <i>event</i> that occurs on a static joinpoint (i.e. a location in a the program). For instance, 
an invocation is the runtime  joinpoint on a method (static joinpoint). The static part of a given 
joinpoint can be generically retrieved using the {@link #getStaticPart()} method.
>
> In the context of an interception framework, a runtime joinpoint is then the reification of an 
access to an accessible object (a method, a constructor, a field), i.e. the static part of the
joinpoint. It is passed to the interceptors that are installed on the static joinpoint.
 
注释里面有一个概念：static joinpoint，比如方法就是一种，可以通过 `getStaticPart` 方法获取一个 *joinpoint* 的
 *static part* 。

对于 `getThis` 方法来说需要注意的一点，如果它返回的是持有当前 *jointpoint* 的static part的对象，比如一个触发的目标对象，
如果是静态方法则返回null。

这里提到了 `Invocation` ，看一下它的接口定义：
```java
public interface Invocation extends Joinpoint {

	/**
	 * Get the arguments as an array object.
	 * It is possible to change element values within this
	 * array to change the arguments.
	 * @return the argument of the invocation
	 */
	Object[] getArguments();

}
```
> This interface represents an invocation in the program. An invocation is a joinpoint and can be 
intercepted by an interceptor.

`Invocation` 即「调用」，它也是一种 *jointpoint* ，主要用于 `Interceptor` 拦截器拦截的时候使用。

它的接口 `getArgument` 会返回当前被执行的方法的入参，以数组的形式返回。

一种比较常见的子接口是 `MethodInvocation` ：
```java
public interface MethodInvocation extends Invocation {

	/**
	 * Get the method being called.
	 * <p>This method is a friendly implementation of the
	 * {@link Joinpoint#getStaticPart()} method (same result).
	 * @return the method being called
	 */
	Method getMethod();

}
```
> Description of an invocation to a method, given to an interceptor upon method-call.
A method invocation is a joinpoint and can be intercepted by a method interceptor.

可以看到一个 *method invocation* 就是一个 *jointpoint*，即方法调用类型的 *joinpoint* ，它会拦截器拦截，同时它的
方法 `getMethod` 返回的和 `Jointpoint` 的方法 `getStaticPart` 的返回结果是一样的，都是当前被执行的方法。

关于拦截器 `Interceptor` 下面讲 `Advice` 的时候会再详细介绍。
#### Pointcut
> A pointcut defines at what joinpoints, the associated Advice should be applied. 
Advice can be applied at any joinpoint supported by the AOP framework. Of course, 
you don’t want to apply all of your aspects at all of the possible joinpoints. 
Pointcuts allow you to specify where you want your advice to be applied. 
Often you specify these pointcuts using explicit class and method names or 
through regular expressions that define matching class and method name patterns. 
Some AOP frameworks allow you to create dynamic pointcuts that determine whether 
to apply advice based on runtime decisions, such as the value of method parameters.

区别如下：
> Joinpoint - Potential places to apply/run the advice code.
> 
> Pointcut - actual chosen joinpoints for executing the advice.

spring-aop中的 `Pointcut` 接口定义如下：
```java
public interface Pointcut {

	/**
	 * Return the ClassFilter for this pointcut.
	 * @return the ClassFilter (never {@code null})
	 */
	ClassFilter getClassFilter();

	/**
	 * Return the MethodMatcher for this pointcut.
	 * @return the MethodMatcher (never {@code null})
	 */
	MethodMatcher getMethodMatcher();


	/**
	 * Canonical Pointcut instance that always matches.
	 */
	Pointcut TRUE = TruePointcut.INSTANCE;

}
```
它需要提供 `MethodMatcher` 实现类和 `ClassFilter` 实现类分别用于匹配方法和类，二者要同时满足才会被增强，如我想拦截
所有Grpc服务类的非 *Object* 方法，或者带有某个类注解的所有方法等。
#### Advice
> This is an object which includes API invocations to the system wide concerns 
representing the action to perform at a joinpoint specified by a point.

说白了， *advice* 就是你作用到 *pointcut* 上的方式，如可以使用Before, After 或者Around等方式。

spring-aop中的定义如下：
```java
/**
 * Tag interface for Advice. Implementations can be any type
 * of advice, such as Interceptors.
 */
public interface Advice {

}
```
是的，一个空的接口定义，只是一个 `Tag interface` ，实现类可以是任何的 *advice* ，比如拦截器 `Interceptor` 也是一种。

基于该接口衍生出了很多子接口如： `MethodBeforeAdvice` 、 `AfterReturningAdvice` 、 `ThrowsAdvice` 等。

#### Interceptor
我们来看一下一种常见的 `Advice` 拦截器 `Interceptor` 的定义：
```java
public interface Interceptor extends Advice {

}
```
这是一个通用的接口，一般不会直接使用而是使用它的一些子接口（如MethodInterceptor），文档中对它的解释重点如下：
> A generic interceptor can intercept runtime events that occur within a base program. Those 
events are materialized by (reified in) joinpoints. Runtime joinpoints can be invocations, field
 access, exceptions
 
可以看到它是用来拦截运行时程序中的事件event的，这些事件以 *jointpoint* 的「物化形式」存在，比如调用（Invocations）、
属性访问（Field Access）和异常（Exceptions）。

看一下我们常用的方法拦截器 `MethodInterceptor` 接口的定义：
```java
@FunctionalInterface
public interface MethodInterceptor extends Interceptor {

	/**
	 * Implement this method to perform extra treatments before and
	 * after the invocation. Polite implementations would certainly
	 * like to invoke {@link Joinpoint#proceed()}.
	 * @param invocation the method invocation joinpoint
	 * @return the result of the call to {@link Joinpoint#proceed()};
	 * might be intercepted by the interceptor
	 * @throws Throwable if the interceptors or the target object
	 * throws an exception
	 */
	Object invoke(MethodInvocation invocation) throws Throwable;

}
```
可以看到它本质上是抽象了对拦截到的「方法调用」的处理接口，入参是 `MethodInvocation` ，一般在执行 `Jointpoint#proceed()` 
之前和之后进行处理，返回结果可以是方法的返回值或hack后的返回值。
#### Advisor
*advisor* 就是作用在具体对象上的 *pointcut* 和 *advice* ，把 *pointcut* 和 *advice* 合起来就是 *advisor* 。
比如切到哪个具体方法上面，是使用的Before、After还是Around，这个就叫 *advisor* 。

看一下spring-aop中的 `Advisor` 接口的定义：
```java
/**
 * Base interface holding AOP <b>advice</b> (action to take at a joinpoint)
 * and a filter determining the applicability of the advice (such as
 * a pointcut). <i>This interface is not for use by Spring users, but to
 * allow for commonality in support for different types of advice.</i>
 *
 * <p>Spring AOP is based around <b>around advice</b> delivered via method
 * <b>interception</b>, compliant with the AOP Alliance interception API.
 * The Advisor interface allows support for different types of advice,
 * such as <b>before</b> and <b>after</b> advice, which need not be
 * implemented using interception.
 *
 * @author Rod Johnson
 * @author Juergen Hoeller
 */
public interface Advisor {

	Advice EMPTY_ADVICE = new Advice() {};


	/**
	 * Return the advice part of this aspect. An advice may be an
	 * interceptor, a before advice, a throws advice, etc.
	 * @return the advice that should apply if the pointcut matches
	 */
	Advice getAdvice();

	boolean isPerInstance();

}
```
> Base interface holding AOP <b>advice</b> (action to take at a joinpoint) and a filter determining 
the applicability of the advice (such as a pointcut). <i>This interface is not for use by Spring 
users, but to allow for commonality in support for different types of advice.
>
> Spring AOP is based around <b>around advice</b> delivered via method <b>interception</b>, 
compliant with the AOP Alliance interception API.

它有两个接口需要实现：
- *getAdvice* ，需要提供一个 `Advice` 的实现，默认有一个空实现 *EMPTY_ADVICE*
- *isPerInstance* ，是否是每个实例生成一个还是统一用一个

更通用的接口 `PointcutAdvisor` 定义如下：
```java
public interface PointcutAdvisor extends Advisor {

	/**
	 * Get the Pointcut that drives this advisor.
	 */
	Pointcut getPointcut();

}
```
> Superinterface for all Advisors that are driven by a pointcut. This covers nearly all advisors 
except introduction advisors, for which method-level matching doesn't apply.

它提供一个接口返回一个 `Pointcut` 对象，这个接口有也是通过 *pointcut* 来驱动 *advisor* 的通用接口。一般我们实现
这个接口就可以了。比如，我们可以通过实现 `getPointcut` 方法返回一个只 `PointCut` 的实现类，它的 `ClassFilter` 
和 `MethodMatcher` 实现的功能是： 对Grpc服务类的自有接口进行拦截的。 然后通过实现 `getAdvice` 方法返回一个 
`MethodInteceptor` 的实现类，默认对执行的方法通过Around的方式进行增强。

### References
- https://stackoverflow.com/questions/15447397/spring-aop-whats-the-difference-between-joinpoint-and-pointcut

> 本文首次发布于 [S.L's Blog](http://elsef.com), 作者 [@stuartlau](http://github.com/stuartlau) ,
转载请保留原文链接.
