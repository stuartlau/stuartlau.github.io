---
layout:     post
title:      "理解Java中的Integer的实例化"
subtitle:   "Initialization Integer in Java"
date:       2019-11-10
author:     S.L
header-img: img/home-bg-o.jpg
catalog: true
tags:
    - Java
---
> Spring的IoC容器功能非常强大，负责Spring的Bean的创建和管理等功能。了解Spring Bean的生命周期对我们了解整个Spring框架会有很大的帮助。
>
> 本文主要介绍ApplicationContext和BeanFactory两种容器的Bean的生命周期。 


### Bean的生命周期
Bean 的生命周期由多个特定的生命阶段组成，每个生命阶段都开除了一扇门，允许外接对 Bean 施加控制。

在 Spring 中，我们可以从两个层面定义 Bean 的生命周期：第一个层面是 Bean 的作用范围；第二个层面是是实例化 Bean 时所经历的一系列阶段。

BeanFactory和ApplicationContext是Spring两种很重要的容器，前者提供了最基本的依赖注入的支持，而后者在继承前者的基础进行了功能的拓展，例如增加了事件传播，资源访问和国际化的消息访问等功能。
#### BeanFactory中Bean的生命周期
1. 当调用者通过 getBean(beanName) 向容器请求某一个 Bean 时，如果容器注册了 `InstantiationAwareBeanPostProcessor` 接口，
在实例化 Bean 之前，将调用接口的 postProcessBeforeInstantiation()方法；
2. 根据配置情况调用 Bean 构造函数或工厂方法实例化 Bean；
3. 如果容器注册了 `InstantiationAwareBeanPostProcessor` 接口，在实例化 Bean 之后，调用该接口的 
postProcessAfterInstantiation()方法，在这里可以对已经实例化的对象进行一些「梳妆打扮」；
4. 如果 Bean 配资了属性信息，容器在这一步着手将配置值设置到 Bean 对应的属性中，不过在设置每个属性之前将先调用 
`InstantiationAwareBeanPostProcessor` 接口的
postProcessPropertyValues()方法； 
5. 调用 Bean 的属性设置方法设置属性值；
6. 如果 Bean 实现了 `BeanNameAware` 接口，将调用 setBeanName()方法，将配置文件中该 Bean 对应的名称设置到 Bean 中；
7. 如果 Bean 实现了 `BeanFactoryAware` 接口，将调用 setBeanFactory()接口方法，将 BeanFactory 容器设置到 Bean 中；
8. 如果 BeanFactory 装配了 `BeanPostProcessor` 后处理器，将调用 postProcessBeforeInitialization(Object bean, 
String beanName)接口方法对 Bean 进行加工操作，一些常见的功能如AOP、动态代理等都是通过这个接口实现的；
9. 如果 Bean 实现了 `InitializingBean` 接口，将调用接口的 afterPropertiesSet()方法；
10. 如果在<bean>标签里设置了 init-method 属性则执行这个方法；
11. 如果 BeanFactory 装配了 `BeanPostProcessor` 后处理器，将调用 postProcessAfterInitialization(Object 
bean, String beanName)接口方法对 Bean 进行加工操作；
12. 如果设置scope=prototype，将 Bean 返回给调用者，不再负责其生命周期，如果是singleton类型，则放入 Spring IoC 容器的缓存池中，并将引用返回给调用者，
Spring 继续对这些 Bean 进行后续的生命管理；
13. 对于设置scope=singleton，当容器关闭时，将触发 Spring 对 Bean 的后续生命周期的管理工作，如果实现了 `DisposableBean` 
接口，则调用destroy()方法，在此处可以编写如资源释放、日志记录等工作；
14. 如果在<bean>标签中配置了 destroy-method 属性，则将执行这个方法，完成 Bean 资源的释放；

下面对这些关键点的特定方法进行一定的分类：
- Bean 自身的方法：如构造函数实例化 Bean，调用 Setter设置属性，以及通过 <bean> 标签设置init-method和destroy-method所指定的方法；
- Bean 级声明周期接口方法：如 BeanNameAware、BeanFactoryAware、InitializingBean、DisposableBean，这些接口由 Bean 类直接实现；
- 容器级生命周期接口方法：包括 InstantiationAwareBeanPostProcessor和BeanPostProcessor 两个接口，这些称之为后处理器，一般不由 Bean 
本身实现，它们独立于 Bean，实现类以容器附加装置的形式注册到 Spring 容器中并通过接口反射为 Spring 容器预先识别。这些后处理器在任何 Bean 创建的时候
都会发生作用，影响是全局性的。

> 如果喜欢解绑Spring，可以使用init-method替换实现InitializingBean接口，或者使用destroy-method替换实现DisposableBean接口。
>
> 甚至还可以使用@PostConstruct、@PreDestroy注解来完成相同的方法标记工作，它们是由InitDestroyAnnotationBeanPostProcessor后处理器实现的。

#### ApplicationContext中Bean的生命周期
Bean 在应用上下文中的生命周期和再 BeanFactory 中生命周期类似，不同的是，如果 Bean 实现了 ApplicationContextAware 接口，会增加一个调用该接口的
setApplicationContext()方法的步骤。
此外，如果配置文件中声明了工厂后处理器接口 BeanFactoryPostProcessor 的实现类，则应用上下文在装载配置文件之后初始化 Bean 实例之前将调用
这些 BeanFactoryPostProcessor 对配置信息进行加工处理，如 Spring 自带的后工厂处理器 
PropertyPlaceholderConfigurer、CustomEditorConfigurer等。

ApplicationContext 和 BeanFactory 另一个最大的不同之处在于：前者会利用 Java 反射机制自动识别出配置文件中定义的 
BeanPostProcessor、InstantiationAwareBeanPostProcessor和 BeanFactoryPostProcessor，并自动将它们注册到应用上下文中；
后者需要在代码中通过手动调用 addBeanPostProcessor()方法进行注册。

所以一般我们都是用 ApplicationContext，只需要在配置文件中配置对应的 <bean> 即可。

### References
- 《Spring 3.x——企业应用开发实战》，陈雄华、林开雄著


> 本文首次发布于 [S.L's Blog](http://elsef.com), 作者 [@stuartlau](http://github.com/stuartlau) ,
转载请保留原文链接.
