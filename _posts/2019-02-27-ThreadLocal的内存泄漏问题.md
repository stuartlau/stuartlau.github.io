---
layout:     post
title:      "ThreadLocal的内存泄漏问题"
subtitle:   "When ThreadLocal has OOM Issue"
date:       2019-02-27
author:     SL
header-img: img/post-bg-universe.jpg
catalog: true
tags:
    - Java
---
    
> 本文说明当使用Thread和ThreadLocal的方式不当的时候，可能会会导致内存泄漏问题，并提供解决方案。

ThreadLocal通过采用「以空间换时间」的方式避免了并发中使用锁来控制多线程对共享变量的操作，使用线程「本地」变量的方式让多线程中的并发数据访问变得更加简单。
但是如果对ThreadLocal使用不当则会造成内存泄漏问题，本文主要分析内存泄漏出现的场景以及正确的使用ThreadLocal的方式。

## ThreadLocal基础

每个Thread实例都含有一个ThreadLocalMap变量，该变量定义在ThreadLocal中，访问权限为`package private`。

```java
/* ThreadLocal values pertaining to this thread. This map is maintained
     * by the ThreadLocal class. */
    ThreadLocal.ThreadLocalMap threadLocals = null;
```

ThreadLocalMap的JavaDoc如下：
```java
    /**
     * ThreadLocalMap is a customized hash map suitable only for
     * maintaining thread local values. No operations are exported
     * outside of the ThreadLocal class. The class is package private to
     * allow declaration of fields in class Thread.  To help deal with
     * very large and long-lived usages, the hash table entries use
     * WeakReferences for keys. However, since reference queues are not
     * used, stale entries are guaranteed to be removed only when
     * the table starts running out of space.
     */
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
对应的构造函数如下：
```java
    /**
     * Construct a new map initially containing (firstKey, firstValue).
     * 
     * ThreadLocalMaps are constructed lazily, so we only create
     * 
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
可知内部通过维护了一个Entry数组，每个Entry用于保存ThreadLocal为key的value的值。初始化的数组大小为16。

```java
    /**
     * The entries in this hash map extend WeakReference, using
     * 
     * its main ref field as the key (which is always a
     * 
     * ThreadLocal object).  Note that null keys (i.e. entry.get()
     * 
     * == null) mean that the key is no longer referenced, so the
     * 
     * entry can be expunged from table.  Such entries are referred to
     * 
     * as "stale entries" in the code that follows.
     */
    static class Entry extends WeakReference<ThreadLocal<?>> {
        /** The value associated with this ThreadLocal. */
        Object value;

        Entry(ThreadLocal<?> k, Object v) {
            super(k);
            value = v;
        }
    }
```
## 泄漏真凶
注意到Entry继承了WeakReference，而弱引用本身在GC触发时会被回收，所以key可能会变为null，即被回收掉了，但是value是一个强引用。该Entry在table
数组中也不会被垃圾回收自动触发「缩容」删除掉，不过ThreadLocalMap为我们提供了很多`expunge`机制，但前提是这个机制「需要显式触发」，这里也就是容易出现内存泄漏的地方！

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
        tab[staleSlot].value = null;
        tab[staleSlot] = null;
        size--;

        // Rehash until we encounter null
        Entry e;
        int i;
        for (i = nextIndex(staleSlot, len);
             (e = tab[i]) != null;
             i = nextIndex(i, len)) {
            ThreadLocal<?> k = e.get();
            if (k == null) {
                e.value = null;
                tab[i] = null;
                size--;
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
```
很幸运的是，这个方法在内部很多方法实现里都会被调用到，比如：ThreadLocal.remove(), ThreadLocal.set()
。所以当我们显式调用这些方法的时候内部会自动帮我们清理那些已经被垃圾回收的key对应的Entry。

## 解决方案
正如上面介绍的，因为WeakReference类型key被垃圾回收，但其对应的Entry仍然在table中保留，如果没有及时清理并且对应的线程是线程池里的一个long-live
线程，则会造成内存泄漏。
如果是一个new Thread生成的线程则不会有这种问题，原因是线程的生命周期随着`run`方法的结束就结束了，GC会帮我们回收该thread引用的内存。
错误的使用方式：使用ThreadLocal作为内部变量，导致其被垃圾回收，进而导致所有线程中已经实例化的ThreadLocalMap的实例中都包含该ThreadLocal实例对应的key
的Entry实例。
有两种方式可以帮你避免OOM的问题：
- 解决方案1：使用全局static类型修饰ThreadLocal，让其不会被垃圾回收，从而避免撑满ThreadLocalMap。
- 解决方案2：如果非要作为局部变量声明，即每次都new一个新的ThreadLocal对象，则需要在使用前先调用可以触发「清理方法」的方法，如`remove
`方法，保证可以触发ThreadLocalMap
内部的`expunge
`机制，它会对map内已经「无效」的Entry进行清理，从而避免Thread实例中持有的ThreadLocalMap产生无法回收的内存，进而造成内存泄漏。



> 本文首次发布于 [ElseF's Blog](http://elsef.com), 作者 [@stuartlau](http://github.com/stuartlau) ,
转载请保留原文链接.
