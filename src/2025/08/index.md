---
date: 2025-09-01
next: false
prev:
  link: /2025/07
  text: 败犬のC++每月精选 2025-07
title: 败犬のC++每月精选 2025-08
---

![img](/img/2025-08-index.png)

# 败犬のC++每月精选 2025-08

[[toc]]

## 1. 结构化绑定的变量不触发 NRVO

```cpp
#include <iostream>
#include <tuple>
#include <utility>

struct T {
    T() = default;
    T(const T&) { std::cout << "Copy constructor called\n"; }
    T(T&&) noexcept { std::cout << "Move constructor called\n"; }
};

std::pair<int, T> foo() {
    return {std::piecewise_construct, std::forward_as_tuple(42),
            std::forward_as_tuple()};
}

T func() {
    auto [x, y] = foo();
    // copy!!!
    return y;
}

int main() {
    T t = func();
    return 0;
}
```

输出 "Copy constructor called"。

结构化绑定实际上仍然是单个变量，然后给每个字段一个别名，而非直接构建出多个变量。

nrvo 是直接在返回值那个地址对象上构造局部变量。对于子对象，你没法把这个子对象换成函数返回值，其它子对象用原本局部变量的。所以一定没法 rvo/nrvo。

所以要写成 `return std::move(y);`。

## 2. bool 变量分发到 bool 模板实参

简单的做法是宏，将 bool 传给 constexpr 变量：

```cpp
#include <iostream>

#define DISPATCH_BOOL(condition, name, ...) \
    if (condition) {                        \
        constexpr bool name = true;         \
        (__VA_ARGS__)();                    \
    } else {                                \
        constexpr bool name = false;        \
        (__VA_ARGS__)();                    \
    }

template <bool Flag>
void foo() {
    printf("%d\n", Flag);
}

int main() {
    for (bool flag : {false, true}) {
        DISPATCH_BOOL(flag, Flag, [] { foo<Flag>(); });
    }
    return 0;
}
```

不用宏，用模板也是可以的：

```cpp
#include <iostream>
#include <type_traits>

template <typename lambda_t>
auto dispatch_bool(bool condition, const lambda_t& lambda) {
    if (condition) {
        return lambda.template operator()<true>();
    } else {
        return lambda.template operator()<false>();
    }
}

template <bool Flag>
void foo() {
    printf("%d\n", Flag);
}

int main() {
    for (bool flag : {false, true}) {
        dispatch_bool(flag, []<bool Flag> { foo<Flag>(); });
    }
}
```

群友还给了 `std::visit` 的做法，支持多个 bool，不过看起来有点啰嗦：

```cpp
#include <iostream>
#include <type_traits>
#include <variant>

std::variant<std::false_type, std::true_type> inline make_bool_variant(
    bool condition) {
    if (condition) {
        return std::true_type{};
    } else {
        return std::false_type{};
    }
}

int main() {
    for (auto [a, b, c] : {std::tuple{0, 0, 1}, std::tuple{1, 0, 1}}) {
        std::visit(
            [&](auto a, auto b, auto c) {
                printf("%d %d %d\n", decltype(a)::value, decltype(b)::value,
                       decltype(c)::value);
            },
            make_bool_variant(a), make_bool_variant(b), make_bool_variant(c));
    }
}
```

## 3. 临时对象是纯右值

众所周知 `std::vector{1} = std::vector{2};` 可以编译通过。

另一个例子是：

```cpp
struct T {
    T& operator=(T) { return *this; }
};

struct V {
    V& operator=(V) & { return *this; }
};

int main() {
    T{} = T{};  // ok
    V{} = V{};  // error: Candidate function not viable: expects an lvalue for object argument
}
```

这里的 V 的拷贝函数限制了左值，因此过不了编译。

## 4. asan 用于下毒的代码

```cpp
class AsanPoisonDefer {
#ifdef ADDRESS_SANITIZER
public:
    // Poison the memory region to prevent accidental access
    // during the lifetime of this object.
    AsanPoisonDefer(const void* start, size_t len) : start(start), len(len) {
        ASAN_POISON_MEMORY_REGION(start, len);
    }
    // Unpoison the memory region when this object goes out of scope.
    ~AsanPoisonDefer() { ASAN_UNPOISON_MEMORY_REGION(start, len); }

private:
    const void* start;
    size_t len;
#else
public:
    // No-op for platforms without ASAN_DEFINE_REGION_MACROS
    AsanPoisonDefer(const void*, size_t) {}
    ~AsanPoisonDefer() = default;
#endif
};
```

手动下毒，防止内存上没越界，但逻辑上越界了。

例如访问 `vec[0]` 的时候，给 `vec[1]` 打 poison。

主要用于内存池，越界也不会报错，只能手动下毒。

## 5. 数学函数（例如 std::sqrt）不是 constexpr

因为数学函数会被舍入模式影响，还可能设置 errno，也就是有全局状态的读写。C++26 开始变成 constexpr，做法就是用 if consteval 主动判断是否编译期求值返回不同结果。

参考文章：<https://www.zhihu.com/question/265774676/answer/3471569930>

## 6. 怎么让变量在不同编译期条件下绑定不同类型的变量

类似 `auto val = cond ? int{} : std::string{};`

可以这么做：

```cpp
auto val = [] {
    if constexpr (cond) {
        return int{};
    } else {
        return std::string{};
    }
}();
```

注意如果 else 去掉会报错，代码如下，这是因为函数返回值类型推导要求，在 constexpr if 里的语句才可能不参与推导。

```cpp
auto val = [] {
    if constexpr (cond) {
        return int{};
    }
    return std::string{};  // return type 'std::string' (aka 'basic_string<char>') must match previous return type 'int' when lambda expression has unspecified explicit return type
}();
```

## 7. `buildin_ctz(0)` 是未定义行为

是的。ref <https://gcc.gnu.org/onlinedocs/gcc/Bit-Operation-Builtins.html#index-_005f_005fbuiltin_005fctz>

这是因为处理器一般只输出 32 个状态（5 bit），处理 0 就要 33 个状态，于是不支持。

builtin 应该是希望做简单一点的，所以给 0 设成未定义行为了。如果要通用的话就特殊处理 0，比如 `std::countr_zero` 就是通用的，x86 上汇编就是这样：

```cpp
#include <bit>

int foo1(unsigned x) {
    return std::countr_zero(x);
    // xor     eax, eax
    // mov     edx, 32
    // rep bsf eax, edi
    // test    edi, edi
    // cmove   eax, edx
    // ret
}

int foo2(unsigned x) {
    [[assume(x != 0)]];
    return std::countr_zero(x);
    // xor     eax, eax
    // rep bsf eax, edi
    // ret
}
```

## 8. C++ vector 的 push_back 扩容机制为什么不考虑在尾元素后面的空间申请内存

参考文章：<https://www.zhihu.com/question/384869006>

关键点是，realloc 接口不灵活，它在原地扩张失败后会自动分配内存并 memcpy 过去，不会调移动构造函数。这就必须要保证对象是 trivially copyable 的。

C++ 还没有类似的函数进入标准，可以看 [C++ 中的 relocate 语义 - YKIKO的文章 - 知乎](https://zhuanlan.zhihu.com/p/679782886)

## 9. 模板模板参数的一个例子：Allocator rebind

这个操作非常神人。

如果要写一个模板容器（如红黑树），用户提供的是一个节点的 allocator 类型 `Allocator<Node>`，模板容器可以把 allocator 拿出来 rebind 成其他类型 `Allocator<Other>`。

## 10. 父类 16 字节，子类有成员变量还是 16 字节

这是因为父类为了字节对齐，尾部有 padding，一些情况下子类可以往这里面塞成员变量。

例如：

```cpp
#include <cstdint>
#include <cstdio>

class A {
    int64_t a;
    int32_t b;
};

class B : A {
    int32_t c;
};

int main() {
    printf("%zu %zu\n", sizeof(A), sizeof(B));  // 输出 16 16（GCC 15.1）
}
```

[往期](/2025/04/02)有个更复杂的例子：继承中的 public private 影响内存布局。

## 11. constexpr std::source_location::current 丢失模板信息

```cpp
#include <iostream>
#include <string_view>
#include <source_location>

template <class T>
constexpr std::string_view foo1() {
    constexpr auto tmp = std::source_location::current();
    return tmp.function_name();
}

template <class T>
constexpr std::string_view foo2() {
    auto tmp = std::source_location::current();
    return tmp.function_name();
}

int main() {
    std::cout << foo1<int>() << '\n';  // constexpr std::string_view foo1()
    std::cout << foo2<int>() << '\n';  // constexpr std::string_view foo2() [with T = int; std::string_view = std::basic_string_view<char>]
}
```

foo2 的 `std::source_location` 会尽可能反映调用点的信息，所以会把求值阶段推迟到实例化模板阶段以让 `function_name` 包含模板信息。

foo1 因为 `std::source_location` 不依赖模板参数，constexpr 就把求值时机提前了，自然在编译期丢失了模板信息。

## 12. Analyzing Computer System Performance with Perl PDQ（书）

群友的分享：

看完第一章了，这书和 perl 没啥关系，第一张分析的事怎么评估系统负载，吞吐量和延迟的关系。

第二章介绍了几个很老的性能采样工具，这段可以跳过，后面介绍了怎么评估负载率的采样结果是否满足泊松分布。

第三章讲了时间的一些概念，怎么理解时间，系统的时间戳，怎么精确计时，对响应时间的离散点怎么拟合成各种分布，一些特殊场景的响应时间统计，比如分布式服务器，可用性与停机时长的关系，故障率与可靠性，可靠性模型。

第四章讲了一堆排队论的基本概念，数学定义，little's law，并且通过几个版本的定律形式，推导出了单服务器系统，怎么用利用率以及平均服务时长计算任务的平均驻留时长，怎么用利用率计算平均队列长度，这样得到了怎么理解利用率这个指标的几个经验法则。然后把这些公式扩展到了多服务器系统，在多服务器系统上，高负载情况通过数学推理能够得到一些反直觉的结果。在这之后，给出了Erlang的C公式和B公式，用于更精确的分析多服务器系统高负载情况下的繁忙概率和丢弃任务的概率。用这些公式，可以估算系统要达到某个可用指标，应该怎么准确的扩容。后面补充介绍了几种服务器，实际上是轮询算法和任务流程。接下来推导了 PK 方程，指导怎么根据历史指标，计算每个队列的平均驻留时间，来辅助新的任务选择等待的队列，然后说了这个辅助决策的算法不如轮询。最后作者通用可拓展性定律之父介绍了通用可拓展性定律。

第五章开始考虑了多个计算机子系统的组合，比如硬盘 + 内存 + cpu，来分析多队列的情况，第四章的考虑的是多个相同性能的接口。

## 13. 一些文章

群主教写简历 直播回放 <https://www.bilibili.com/video/BV1BNtzz8E7A/>（虽然不是文章）

C++ 中文周刊 2025-08-11 第188期 <https://wanghenshui.github.io/cppweeklynews/posts/188.html>

高频相关，莫队交易赛的文章 <https://zhuanlan.zhihu.com/p/470766162>

理解与实现 SIMD 函数 <https://johnnysswlab.com/the-messy-reality-of-simd-vector-functions/>

c++有哪些开源的内存池值得学习?（文章）<https://www.zhihu.com/question/663670460/answer/1942914503420417900>

***

都看到这了，来关注一下败犬日报吧！

[主站](https://makeinu-daily.pages.dev/) | [知乎专栏](https://www.zhihu.com/column/c_1846629212653506560) | [微信公众号](https://makeinu-daily.pages.dev/img/wechat.png) | [RSS](https://makeinu-daily.pages.dev/feed.rss)
