---
title: 败犬のC++每月精选 2025-02
prev:
    text: 败犬のC++每月精选 2025-01
    link: /2025/01
next: false
---

# {{ $frontmatter.title }}

[[toc]]

## 1. inline 对内联优化的影响

我们知道，inline 现在最主要的作用是允许函数、变量的定义在多个翻译单元出现。

除此之外 inline 让编译器更倾向于内联优化（只是影响很小）。

> LLVM IR 有一个 inlinehint 属性。根据 LLVM IR 参考文档关于 inlinehint 的说明:
>
> 此属性表示源代码包含了一个提示，表明内联此函数是可取的(例如 C/C++ 中的"inline"关键字)。这只是一种提示，不会对内联器施加任何要求。
>
> inline 关键字与优化有关，而且优化器会关心你是否添加了它，但也没有太大影响。如果你真的想要内联一个函数，我想你应该添加 always_inline 说明符，这是完全不同的情况：除非完全不可能，否则编译器将始终内联这些函数。

<https://github.com/llvm/llvm-project/commit/74bb06c0f02e650ea9ec73729f41a620fc55a8ee>

<https://godbolt.org/z/jfo35vvzf>

## 2. 运行报错 "pure virtual method called"

这个问题一般是基类构造时、析构时或者析构后调用了纯虚函数。

例如下面代码就是**析构后**调用了纯虚函数：

```cpp
#include <cstdlib>
#include <new>

struct A {
    virtual void foo() = 0;
    virtual ~A() = default;
};

struct B : A {
    void foo() override {}
};

int main() {
    B* b = (B*)malloc(sizeof(B));
    new (b) B();
    A *a = b;
    b->~B();
    a->foo();  // pure virtual method called
    free(b);
    return 0;
}
```

代码在 GCC 14.2 不加优化时会报 "pure virtual method called"，加 O2 优化会正常退出（因为是未定义行为，发生什么都合理）。

<https://zh.cppreference.com/w/cpp/language/virtual> 有记载：

> 在构造和析构期间，进一步的派生类并不存在，如同\*this的动态类型是正在构造的类的静态类型（动态派发不在继承层级下传）。

因此**一个可能的实现是**，B 构造依次执行 A, B 的构造函数，虚表指针也会依次指向 A, B 的虚表。析构则是倒过来。

<https://itanium-cxx-abi.github.io/cxx-abi/abi.html#pure-virtual> 有记载，存虚函数在虚表里也会有表项。例如，GCC 给 A 虚表的 foo 一个占位符号 __cxa_pure_virtual，它负责直接 terminate：

```text
vtable for A:
        .quad   0
        .quad   typeinfo for A
        .quad   __cxa_pure_virtual
        .quad   0
        .quad   0
```

```cpp
LIBCXXABI_NORETURN
void __cxa_pure_virtual(void) {
    abort_message("Pure virtual function called!");
}
```

这下就能解释了。

扩展阅读：调用 deleted 虚函数的相关问题 <https://stackoverflow.com/questions/30596591/when-is-cxa-deleted-virtual-called>。

## 3. `stdx::simd` 默认使用什么指令集

cppref 上的 `stdx::simd` 默认模板是 `simd_abi::compatible`，可能会误以为是动态选择指令集。

实则不然，这个 compatible 的描述是保证兼容性。<https://zh.cppreference.com/w/cpp/experimental/simd/compatible>

所以大概是指最“短”的向量。

```cpp
#include <experimental/simd>
namespace stdx = std::experimental;

auto simd_add(stdx::simd<float> x, stdx::simd<float> y) {
    return x + y;
}
```

GCC 14.2 编译参数 `-std=c++23 -march=x86-64 -mavx512f -O3`，这个生成的汇编是 `vaddps  xmm0, xmm0, xmm1`，用的是 SSE 指令集。如果 `stdx::native_simd` 就是 AVX512。（另外试了一下 arm clang 19.1，native_simd 只有 NEON，不支持 SVE）

这点也可以在 stdlibc++ 代码里得到验证：<https://github.com/gcc-mirror/gcc/blob/trunk/libstdc%2B%2B-v3/include/experimental/bits/simd.h#L2977>。

那么 `stdx::simd` 有什么用呢？可能……就是没用，我直接编译参数限制 SSE 也能有同样效果。

一般情况用 `stdx::native_simd` 就行了。

## 4. 内存序 AcqRel，实际运行各个核会看到不一样的顺序吗

因为缓存失效通知是异步送达的。<https://zh.cppreference.com/w/cpp/atomic/memory_order> 最后的例子中，假设双路主板，a 和 c 在一个插槽上，b 和 d 在另一个插槽上。

## 5. 内存序先写后读的问题

```cpp
atomic<int> done;
atomic<int> waiting;

void notify() {
    done = 1;
    if (!waiting)
        return;
    // ... wake up waiter...
}

void wait() {
    waiting = 1;
    if (done)
        return;
    // ... sleep...
}
```

done, waiting 读的内存序是 acquire，写是 release。并发调用 notify 和 wait，为什么有可能出现 notify 立刻返回且 wait 陷入 sleep？

因为内存序的定义是这样的。acquire 阻止之后的指令不能排到前面，release 阻止之前的指令不能排到后面。但是先写后读不同的变量（同一变量有保障），不能阻止它们的乱序成先读后写。

所以这里需要 seqcst 内存序。

也可以用屏障，但是开销比 seqcst 内存序大。

## 6. 标记访问某个变量时必须持有某个锁

Clang 的 Thread Safety Analysis。

<https://clang.llvm.org/docs/ThreadSafetyAnalysis.html>

<https://www.cnblogs.com/jicanghai/p/9472001.html>

还能报告句柄竞争。

```cpp
struct BankAccount {
    Mutex mu;
    int balance GUARDED_BY(mu);
};
```

## 7. magic static

```cpp
void swapTwoPoints(std::pair<double,double>& a, std::pair<double,double>& b) {
    static std::pair<double,double> tmp = a;
    a = b;
    b = tmp;
    return;
}
```

这个代码的 bug 是静态局部变量只有首次调用会初始化，第二次调用就寄了。

magic static 就是用运行时的值去初始化静态局部变量，效果是只会初始化一次，还能保证并发安全。

效果和 `std::call_once` 相同。

magic static 可以用来实现单例模式。

（代码来源是 <https://www.zhihu.com/question/451327108/answer/53592485454>）

## 8. 拷贝构造的参数不加引用

```cpp
struct T {
    T(const T rhs) { ... }
};
```

不行。因为 rhs 传参的时候，它需要被初始化。而“初始化”这个过程依赖构造函数，这样就会无限递归。

事实上编译器会报错 `error: invalid constructor; you probably meant 'T (const T&)'`。

## 9. 为什么 L1 Cache 只有页内的位才能索引

缓存一致性问题。

虚拟地址分为页号（高位部分）和页内偏移（低位部分）。如果两个虚拟地址映射到同一物理地址时，这个物理地址就可以映射到不同的缓存组中。而虚拟 / 物理地址的页内偏移是一致的（翻译前后不变），就不会出现这个问题。

## 10. 加 prefetch 性能是否有提升

经常没有提升。

因为一般 CPU 的硬件预取能覆盖常见的访问模式，不用再做软件预取了，简单的 CPU 除外。另外一些算法的特殊访问模式也会对预取效果有影响。

所以满足上述条件的可以多花时间研究 prefetch。

## 11. float 转换为相同二进制表示的 int

标准做法是 `std::bit_cast`（C++20），旧版本用 `memcpy`。不用担心性能，memcpy 第三个参数是常量会被编译器优化掉，从而没有函数调用开销。

```cpp
int convert(float x) {
    int y;
    memcpy(&y, &x, sizeof(int));
    return y;
}
```

不标准但可行的做法是搞个 `union`。<https://zh.cppreference.com/w/cpp/language/union> 有记载：

> 读取并非最近写入的联合体成员是未定义行为。许多编译器以非标准语言扩展实现读取联合体的不活跃成员的能力。

不标准且不推荐用 `reinterpret_cast`（是未定义行为，有类型别名问题）。

## 12. 单元测试怎么测 private 函数

好的实践是测接口功能而不是内部实现。如果你觉得你特别需要测 private 函数，很有可能意味着需要修改设计，把复杂的逻辑单独提出来一个工具类。

如果一定要测，就用 `-fno-access-control`（不要用 `#define private public` 给代码下毒）。

推荐阅读 <https://google.github.io/googletest/advanced.html#testing-private-code>。

## 13. `unique_ptr` 的大小

如果 Deleter 是默认的，或者是空类，大小是 8（一个指针的大小）。在实现上可以用空基类优化把这个 Deleter 空间搞掉。

```cpp
#include <iostream>
#include <memory>

struct A {
    void operator()(int*) {}
};

int main() {
    std::unique_ptr<int, A> a;
    std::tuple<int*, A> b;
    std::cout << sizeof(a) << '\n';  // 输出 8
    std::cout << sizeof(b) << '\n';  // 输出 8
}
```
