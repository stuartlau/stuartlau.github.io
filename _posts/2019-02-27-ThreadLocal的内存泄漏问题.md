---
layout:     post
title:      "ThreadLocal和内存泄漏问题"
subtitle:   "When ThreadLocal has OOM Issue"
date:       2019-02-27
author:     SL
header-img: img/post-bg-universe.jpg
catalog: true
tags:
    - Java
---
    
> 本文说明当使用`Thread`和`ThreadLocal`的方式不当的时候，可能会导致内存泄漏问题，并提供使用`ThreadLocal`的最佳方式。

`ThreadLocal`通过采用「以空间换时间」的方式避免了并发中使用锁来控制多线程对共享变量的操作，使用线程「本地」变量的方式让多线程中的并发数据访问变得更加简单。
但是如果对ThreadLocal使用不当则会造成内存泄漏问题，本文主要分析内存泄漏出现的场景以及正确的使用`ThreadLocal`的方式。

## ThreadLocal基础

每个`Thread`实例都含有一个`ThreadLocal.ThreadLocalMap`变量`threadLocals`，注意该类定义在`ThreadLocal`类中，访问权限为`package 
private`，即操作`ThreadLocal`内的数据结构（`ThreadLocalMap`）都在`ThreadLocal`类中定义，但是获取对应的`ThreadLocalMap
`却需要通过`Thread`来获取，因为是绑定在线程上的。

ThreadLocalMap保存了它所属于的线程的一些数据，什么数据呢，当前线程执行过的ThreadLocal对象的初始化方法和设置值的方法。
举个例子，如有8个ThreadLocal对象，存储类型分别为Java的8
种基本类型的包装类，一个线程的初始化`ThreadLocal`操作中都会被该线程生成一个默认的值为0的对应类型的数据，所以该线程的`threadLocals`变量中存储了这8个`ThreadLocal`
对象和该线程存储的*value*，我们称之为`local value`。

```java
    /* ThreadLocal values pertaining to this thread. This map is maintained by the ThreadLocal 
    class. */
    ThreadLocal.ThreadLocalMap threadLocals = null;
```

ThreadLocalMap的JavaDoc如下：

> ThreadLocalMap is a customized hash map suitable only for maintaining thread local values. 
> No operations are exported maintaining thread local values. No operations are exported
> outside of the ThreadLocal class. The class is package private to allow declaration of 
> fields in class Thread.  To help deal with very large and long-lived usages, the hash 
> table entries use WeakReferences for keys. However, since reference queues are not
> used, stale entries are guaranteed to be removed only when the table starts running 
> out of space.

默认table entries使用`WeakReference`作为key，但是由于没有使用`ReferenceQueue`参数初始化key，所以及时JVM回收了对应的key
的引用的`ThreadLocal`对象我们也无法得知并做一些清除工作，这里就埋下一个隐患给我们。

```java
    static class ThreadLocalMap {
        /**
         * The initial capacity -- MUST be a power of two.
         */
        private static final int INITIAL_CAPACITY = 16;

        /**
         * The table, resized as necessary.
         * table.length MUST always be a power of two.
         */
        private Entry[] table;

        /**
         * The number of entries in the table.
         */
        private int size = 0;

        /**
         * The next size value at which to resize.
         */
        private int threshold; // Default to 0        
        ......
    }
```
可知它其实并不是一个`Map`的实现类，而是通过`Entry`来实现的key和value的映射关系，并用数组进行保存多个`Entry`。
`ThreadLocalMap`对应的构造函数如下：
```java
    /**
     * Construct a new map initially containing (firstKey, firstValue).
     * ThreadLocalMaps are constructed lazily, so we only create
     * one when we have at least one entry to put in it.
     */
    ThreadLocalMap(ThreadLocal<?> firstKey, Object firstValue) {
        table = new Entry[INITIAL_CAPACITY];
        int i = firstKey.threadLocalHashCode & (INITIAL_CAPACITY - 1);
        table[i] = new Entry(firstKey, firstValue);
        size = 1;
        setThreshold(INITIAL_CAPACITY);
    }
```
可知每个`Entry`持有了key为`ThreadLocal`对象实例，value为具体的ThreadLocal<T>泛型T的实例对象。初始化的数组大小为16。

> The entries in this hash map extend WeakReference, using its main ref field as the key (which 
> is always a ThreadLocal object). Note that null keys (i.e. entry.get() == null) mean that 
> the key is no longer referenced, so the entry can be expunged from table.  Such entries 
> are referred to as "stale entries" in the code that follows.
       
```java
    static class Entry extends WeakReference<ThreadLocal<?>> {
        /** The value associated with this ThreadLocal. */
        Object value;

        Entry(ThreadLocal<?> k, Object v) {
            super(k);
            value = v;
        }
    }
```
注意到Entry继承了`WeakReference`，而弱引用本身在GC触发时会被回收，所以key可能会变为`null`，即被回收掉了，但是value是一个强引用。该Entry在table
数组中也不会被垃圾回收自动触发「缩容」删除掉，不过`ThreadLocalMap`为我们提供了很多`expunge`机制，但前提是这个机制「需要显式触发」，这里也就是容易出现内存泄漏的地方！

```java
    /**
     * Expunge a stale entry by rehashing any possibly colliding entries
     * 
     * lying between staleSlot and the next null slot.  This also expunges
     * 
     * any other stale entries encountered before the trailing null.  See
     * 
     * Knuth, Section 6.4
     *
     * @param staleSlot index of slot known to have null key
     * 
     * @return the index of the next null slot after staleSlot
     * 
     * (all between staleSlot and this slot will have been checked
     * 
     * for expunging).
     */
    private int expungeStaleEntry(int staleSlot) {
        Entry[] tab = table;
        int len = tab.length;

        // expunge entry at staleSlot
        tab[staleSlot].value = null; // 清除对应的value的值
        tab[staleSlot] = null; // 清除ThreadLocalMap中的Entry[]中对应i位置的Entry，回收内存
        size--; // 数组缩容

        // Rehash until we encounter null
        Entry e;
        int i;
        for (i = nextIndex(staleSlot, len);
             (e = tab[i]) != null;
             i = nextIndex(i, len)) {
            ThreadLocal<?> k = e.get();
            if (k == null) { // 如果k已经被回收，即ThreadLocal对象被回收
                e.value = null; // 清除对应的value的值
                tab[i] = null; // 清除ThreadLocalMap中的Entry[]中对应i位置的Entry，回收内存
                size--; // 数组缩容
            } else {
                int h = k.threadLocalHashCode & (len - 1);
                if (h != i) {
                    tab[i] = null;

                    // Unlike Knuth 6.4 Algorithm R, we must scan until
                    // null because multiple entries could have been stale.
                    while (tab[h] != null)
                        h = nextIndex(h, len);
                    tab[h] = e;
                }
            }
        }
        return i;
    }
    
    /**
     * Expunge all stale entries in the table.
     */
    private void expungeStaleEntries() {
        Entry[] tab = table;
        int len = tab.length;
        for (int j = 0; j < len; j++) {
            Entry e = tab[j];
            if (e != null && e.get() == null) // 清理Entry不存在或对应的key已经过期的数据
                expungeStaleEntry(j);
        }
    }
```
很幸运的是，这个方法在内部很多方法实现里都会被调用到，比如：ThreadLocal#remove(), ThreadLocal#set()
。所以当我们显式调用这些方法的时候内部会自动帮我们清理那些已经被垃圾回收的key对应的Entry。
来看一下ThreadLocalMap的set()的实现：
```java
    /**
     * Set the value associated with key.
     *
     * @param key the thread local object
     * @param value the value to be set
     */
    private void set(ThreadLocal<?> key, Object value) {

        // We don't use a fast path as with get() because it is at
        // least as common to use set() to create new entries as
        // it is to replace existing ones, in which case, a fast
        // path would fail more often than not.

        Entry[] tab = table;
        int len = tab.length;
        int i = key.threadLocalHashCode & (len-1);

        for (Entry e = tab[i];
             e != null;
             e = tab[i = nextIndex(i, len)]) {
            ThreadLocal<?> k = e.get();

            if (k == key) { // 更新value
                e.value = value;
                return;
            }

            if (k == null) { // 对应位置上的老的ThreadLocal对象已经被回收，替换为新的key
                replaceStaleEntry(key, value, i);
                return;
            }
        }
        // 如果当前的Entry[]中不存在对应的ThreadLocal的数据，则实例化一个新的Entry并触发扩容
        // 如果超过阈值会触发rehash，内部会调用
        tab[i] = new Entry(key, value);
        int sz = ++size;
        if (!cleanSomeSlots(i, sz) && sz >= threshold)
            rehash();
    }
    
    /**
     * Re-pack and/or re-size the table. First scan the entire
     * table removing stale entries. If this doesn't sufficiently
     * shrink the size of the table, double the table size.
     */
    private void rehash() {
        expungeStaleEntries();

        // Use lower threshold for doubling to avoid hysteresis
        if (size >= threshold - threshold / 4)
            resize();
    }
```
再来看一下ThreadLocal是如何调用它的：
```java
    /**
     * Sets the current thread's copy of this thread-local variable
     * to the specified value.  Most subclasses will have no need to
     * override this method, relying solely on the {@link #initialValue}
     * method to set the values of thread-locals.
     *
     * @param value the value to be stored in the current thread's copy of
     *        this thread-local.
     */
    public void set(T value) {
        Thread t = Thread.currentThread();
        ThreadLocalMap map = getMap(t);
        if (map != null)
            map.set(this, value);
        else
            createMap(t, value);
    }
    
    /**
     * Get the map associated with a ThreadLocal. Overridden in
     * InheritableThreadLocal.
     *
     * @param  t the current thread
     * @return the map
     */
    ThreadLocalMap getMap(Thread t) {
        return t.threadLocals;
    }
    
    /**
     * Create the map associated with a ThreadLocal. Overridden in
     * InheritableThreadLocal.
     *
     * @param t the current thread
     * @param firstValue value for the initial entry of the map
     */
    void createMap(Thread t, T firstValue) {
        t.threadLocals = new ThreadLocalMap(this, firstValue);
    }
```
通过获取当前线程的`threadLocals`变量来获取它的`ThreadLocalMap`实例，进而调用它的`set()`进行数据的设置。

## 在什么情况下会导致内存泄漏？
正如上面介绍的，因为`WeakReference`类型key被垃圾回收，但其对应的`Entry`仍然在`table`中保留，如果没有及时清理`table
`中的过期数据，并且对应的线程是线程池里的一个long-live线程，则可能会造成该线程内持有的过期`Entry`不能及时回收造成内存泄漏。
但是这个过程可能比较短暂，因为一旦该线程操作了其他ThreadLocal实例后，就会触发`expunge`机制对`threadLocals`进行清理。
所以下面的代码不会造成内存泄漏：
```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
 
public class ThreadLocalLeakTest {
 
    public static void main(String[] args) {
        // 如果控制线程池的大小为50，不会导致内存溢出
        testWithThreadPool(50);
        // 也不会导致内存泄露
        testWithThread();
    }
 
    static class TestTask implements Runnable {
 
        public void run() {
            ThreadLocal tl = new ThreadLocal();
            // 确保threadLocal为局部对象,在退出run方法之后，没有任何强引用，可以被垃圾回收
            tl.set(allocateMem());
        }
    }
 
    public static void testWithThreadPool(int poolSize) {
        ExecutorService service = Executors.newFixedThreadPool(poolSize);
        while (true) {
            try {
                Thread.sleep(100);
                service.execute(new TestTask());
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
 
    public static void testWithThread() {
 
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
 
        }
        new Thread(new TestTask()).start();
 
    }
 
    public static final byte[] allocateMem() {
        // 这里分配一个1M的对象
        byte[] b = new byte[1024 * 1024 * 1];
        return b;
    }
 
}
```

## 最坏的case
当前线程是通过线程池进行维护的，属于核心线程一旦被启动不会被回收，并且它的`threadLocals`中存有了大量的局部变量的`ThreadLocal`
的实例，并且这些实例都已经失效了。此时该线程不再有操作任何ThreadLocal实例（局部或静态类型）的代码要执行，所以`threadLocals`内的数据不会被释放。
同时，没有被释放的`Entry`的value的类是通过一个自定义的`ClassLoader`
加载的，由于该类实例无法被及时回收，并且由于该类实例也强引用了加载它的自定义`ClassLoader`，导致`ClassLoader`无法卸载进而导致其无法卸载其加载的所有`Class`实例。

如果不是使用线程池维护的线程而是通过手动new的`Thread`则不会有这种问题，原因是线程的生命周期随着`run`方法的结束就结束了，GC会帮我们回收该thread
引用的内存，包括堆栈信息和ThreadLocalMap中的内容。

当线程退出时会执行Thread的exit()方法：
```java
private void exit() {
    if (group != null) {
        group.threadTerminated(this);
        group = null;
    }
    /* Aggressively null out all reference fields: see bug 4006245 */
    target = null;
    /* Speed the release of some of these resources */
    threadLocals = null;
    inheritableThreadLocals = null;
    inheritedAccessControlContext = null;
    blocker = null;
    uncaughtExceptionHandler = null;
}
```
从源码可以看出当线程结束时，会令threadLocals=null，也就意味着GC的时候就可以将threadLocalMap进行垃圾回收，换句话说threadLocalMap生命周期实际上thread的生命周期相同。

## 正确的使用方式
- 尽量使用`static`的`ThreadLocal`
- 不要一次性初始化大量的、局部`ThreadLocal`变量
- 业务（线程）再使用完毕ThreadLocal后要及时调用`remove()`方法及时释放`threadLocals`中的内存资源
- 或者（线程）每次使用前都`set()`也是一样可以达到及时清理`stale`的`Entry`的效果的

## 为什么使用弱引用？
从文章开头通过ThreadLocal，ThreadLocalMap和Entry的引用关系看起来`ThreadLocal`存在内存泄漏的问题似乎是因为`ThreadLocal`实例是被
是被弱引用修饰的。那为什么要使用弱引用呢？

> 如果使用强引用

假设`ThreadLocal`中`Entry`里使用的是强引用到ThreadLocal实例，在业务代码中执行threadLocalInstance=null操作，以清理掉threadLocalInstance
的目的，但是因为threadLocalMap
的Entry强引用threadLocalInstance，因此在GC的时候进行可达性分析，threadLocalInstance依然可达，对threadLocalInstance
并不会进行垃圾回收，这样就无法真正达到业务逻辑的目的，出现逻辑错误

> 如果使用弱引用

假设Entry弱引用threadLocal，尽管会出现内存泄漏的问题，但是在threadLocal的生命周期里（set,getEntry,
remove）里，都会针对key为null的脏Entry进行处理。
从以上的分析可以看出，使用弱引用的话在`ThreadLocal`生命周期里会尽可能的保证不出现内存泄漏的问题，达到安全的状态。

## References
- https://www.jianshu.com/p/dde92ec37bd1
- https://blog.csdn.net/zsfsoftware/article/details/50933151

> 本文首次发布于 [ElseF's Blog](http://elsef.com), 作者 [@stuartlau](http://github.com/stuartlau) ,
转载请保留原文链接.
