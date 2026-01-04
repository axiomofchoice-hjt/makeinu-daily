---
date: 2025-02-01
title: 败犬のC++每月精选 2025-01
prev:
  text: 败犬のC++每月精选 2024-12
  link: /2024/12
next:
  text: 败犬のC++每月精选 2025-02
  link: /2025/02
description: 本期日报包含 C++ 性能优化、对象模型、语言特性、工程实践等多个话题
__tags__:
- title: '## 1. 多线程写相邻变量'
  score: 8/10
  tags:
  - C++
  - 并发编程
  - 性能优化
  - 硬件相关
  - 进阶知识
  explanation: 讨论多线程环境下伪共享问题，通过 alignas 对齐解决缓存一致性问题，涉及并发编程和性能优化，属于进阶知识。
- title: '## 2. 切片'
  score: 7/10
  tags:
  - C++
  - 面向对象编程
  - 基础知识
  - 需改进
  explanation: 解释派生类向基类转换时的切片现象，但警告可能是检查工具错报，建议更清晰地说明切片的具体场景和影响。
- title: '## 3. copy-and-swap idiom'
  score: 9/10
  tags:
  - C++
  - 工程实践
  - 内存管理
  - 进阶知识
  explanation: 介绍 copy-and-swap 惯用法实现赋值运算符，强调异常安全和代码简洁性，属于工程实践和内存管理范畴。
- title: '## 4. 开源是什么模式，为什么公司会雇人写开源'
  score: 6/10
  tags:
  - 其他
  - 基础知识
  explanation: 简要说明开源商业模式，通过用户获取和影响力转化盈利，属于基础知识但内容较简略。
- title: '## 5. 面试：程序运行发生了死循环怎么定位'
  score: 7/10
  tags:
  - C++
  - 编译构建和调试
  - 面试常见
  - 基础知识
  explanation: 介绍使用 gdb attach 和 pstack 定位死循环的方法，涉及调试技巧，适合面试场景。
- title: '## 6. GC（垃圾回收）可以处理循环引用吗'
  score: 8/10
  tags:
  - 其他
  - 内存管理
  - 基础知识
  explanation: 分析不同垃圾回收算法对循环引用的处理能力，对比引用计数和标记清除等方法的差异。
- title: '## 7. 非模板语境下，`if constexpr` 对未命中分支做语义检查'
  score: 9/10
  tags:
  - C++
  - 编译期
  - 语法特性
  - 专家知识
  - 冷门知识
  explanation: 深入探讨 if constexpr 在模板和非模板语境下的语义检查时机，涉及 CWG2518 和编译器版本差异，属于专家知识。
- title: '## 8. 字面类型 (Literal Type)'
  score: 8/10
  tags:
  - C++
  - 编译期
  - 语法特性
  - 进阶知识
  explanation: 解释字面类型要求和 constexpr 构造函数的作用，涉及模板非类型参数的使用限制。
- title: '## 9. 为什么要区分 xvalue 和 prvalue'
  score: 9/10
  tags:
  - C++
  - 语法特性
  - 内存管理
  - 专家知识
  explanation: 详细分析 C++ 值类别中 xvalue 和 prvalue 的区别，从 identity、move 语义和临时量实质化角度解释，属于专家知识。
- title: '## 10. 有协程库不绑定调度器吗'
  score: 7/10
  tags:
  - C++
  - 并发编程
  - 语法特性
  - 进阶知识
  explanation: 讨论协程库设计中的调度器绑定问题，对比 C++20 无栈协程和传统实现，涉及并发编程特性。
- title: '## 11. 关于是否禁止用 goto'
  score: 8/10
  tags:
  - C++
  - 工程实践
  - 基础知识
  - 内容较主观
  explanation: 分析 goto 语句在 C 和 C++ 中的适用场景，基于 Dijkstra 观点和实际工程需求，带有一定主观性。
- title: '## 12. 为什么不能在类中初始化静态成员变量'
  score: 8/10
  tags:
  - C++
  - 语法特性
  - 基础知识
  explanation: 解释静态成员变量的 ODR 规则和类内初始化限制，说明 inline 关键字的作用。
- title: '## 13. 函数形参的生命周期'
  score: 9/10
  tags:
  - C++
  - 语法特性
  - 内存管理
  - 专家知识
  - 冷门知识
  explanation: 分析函数形参生命周期结束时机的实现定义行为，通过 CWG2850 说明不同编译器的输出差异，属于专家知识。
---

![img](/img/2025-01-index.png)

# {{ $frontmatter.title }}

[[toc]]

## 1. 多线程写相邻变量

```cpp
struct Point {
    int x;
    int y;
};

int main() {
    struct Point point = {0, 0};

    // Thread 1
    for (int i = 0; i < 100; i++) {
        point.x++;
    }

    // Thread 2
    for (int j = 0; j < 100; j++) {
        point.y++;
    }
}
```

缓存一致性保证了最终结果不会出现 `point.x` 和 `point.y` 不一致的情况。

所以问题只出在性能上，即伪共享（false sharing）。伪共享是多个线程同时修改位于同一 cacheline 中的不同变量，cacheline 会频繁地在多个核的 cahe 之间切换，从而降低性能。

解决方案是通过对齐让 x, y 位于不同的 cacheline 里（cacheline 是 64 字节，考虑到相邻 cacheline 的硬件预取，推荐 128 字节对齐）：

```cpp
struct Point {
    alignas(128) int x;
    alignas(128) int y;
};
```

此事在 c++ 性能优化指南上亦有记载。

## 2. 切片

下面代码可能会有警告 `Slicing derived object "d" by converting class type "Derived" to class type "Base".`

```cpp
class Base {
   private:
    int x;

   protected:
    Base(Base const& b) : x(b.x) {}
};

class Derived : public Base {
   private:
    int y;

   public:
    Derived(Derived const& d) : Base(d), y(d.y) {}  // Base(d) 发生了切片
};
```

切片是指将派生类转换到基类的过程。上面例子里 Derived 类的拷贝构造函数中，将 Derived 引用转换为 Base 引用就会发生切片。

警告可以通过显式类型转换来消除：

```cpp
Derived(Derived const& d) : Base(static_cast<Base const&>(d)), y(d.y) {}
```

但是这里的切片发生在构造函数中，显得有点奇怪，应该是检查工具的错报。

推荐阅读：<https://github.com/isocpp/CppCoreGuidelines/blob/master/CppCoreGuidelines.md#es63-dont-slice>

## 3. copy-and-swap idiom

<https://stackoverflow.com/questions/3279543/what-is-the-copy-and-swap-idiom>

```cpp
T& operator=(T other) {
    swap(*this, other);
    return *this;
}
```

如果这个类实现了 swap 函数，那么 `operator=` 就可以用 copy-and-swap idiom。

优点是异常安全（swap 和析构在实践上不应该抛异常）以及代码短。

## 4. 开源是什么模式，为什么公司会雇人写开源

通过开源项目获取用户，获取影响力，从而可以通过其他方式盈利。

例如 oracle 维护开源软件 mysql，mysql 用户数量多了就可以推广相关服务。

## 5. 面试：程序运行发生了死循环怎么定位

几个方法：

1. `gdb attach pid`，然后就可以 `bt` 查看函数栈。
2. 不暂停程序，可以 pstack。

## 6. GC（垃圾回收）可以处理循环引用吗

不一定，因为 GC 并不指代某个具体算法。

例如 refcount（引用计数）可以是 GC 的一种朴素的实现方式，无法处理循环引用。

现代的 GC 不用或者不只用 refcount，而是用 GC roots 算法，这是可以处理循环引用的。

Python 使用 refcount 但是会 mark and sweep 兜底。

## 7. 非模板语境下，`if constexpr` 对未命中分支做语义检查

这样写会编译报错：

```cpp
int main() {
    uint32_t x;
    if constexpr (std::is_integral_v<decltype(x)>) {
        std::cout << 111 << std::endl;
    } else {
        static_assert(false);
    }
    return 0;
}
```

***

一个不那么优雅的方案是拷贝一下 `if constexpr` 里的条件，这样 `static_assert` 求值出来是 true，可以编译通过：

```cpp
int main() {
    uint32_t x;
    if constexpr (std::is_integral_v<decltype(x)>) {
        std::cout << 111 << std::endl;
    } else {
        static_assert(std::is_integral_v<decltype(x)>);
    }
    return 0;
}
```

***

另一个是把 `if constexpr` 放进模板里：

```cpp
template <typename T>
void f(T x) {
    if constexpr (std::is_integral_v<decltype(x)>) {
        std::cout << 111 << std::endl;
    } else {
        static_assert(false);
    }
}
int main() {
    uint32_t x;
    f(x);
    return 0;
}
```

早期对分支的语义检查时机是在模板实例化前，CWG2518 把这个时机往后挪了，所以较新版本的编译器可以直接 `static_assert(false)`。

但如果是较旧的编译器（GCC 12 及以下），可以在 `if constexpr` 放进模板的基础上，使用惰性求值的方法，<https://zh.cppreference.com/w/cpp/language/if> 有记载：

```cpp
template<typename>
constexpr bool dependent_false_v = false;
 
template<typename T>
void f()
{
    if constexpr (std::is_arithmetic_v<T>)
        // ...
    else {
        // CWG2518 前的变通方案
        static_assert(dependent_false_v<T>, "必须是算术类型"); // OK
    }
}
```

## 8. 字面类型 (Literal Type)

```cpp
class A {
public:
    int x;
    A(int x) : x(x) {}
};

template<A a>
void f() {}

int main() {
    f<A{1}>();
}
```

这样会报错，因为 A 定义了非 constexpr 构造函数，A 不再是字面类型。

可以删掉这个构造函数或者构造函数加上 constexpr。

<https://zh.cppreference.com/w/cpp/named_req/LiteralType>

## 9. 为什么要区分 xvalue 和 prvalue

```cpp
template <class T> struct is_prvalue : std::true_type {};
template <class T> struct is_prvalue<T&> : std::false_type {};
template <class T> struct is_prvalue<T&&> : std::false_type {};

template <class T> struct is_lvalue : std::false_type {};
template <class T> struct is_lvalue<T&> : std::true_type {};
template <class T> struct is_lvalue<T&&> : std::false_type {};

template <class T> struct is_xvalue : std::false_type {};
template <class T> struct is_xvalue<T&> : std::false_type {};
template <class T> struct is_xvalue<T&&> : std::true_type {};
```

一个比较直观但不一定完全精确的解释，就是 xvalue 是有 identity（可取址）的一个将亡对象，所以往往是被 move 的对象；prvalue 是将要创建的对象（C++17 之后在最终用到的时候才会创建，不然中间会经历一个 xvalue 状态）；在 C++11 引入右值引用之后就需要引入这两个概念了，不然我们没法区分上面的 `T` 和 `T&&`；其余的 properties 大抵都是基于这个区别衍生的，比如可否多态。

在 C++17 提出的这套设想里面，prvalue 更类似于一个“值”的概念，是不可操作的，不是对象。所以必须通过临时量实质化转变为对象才能操作，这个对象因为不被持有，所以是个 going to die 的。

"prvalues perform initialization, glvalues produce locations."

## 10. 有协程库不绑定调度器吗

以前没有无栈协程的语法，不方便。一般整协程都是从实践出发，没必要搞通用实现，搞起来也麻烦。对于特定场景下的使用也没啥好处。

现在 C++20 有了无栈协程，弄起来方便点了，就有很多库允许用户自己提供调度器了。例如 async simple 库。

C++26 那个 execution 的设计准则也是允许用户自己提供调度器来适应不同场景。

## 11. 关于是否禁止用 goto

《goto statement considered harmful》 —— Dijkstra

C 使用 goto 是合理的，因为没有异常也没有 RAII，还要管理资源、错误处理，goto 是最简单的方法。linux kernel 就有很多 goto。当然不能滥用，能不用就不用原则。

但是到了 C++ 有了上述的机制，goto 显得没必要了。

## 12. 为什么不能在类中初始化静态成员变量

ODR 问题，详见 <https://zh.cppreference.com/w/cpp/language/definition>。

静态成员变量是声明，不能是定义，否则在多个编译单元里就会有多个定义。

想要类内初始化，可以用 inline。

## 13. 函数形参的生命周期

```cpp
#include <cstring>
#include <memory>
#include <iostream>
#include <string>
#include <vector>

class Resource {
    char _records;
public:
    Resource(char c): _records(c) {}
    ~Resource() {
        std::cout << _records << '\n';
    }
};

using Unique = std::unique_ptr<Resource>;
Unique reset(Unique ptr) {
    return std::make_unique<Resource>('b');
}
void drop(Unique ptr) {}
int main() {
    drop(reset(std::make_unique<Resource>('a')));
    return 0;
}
```

这个代码在 GCC 14.2 输出 b a，在 x86 msvc 19.30 输出 a b。

这是因为函数形参的生命周期是在函数末尾结束还是在全表达式末尾结束，这个东西是实现定义的。

<https://wg21.link/cwg2850>
