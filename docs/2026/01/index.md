---
date: 2026/02/01
title: 败犬のC++每月精选 2026-01
next:
  link: /2026/02
  text: 败犬のC++每月精选 2026-02
prev:
  link: /2025/12
  text: 败犬のC++每月精选 2025-12
---

![img](/img/2026-01-index.webp)

# 败犬のC++每月精选 2026-01

[[toc]]

## 1. 面试题：memmove 怎么实现

memmove 是允许部分重叠的 memcpy，只要判断源和目标指针的大小，然后选择正向拷贝或反向拷贝，代码如下：

```cpp
void memmove(char* dst, const char* src, int n) {
    if (dst < src) {
        for (int i = 0; i < n; i++) {
            dst[i] = src[i];
        }
    } else {
        for (int i = n - 1; i != -1; i--) {
            dst[i] = src[i];
        }
    }
}
```

实测这两个简单的 for 循环，不论正向反向，都能编译器自动向量化，性能是没问题的。

往期讲过独立变量比较地址的结果未指定，这时候正向反向的效果都一样，所以 `dst < src` 是没问题的。

要改进代码可以判断 `dst == src` 就直接 return，如果完全不重合可以直接调用 memcpy。

## 2. 关于 container_of 的未定义行为

container_of 在 C 里有争议（但是广泛使用，不会出问题），但是 C++ 里是没有争议的 UB（但也是广泛使用）。

一般来说 container_of 定义是 `#define container_of(ptr, type, member) ((type *)((char *)(ptr) - offsetof(type, member)))`，UB 发生在指针减法（导致数组越界），[往期](/2025/11/24)聊过这个问题。

例如：

```cpp
struct A { int x, y, z; };

void unknown(int*);

bool foo() {
    A a{0, 1, 2};
    unknown(&a.y);

    return a.x == 0 && a.z == 2;  // 可能优化为永真，当然事实上不会这么优化
}
```

用 container_of 可以修改 x 字段的值，代码可以这么写：

```cpp
#define container_of(ptr, type, member) ((type *)((char *)(ptr) - offsetof(type, member)))

void unknown(int*y) {
    container_of(y, A, y)->x = 1;
}
```

## 3. 左值隐式转换后匹配到右值引用

这是一道 [cppquiz](https://cppquiz.org/q/x7qgf)：

```cpp
#include <iostream>

void f(float &&) { std::cout << "f"; }
void f(int &&) { std::cout << "i"; }

template <typename... T>
void g(T &&... v)
{
    (f(v), ...);
}

int main()
{
    g(1.0f, 2);
}
```

答案是输出 `if`，非常反直觉。

参数包展开为 `(f(v_0), f(v_1));` 这里从左到右求值没问题。关键在于 v 是具名的，是个左值，左值不能匹配右值引用，例如：

```cpp
void f(int&&);
int&& v = 114;
f(v);  // Rvalue reference to type 'int' cannot bind to lvalue of type 'int'
```

回到原问题，`float` 左值把 `f(float&&)` 的候选给移除了，在它视角下只有 `f(int&&)` 一个候选，只能先隐式转换成 `int` 纯右值，所以先输出了 "i"。另一边也同理，输出 "f"。

## 4. libstdc++ `unordered_map.clear()` 复杂度是错的

是关于桶数线性复杂度，而不是关于元素个数。

因为 unordered_map 的桶是惰性释放的（类似 `vector.clear()` 不释放内存），如果有很多桶再多次 `clear()` 会有明显性能问题。

这是 10 年前的问题 <https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67922>。人手不足的情况下，不重要的 bug 就是没时间处理的。别说 10 年，Clang 还有 15+ 年前提的 bug 没修。

没人手处理这些东西确实是个问题，刚刚有编译器小团体建议放慢标准吸纳新特性的速度 <https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3962r0.pdf>

## 5. 不同 TU 的同名 lambda 全局变量会报链接错误吗

这其实取决于编译器是否生成了符号。下面这个代码，用 GCC 10+ 编译可以得到符号 f。

```cpp
auto f = [] {};
```

`g++ test.cpp -c -o test.o && nm test.o` - `0000000000000000 B f`

Clang / GCC 9- 不生成符号，因为 lambda 只在内部使用，别的 TU 无法获得这个变量（这样的定义没办法写声明），就不需要生成符号。

由于 ODR 违背是 UB，那么有没有链接错误都是符合预期的。这里详细说明一下，链接属于实现层面，标准只定义了 ODR，违背这个规则就是 UB。标准不会规定具体符号怎么生成，链接怎么做。

***

我们换个思路让 Clang 生成符号，比如：

```cpp
inline auto g = [] {};
// extern decltype(g) f;
auto f = g;
```

虽然 f 还是 lambda 类型，但是 f 可以被声明成 `extern decltype(g) f;`，所以 Clang 不得不生成了符号 f。

## 6. 检查函数传参传错顺序

clang-tidy 有这个检查 <https://clang.llvm.org/extra/clang-tidy/checks/bugprone/easily-swappable-parameters.html>。

解决方法也很简单，把几个参数打包成一个结构体参数 xxxparams。

***

最近有一篇 C 语言提案 strong typedef，用来解决类似的问题。

<https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3320.htm>

```c
[[strong]] typedef int Width;
[[strong]] typedef int Height;
void draw_rect(Width w, Height h);

Width w = 3;
Height h = 4;
draw_rect(w, h);
// draw_rect(h, w);
```

不过这个提案放到 C++ 的问题很多 <https://discourse.llvm.org/t/rfc-clang-adding-strong-typedefs/88843>，不用期待了。

## 7. 踩坑之 `for (auto i = v.size() - 1; i >= 0; i--)`

这个代码的问题是 auto 推导出来是 size_t，所以 `i >= 0` 永真，死循环了。好在编译参数 `-Wextra` 也能发现问题 `warning: comparison of unsigned expression in ‘>= 0’ is always true [-Wtype-limits]`。

看到 `v.size() - 1` 的这个减法就应该警惕了，如果 `v.size() == 0`，i 初值就是很大的数，容易出问题。

第二个问题就是 auto 滥用了，不能一眼看出类型，直接写 `int64_t` 也不会麻烦多少。

## 8. benchmark 怎么阻止优化

DoNotOptimize 肯定是最佳实践，可以抄 google benchmark 的代码：

```cpp
template <class Tp>
inline BENCHMARK_ALWAYS_INLINE void DoNotOptimize(Tp&& value) {
#if defined(__clang__)
  asm volatile("" : "+r,m"(value) : : "memory");
#else
  asm volatile("" : "+m,r"(value) : : "memory");
#endif
}
```

然后看汇编对不对，如果耗时大的函数分离 TU 也行。

## 9. 编译期检查类的一些字段非空

一般来说可以用构造函数传递所有字段，从而保证非空。群友给了 builder + 模板的办法，不知道实用性如何（代码量大，建议在代码生成时使用）：

```cpp
#include <iostream>

struct A {
    int x;
    std::string y;
};

template <bool is_set_x = false, bool is_set_y = false, bool is_set_z = false>
struct A_Builder {
    static A_Builder<false, false, false> create() {
        return A_Builder<false, false, false>();
    }
    A_Builder<true, is_set_y, is_set_z> set_x(int x) {
        A_Builder<true, is_set_y, is_set_z> rhs;
        rhs.a_ = a_;
        rhs.a_.x = x;
        return rhs;
    }
    A_Builder<is_set_x, true, is_set_z> set_y(const std::string& y) {
        A_Builder<is_set_x, true, is_set_z> rhs;
        rhs.a_ = a_;
        rhs.a_.y = y;
        return rhs;
    }
    A build() {
        static_assert(is_set_x, "Field x is not set");
        static_assert(is_set_y, "Field y is not set");
        return a_;
    }

   private:
    template <bool Sx, bool Sy, bool Sz>
    friend struct A_Builder;
    A a_;
};

int main() {
    A a = A_Builder<>::create().set_x(42).set_y("Hello").build();
    std::cout << "A.x: " << a.x << ", A.y: " << a.y << std::endl;
}
```

也可以实现 `required<T>`，然后用聚合初始化：

```cpp
#include <iostream>

template <typename T>
struct required {
    T data;
    template <typename U>
    required(U&& data) : data(data) {}
};

struct A {
    int x;
    std::string y;
};

struct A_Builder {
    required<int> x;
    required<std::string> y;

    A build() { return A{std::move(x.data), std::move(y.data)}; }
};

int main() {
    A a = A_Builder{.x = 42, .y = "Hello"}.build();

    std::cout << "A.x: " << a.x << ", A.y: " << a.y << std::endl;
    return 0;
}
```

## 10. 推荐阅读

[打破黑盒：Linux共享内存内核实现全解析](https://mp.weixin.qq.com/s/YHxl4OSGL3X09wALcR8nfg)

[大模型的幻觉问题调研: LLM Hallucination Survey](https://zhuanlan.zhihu.com/p/642648601)

[C++20 Modules 用户视角下的最佳实践](https://chuanqixu9.github.io/c++/2025/12/30/C++20-Modules-Best-Practices.html)

[Bjarne Stroustrup：现代 C++ 的跨世纪演进（演讲全文）](https://zhuanlan.zhihu.com/p/1990476964423820269)，讲技术的部分有资源管理，基于概念的泛型编程，模块，核心指南。

[退役算法竞赛选手如何学习C++就业](https://zhuanlan.zhihu.com/p/1986922284506702637)

[How Terminals Work](https://how-terminals-work.vercel.app/)，带交互的博客，挺有意思。

[超越 lock-free 的是 wait-free](https://mp.weixin.qq.com/s/kDKkNVWqjPaSzmvOc4U-7Q)
