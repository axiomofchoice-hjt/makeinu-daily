---
date: '2025-11-01'
title: 败犬のC++每月精选 2025-10
next: false
prev:
  link: /2025/09
  text: 败犬のC++每月精选 2025-09
description: 本期败犬日报包含 C++ 语言特性、标准库行为、模板编程、多线程优化等多个话题，涵盖从基础到专家的知识层次。
__tags__:
- title: '## 1. 为什么成员函数模板不能是虚函数'
  score: 9/10
  tags:
  - C++
  - 语法特性
  - 面向对象编程
  - 泛型编程
  - 专家知识
  explanation: 探讨 C++ 标准规定成员函数模板不能为虚函数的原因，涉及基于继承的多态局限性、非侵入式多态解决方案，属于语法层面的专家知识。
- title: '## 2. `std::map` 用 const_cast 修改 key 是不是未定义行为'
  score: 8/10
  tags:
  - C++
  - STL
  - 内存管理
  - 基础知识
  - 需改进
  explanation: 分析 std::map 中 const_cast 修改 key 的未定义行为，指出标准库设计原理和正确修改方式，但未深入解释 const
    修饰的底层原因，需改进补充。
- title: '## 3. `A a = A();` 有没有触发拷贝或移动构造'
  score: 7/10
  tags:
  - C++
  - 语法特性
  - 内存管理
  - 基础知识
  explanation: 解释 C++17 复制消除规则，说明直接构造行为与编译器优化的区别，属于基础语法知识。
- title: '## 4. `requires { expr; }` 和 `requires expr` 的区别'
  score: 8/10
  tags:
  - C++
  - 语法特性
  - 泛型编程
  - 进阶知识
  explanation: 区分 requires 表达式和 requires 子句的语法功能，展示概念约束的实际应用，属于泛型编程的进阶知识。
- title: '## 5. 无捕获 lambda 转换的指针会悬垂吗'
  score: 7/10
  tags:
  - C++
  - 语法特性
  - 函数
  - 基础知识
  explanation: 说明无捕获 lambda 转换函数指针的生命周期安全性，提及非标准场景的例外情况，属于基础函数特性知识。
- title: '## 6. 静态类型、动态类型、强类型、弱类型'
  score: 6/10
  tags:
  - 其他
  - 基础知识
  - 内容较主观
  - 需改进
  explanation: 讨论类型系统术语的模糊定义，总结常见说法但缺乏权威引用，内容较主观且需改进补充严格定义。
- title: '## 7. 业务要求新代码和老代码的 `unordered_map` 遍历顺序必须一致，且老代码不能改'
  score: 8/10
  tags:
  - C++
  - STL
  - 工程实践
  - 进阶知识
  - 搞笑
  explanation: 吐槽依赖 unordered_map 未指定顺序的代码问题，提供锁编译器版本或重实现等解决方案，带有搞笑元素。
- title: '## 8. 怎么给 `T&&` 参数一个回调函数默认参数'
  score: 7/10
  tags:
  - C++
  - 语法特性
  - 泛型编程
  - 进阶知识
  explanation: 解决模板参数推导与默认参数的冲突，展示 C++20 及之前的两种实现方式，属于泛型编程进阶知识。
- title: '## 9. memset 是循环实现的吗'
  score: 6/10
  tags:
  - C++
  - 标准库特性
  - 性能优化
  - 硬件相关
  - 基础知识
  - 需改进
  explanation: 说明 memset 实现未由标准规定，可能涉及编译器优化和硬件特性，但未详细展开具体优化技术，需改进补充。
- title: '## 10. 面试题：1024 核，N 个数找最大值，不许用锁或原子操作'
  score: 8/10
  tags:
  - C++
  - 并发编程
  - 性能优化
  - 算法
  - 工程实践
  - 进阶知识
  explanation: 分析多线程求最大值的算法设计，讨论线程同步开销与优化策略，涉及并发编程和性能优化的工程实践。
- title: '## 11. 一些文章'
  score: 7/10
  tags:
  - 其他
  - 基础知识
  - 进阶知识
  - 内容较主观
  explanation: 汇总多篇技术文章链接，涵盖硬件延迟、C++20 ranges 批评、函数调用原理等话题，内容较主观且范围广泛。
---

![img](/img/2025-10-index.png)

# 败犬のC++每月精选 2025-10

[[toc]]

## 1. 为什么成员函数模板不能是虚函数

对应知乎问题 <https://www.zhihu.com/question/474773455>。

标准已经规定 [ref](https://en.cppreference.com/w/cpp/language/virtual.html): Function templates cannot be declared virtual，那么为什么这么规定呢？

***

首先，子类并不知道基类的成员函数模板有哪些实例，比如：

```cpp
#include <memory>
#include <print>

struct Base {
    template <typename T>
    /* virtual */ void foo(T) {
        std::println("Base::foo");
    }
};

struct Derived : Base {
    template <typename T>
    void foo(T) {
        std::println("Derived::foo");
    }
};

int main() {
    std::unique_ptr<Base> d = std::make_unique<Derived>();
    d->foo(114514);  // Base::foo，怎么才能输出 Derived::foo？
}
```

想要上面代码只有基类实例化了 `Base::foo<int>`，子类没实例化。如果想要调 `Derived::foo<int>`，除非运行时调编译器给你实例化一个。（如果你觉得编译器足够聪明会尽可能实例化子类的函数模板，那再想想多编译单元 + 动态链接，编译器、链接器都无法拿到全部信息）

***

上面例子的原因是，基于继承的多态已经满足不了我们了。于是我们掏出非侵入式多态（[往期](/2025/09/09)有讲原理，但这里不需要知道原理），假设有个神奇的宏 INTERFACE：

```cpp
#include <memory>
#include <print>

struct Base {
    template <typename T>
    /* virtual */ void foo(T) {
        std::println("Base::foo");
    }
};

struct Derived : Base {
    template <typename T>
    void foo(T) {
        std::println("Derived::foo");
    }
};

INTERFACE(Base2, Base, FUNC(foo, int));

int main() {
    std::unique_ptr<Base2> d = std::make_unique<Derived>();
    d->foo(114514);
}
```

区别就是 INTERFACE 宏指定了哪些函数模板会实例化，这样就完美解决了问题。我用微软的 proxy 库试了一下，是可以的：<https://godbolt.org/z/b7q1z4WPW>

***

这里甚至都没提到虚表的事情，因为只在语法层面探讨，没有到实现层面。虚表绑定了基于继承的多态，对于非侵入式多态，虚表不够用了。至于为什么可以看上面的知乎问题。（这可能是面试官想要的答案，但是，问题的根源是语法而不是实现）

## 2. `std::map` 用 const_cast 修改 key 是不是未定义行为

```cpp
std::map<int, int> map = {{1, 2}};
const_cast<int&>(map.begin()->first) = 2;
```

是 UB。这是因为 map value_type 是 `std::pair<const Key, Value>`，初始化就带有 const 就不能修改了。

同时 <https://en.cppreference.com/w/cpp/container/map/extract.html> 里说：

> extract is the only way to change a key of a map element without reallocation

只能用 extract 修改 key，但是复杂度是 $O(\log n)$，很显然标准没有提供一个更快的接口。

真有需求只能手写数据结构，或者 key 用结构体 + mutable 包装一层。

## 3. `A a = A();` 有没有触发拷贝或移动构造

C++ 老版本有拷贝或移动（有移动调移动）。C++17 规定了复制消除，不调用移动或拷贝，会直接构造到对应位置上。

注意了，这是标准行为，不是编译器优化。优化是不会把拷贝或移动给优化没的（比如拷贝 / 移动里有打印，就一定会打印）。

## 4. `requires { expr; }` 和 `requires expr` 的区别

`requires { expr; }` 是 requires 表达式 (requires expression)，判断 expr 合不合法，可以得到一个 bool 值。[ref](https://en.cppreference.com/w/cpp/language/requires.html)

`requires expr` 是 requires 子句 (requires clause)，约束模板的语法，检查 expr 是否为真。[ref](https://en.cppreference.com/w/cpp/language/constraints.html)

```cpp
template <typename T>
concept Addable = requires { T{} + T{}; };  // requires 表达式

template <typename T>
    requires Addable<T>  // requires 子句
void f() {}

template <typename T>
    requires requires { T{} + T{}; }  // requires 子句套 requires 表达式
void g() {}

int main() {
    f<int>();
    g<int>();
}
```

## 5. 无捕获 lambda 转换的指针会悬垂吗

不会，一般来说函数指针都不会悬垂。更严谨地，有效的函数指针会一直有效。

（不一般的情况是 mmap 可执行内存，cast 为函数指针，这样 munmap 就会悬垂了。只不过这个 mmap 并非标准）

[cppref](https://en.cppreference.com/w/cpp/language/lambda.html) 里只能查到转换后是 "a pointer to a function with C++ language linkage"，应该暗示了生命周期是 static 的。

## 6. 静态类型、动态类型、强类型、弱类型

都没有严格定义。

几乎所有人对静态 / 动态类型的说法是：静态类型语言在编译期进行类型检查，类型检查是指标识符（通常是变量）是否和类型绑定，不可更改；动态类型语言相反。

但是有几个问题，编译期（语言的实现）和语言应该是解耦的，不能用来定义语言的属性。还有不应该只有标识符，而是所有表达式。

当然了，因为没有严格的定义，所以这么说也无妨。

***

对于强 / 弱类型的说法更多更模糊了：

1. 是否禁止隐式转换。（最常见的说法，随便一搜全是）
2. 是否禁止丢失信息的隐式转换。[wikipedia](https://en.wikipedia.org/wiki/Type_system)
3. 类型安全：数据是否只按一个类型处理。[wikipedia](https://en.wikipedia.org/wiki/Type_safety)

其实隐式转换和类型安全都是阻止不合理的类型，只不过前者的结果明确但不符合人的期望，后者会导致严重问题（严格别名问题、数组越界、野指针等）。

## 7. 业务要求新代码和老代码的 `unordered_map` 遍历顺序必须一致，且老代码不能改

你猜为什么这个容器叫 unordered_map。unordered_map 的遍历顺序是未指定的 [ref](https://eel.is/c++draft/unord.req#general-6)，依赖这个顺序的人应该被问候一顿。

老代码不能改，可以让新代码锁编译器版本；或者把老代码的 unordered_map 实现抄出来，这样可以升级编译器。

## 8. 怎么给 `T&&` 参数一个回调函数默认参数

```cpp
template <typename T>
void run(T &&callback = [](auto &&arg) {}) {
    callback(1);
}

int main() {
    run();  // Candidate template ignored: couldn't infer template argument 'T'
    run([](auto &&arg) {});
}
```

要指定默认模板参数，因为默认参数不参与模板推导。

```cpp
template <typename T = decltype([](auto &&) {})>
void run(T &&callback = {}) {
    callback(1);
}

int main() {
    run();
    run([](auto &&) {});
}
```

在 C++20 以前的写法是：

```cpp
struct default_functor {
    template <typename T>
    void operator()(T &&) const {}
};

template <typename T = default_functor>
void run(T &&callback = {}) {
    callback(1);
}

int main() {
    run();
    run([](auto &&) {});
}
```

## 9. memset 是循环实现的吗

标准没有规定 memset 怎么实现。你可以只用循环实现（这样性能就不好），可以汇编，也可以调用 `__builtin_memset` 交给编译器实现。

如果要深究实现，那就可能碰到编译器优化、不同尺寸优化、循环展开、SIMD 等操作。

## 10. 面试题：1024 核，N 个数找最大值，不许用锁或原子操作

这问题就很奇怪，线程同步的几个方式算不算用锁或原子变量？算就没法多线程了，那 1024 核的条件有什么用。

不考虑“不许用锁或原子操作”，就把 N 给分为 1024 个等长的块，每个线程处理一块，拿到每一块的最大值。最后单线程把每个块的最大值再求一遍最大值即可。

用 openmp 很容易就能实现：

```cpp
#include <omp.h>

#include <algorithm>
#include <cstdio>
#include <limits>
#include <vector>

int get_max(int *a, int n, int n_threads) {
    std::vector<int> result(n_threads, 0);
#pragma omp parallel num_threads(n_threads)
    {
        int max = std::numeric_limits<int>::min();
#pragma omp for
        for (int i = 0; i < n; i++) {
            max = std::max(max, a[i]);
        }
        result[omp_get_thread_num()] = max;
    }
    return *std::max_element(result.begin(), result.end());
}

int main() {
    int arr[] = {1, 3, 2, 8, 4, 6};
    printf("%d\n", get_max(arr, std::size(arr), 4));
}

// g++ test.cpp -o test -O3 -fopenmp && ./test
```

这里有一点是最后一步为什么不用多线程？这是因为 1024 个数求最大值已经非常快了，而且数据在 L3 cache 上，粗略估计 100 ns。而线程同步开销本身就至少几百 ns，在我机器上 4 核同步 600 ns。

所以单线程就是最快的。

用下面的程序可以测一下线程同步开销：

```cpp
#include <omp.h>

#include <chrono>
#include <iostream>

int main() {
    const int STEP = 1000000;
    const int n_threads = 4;
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < STEP; ++i) {
#pragma omp parallel num_threads(n_threads)
        {
            asm volatile("" ::: "memory");
        }
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto elapsed = end - start;
    std::cout << "time: " << elapsed.count() / STEP << " ns\n";
}
```

但是群友表示这个答案面试官认为还能再快，那就再把 simd，numa，分布式，gpu 这些答一遍，总该满意了。

## 11. 一些文章

存储设备的延迟 <https://planetscale.com/blog/io-devices-and-latency>。

为什么C++20 ranges 如此反直觉？<https://www.zhihu.com/question/1960030184716637579/answer/1960083519884760037> 这是真的 shit 山。

x86 函数调用的原理 <https://mp.weixin.qq.com/s/zMe05GJz67CHvf1wds4t6g> 每个 C++er 的基本功。

傅里叶变换，带交互的博客 <https://www.jezzamon.com/fourier/zh-cn.html> 交互很丝滑。

c、c++运行速度快，是语法决定的还是编译器决定的？<https://www.zhihu.com/question/662554502/answer/1961219439233053978>。

jemalloc 内存分配与优化实践 <https://mp.weixin.qq.com/s/U3uylVKZ-FsMjdeX3lymog>。

深度｜DeepSeek-OCR引爆“语言vs像素”之争，Karpathy、马斯克站台“一切终归像素”，视觉派迎来爆发前夜 <https://mp.weixin.qq.com/s/UeFPdfFTzC8XNb9IX13rnQ> 一种压缩 token 思路，用视觉 token。

x86 LOCK 指令前缀介绍 <https://mp.weixin.qq.com/s/-3TFPsZb_n53fpSMfBXp0w>。

实战案例：如何调试 Linux 内核丢包问题？
<https://mp.weixin.qq.com/s/W9kalwnpkvjHM-KiQuOrYw>

Introducing the Maple Tree <https://lwn.net/Articles/901714/> kernel 里面的并发 tree 结构，based on B-tree。

避开 Linux OOM：先懂动态内存管理 <https://mp.weixin.qq.com/s/rv1DCcyiIOIkBSBs5C7FIA>。

Google DeepMind：AI下一阶段的预测（Hot Chips 2025 主题演讲）<https://mp.weixin.qq.com/s/SF6vWMuVgiwZcMx8O_25VQ>。

AI 会让编程初学者更快入门，还是更快迷失？<https://www.zhihu.com/question/1962181838035444178/answer/1963771107871006826>。

Meta 每秒如何移动 TB 级数据？<https://mp.weixin.qq.com/s/N0xU2ZrytWZRcIKC97ZYtw>
