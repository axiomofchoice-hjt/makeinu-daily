---
date: 2025-10-01
next: false
prev:
  link: /2025/08
  text: 败犬のC++每月精选 2025-08
title: 败犬のC++每月精选 2025-09
description: 本期日报包含 C++ 哈希表设计、标准库特性、语言特性、编程实践等多个话题
__tags__:
- title: '## 1. 哈希表怎么设计'
  score: 8/10
  tags:
  - C++
  - STL
  - 性能优化
  - 工程实践
  - 进阶知识
  explanation: 讨论哈希表设计和高性能实现，对比 C++ unordered_map 与 ClickHouse 的实现，涉及性能优化和工程实践，属于进阶知识。
- title: '## 2. std::accumulate 的类型设计失误'
  score: 7/10
  tags:
  - C++
  - 标准库特性
  - STL
  - 基础知识
  - 需改进
  explanation: 指出 std::accumulate 因返回值类型由初始值决定而易出错，对比 ranges::fold_left 的设计，属于基础知识。需改进：文章可更详细说明解决方案。
- title: '## 3. `std::unordered_map<int*, int>` 不能传常量指针'
  score: 6/10
  tags:
  - C++
  - STL
  - 标准库特性
  - 语法特性
  - 进阶知识
  explanation: 解决 std::unordered_map 使用常量指针的问题，介绍 const_cast 和透明查找方法，涉及语法特性和标准库特性，属于进阶知识。
- title: '## 4. 怎么搞出 sizeof 是 0 的类型'
  score: 5/10
  tags:
  - C++
  - 语法特性
  - 内存管理
  - 基础知识
  - 需改进
  explanation: 探讨 C++ 中 sizeof 为 0 的类型，指出标准不允许且依赖编译器扩展，属于基础知识。需改进：文章未充分解释标准要求和实际限制。
- title: '## 5. Concept-Model Idiom 非侵入式多态'
  score: 7/10
  tags:
  - C++
  - 泛型编程
  - 工程实践
  - 进阶知识
  explanation: 介绍 Concept-Model Idiom 实现非侵入式多态，推荐使用 proxy 库简化代码，涉及泛型编程和工程实践，属于进阶知识。
- title: '## 6. `[[no_unique_address]]` C++20'
  score: 8/10
  tags:
  - C++
  - 语法特性
  - 内存管理
  - 进阶知识
  explanation: 讲解 C++20 的 [[no_unique_address]] 特性，允许成员变量地址重叠，优化空类存储，涉及内存管理和语法特性，属于进阶知识。
- title: '## 7. 锐评 `if (flag) { res = 0.0; }` 和 `res = static_cast<double>(!flag)
    * res;`'
  score: 9/10
  tags:
  - C++
  - 工程实践
  - 性能优化
  - 基础知识
  - 内容较主观
  explanation: 对比两种代码写法，强调可读性优先，讨论分支和乘法性能，引用 Donald Knuth 名言，涉及工程实践和性能优化，属于基础知识。内容较主观：包含作者个人观点。
- title: '## 8. 参数包后面塞默认实参的问题 - 推导指引'
  score: 7/10
  tags:
  - C++
  - 语法特性
  - 标准库特性
  - 进阶知识
  explanation: 解决参数包与默认实参（如 source_location）结合的问题，使用推导指引实现，涉及语法特性和标准库特性，属于进阶知识。
- title: '## 9. 能不能限制一个类型只能创建临时对象，禁止具名'
  score: 6/10
  tags:
  - C++
  - 语法特性
  - 内存管理
  - 专家知识
  - 需改进
  explanation: 探讨限制类型只能创建临时对象的方法，指出常见错误和形参生命周期方案，涉及内存管理和语法特性，属于专家知识。需改进：方案依赖实现定义行为，不够稳健。
- title: '## 10. 为什么有符号整数溢出是未定义行为'
  score: 8/10
  tags:
  - C++
  - 语法特性
  - 基础知识
  explanation: 解释有符号整数溢出为 UB 的原因，包括编译器优化和硬件差异，引用外部文章补充，涉及语法特性，属于基础知识。
- title: '## 11. 一些文章'
  score: 7/10
  tags:
  - C++
  - 其他
  - 基础知识
  - 内容较主观
  explanation: 推荐多篇外部文章，涵盖提问技巧、gcc patch、AI 新闻等，主题多样，属于基础知识。内容较主观：选择文章体现作者偏好。
---

![img](/img/2025-09-index.png)

# 败犬のC++每月精选 2025-09

[[toc]]

## 1. 哈希表怎么设计

像 C++ unordered_map 的链表法、java 的链表转红黑树，都走偏了。高性能哈希表的方向完全不是这样，在链表法上雕花显然不会增加访存局部性。

工程上哈希表的设计可以看 <https://zclll.com/index.php/doris/hashtable_in_clickhouse.html>。

## 2. std::accumulate 的类型设计失误

```cpp
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    std::vector<double> a{1, 1.5};
    auto res = std::accumulate(a.begin(), a.end(), 0);
    std::cout << res << std::endl;  // 输出 2
}
```

std::accumulate 返回值的类型是由初始值决定的，所以希望得到 double 的时候传了 0 就会寄。

ranges::fold_left 就很正确，它的返回值类型是 auto。都是左折叠，所以 std::accumulate 算设计失误。

这个坑太容易踩了。

***

为什么不要求和迭代器类型一致，可能是允许更灵活的操作，比如：

```cpp
std::vector<char> v{'a', 'b', 'c'};
std::accumulate(v.begin(), v.end(), std::string{});
```

## 3. `std::unordered_map<int*, int>` 不能传常量指针

```cpp
void foo(std::unordered_map<int*, int> &m, const int* key) {
    m.find(key);  // 报错
    m.find(const_cast<int*>(key));
}
```

如果不能改 unordered_map 的类型，就只能每次都 const_cast 了。

如果能改，最简单的做法是 `std::unordered_map<const int*, int>`。

也可以加透明查找，但是问题是：

1. 需要 C++20。
2. 得自己写一个资瓷 transparent hash 的工具类。
3. 有一个理论的问题，标准没有保证 `std::hash<int*>{}(ptr) == std::hash<const int*>{}(ptr)` 始终为 true，实际上应该能跑。

代码如下：

```cpp
struct MyTransparentHash {
    using is_transparent = void;

    template<typename T>
    auto operator()(const T& x) const {
        return std::hash<T>{}(x);
    }
};

void foo(std::unordered_map<int*, int, MyTransparentHash, std::equal_to<>>& map,
         const int* key) {
    map.find(key);
}
```

## 4. 怎么搞出 sizeof 是 0 的类型

C++ 不存在这个东西。标准不允许两个对象地址相同（更新：是两个同类型的独立对象），如果 `sizeof(T)` 是 0，定义数组 `T a[2];` 就会有 `a[0] a[1]` 的地址相同，违背了要求。

```cpp
#include <iostream>

struct A {
    int a[0];  // warning: ISO C++ forbids zero-size array ‘a’
};

int main() {
    std::cout << sizeof(A) << std::endl;
}
```

这个用 GCC 编译确实输出 0，但是这是编译器扩展（柔性数组）。而且 MSVC 输出是 4。

## 5. Concept-Model Idiom 非侵入式多态

<https://gracicot.github.io/conceptmodel/2017/09/13/concept-model-part1.html>

如果自己实现还是要写一堆，直接用 proxy 库就可以自动生成了。

## 6. `[[no_unique_address]]` C++20

允许成员变量和其他成员变量的地址重叠。

```cpp
struct Empty {};
struct A {
    [[no_unique_address]] Empty e;
    int x;
};
```

这里的 e 的 size 还是 1，只是允许重叠，A 的 size 就可以是 4。`[[no_unique_address]]` 只是“允许”，不是强制，虽然实际没问题。

什么时候要用到空类成员呢？主要是想要这个空类的行为。往期就讲过 `std::unique_ptr` 的 Deleter 可以被空基类优化掉，还有 `std::vector` 的 Allocator。空基类优化是为了 C++17 及之前也能用，有了 no_unique_address 写法上可以直观一点。

## 7. 锐评 `if (flag) { res = 0.0; }` 和 `res = static_cast<double>(!flag) * res;`

起因是群友同事不好好写代码，把 `if (flag) { res = 0.0; }` 写成 `res = static_cast<double>(!flag) * res;`。

简单来说就是可读性优先，选择第一种或者三目 `res = flag ? 0 : res;` 都可以接受。功能上如果 res = inf / nan 乘法会寄。虽然有分支，但是性能不会有很大差别，没必要抠这点性能。

过早的优化是万恶之源。—— Donald Knuth 等人, 1974

***

虽然没必要抠性能，但架不住很有意思啊。

我们知道分支惩罚是大概 15-20 个 CPU 周期，常见 CPU double 乘法的 latency 是 4 个，分支命中率至少 75% 才能性能接近。这就取决于程序是否分支友好（例如矩阵乘能有很高的命中率，而排序就不行）。

这里可能有人要说，三目运算符不是可以优化为 cmov 吗，为什么还有分支。这就不得不提 x86 cmov 只支持通用寄存器。

虽然 sse 有 blend 指令可以替代，也可以 mov 到通用寄存器 cmov，但是试了一下编译器（GCC）似乎强烈地倾向于使用分支。即使我手动写了 `std::bit_cast`，以及其他很多方法都不行，只有手动写 sse 内置函数和内嵌汇编可以。这块我打算另写一个文章，可以期待一下。（文章已完成 <https://zhuanlan.zhihu.com/p/1958574956985156706>）

## 8. 参数包后面塞默认实参的问题 - 推导指引

众所周知 source_location 是默认实参传递的，在此基础上怎么实现参数包？其实只要写一个推导指引即可：

```cpp
#include <format>
#include <print>
#include <source_location>

template <typename... Args>
struct Logger {
    Logger([[maybe_unused]] Args&&... args,
           std::source_location loc = std::source_location::current()) {
        std::print("{}:{}:{}: ", loc.file_name(), loc.line(), loc.column());
        (std::print("{}", std::forward<Args>(args)), ...);
        std::println();
    }
};

template <typename... Args>
Logger(Args...) -> Logger<Args...>;

int main() { Logger("Hello world", 123); }
```

日志 + 参数包 + source_location 的完整代码可以在这里获取 <https://github.com/clice-io/clice/blob/main/include/Support/Logging.h>。

## 9. 能不能限制一个类型只能创建临时对象，禁止具名

相关提问：<https://www.zhihu.com/question/667304681>

不能。一个常见错误是构造 private + `T&& create();`，这样是悬垂引用（因为函数内变量或对象的生命周期在函数里）：

```cpp
struct A {
   private:
    A() {}

   public:
    static A&& create() {
        return A{};  // warning: returning reference to temporary
    }
    static A&& create_v2() {
        A a;
        return a;  // warning: reference to local variable ‘a’ returned
    }
};
```

单例模式 `T& create();` 不是临时对象，不符合要求。

一旦 `T create();` 就允许具名了（这个叫静态工厂方法）。

综上，无解。views 那堆东西也是这样，要自己保证不悬垂。

***

kedixa 的评论提供了个方法，用形参生命周期来解决悬垂的问题，代码如下。这可能是最接近的答案，唯一不足的是形参的生命周期是在函数末尾结束还是在全表达式末尾结束，这个东西是实现定义的。实现定义，就是如果编译器有保障，那就没问题（跨平台 / 编译器的代码就不太推荐了）。

```cpp
#include <cstdio>

struct A {
   private:
    A() {}

   public:
    static A&& create(A&& a = A{}) { return a; }

    void f() { std::puts("A::f()"); }
};

int main() {
    A::create().f();
}
```

## 10. 为什么有符号整数溢出是未定义行为

规定有符号整数溢出是 UB 可以让编译器做一些优化，比如假设 x + 1 > x 恒为真。

还有 lancern 佬的文章 <https://zhuanlan.zhihu.com/p/391088391> 写的：

> 举例来说，在大部分 CPU 上，有符号整数的溢出是一个 perfectly well-defined behavior；然而，在某些 CPU 芯片上，有符号整数的溢出却会导致 trap。

## 11. 一些文章

如何科学地提问 <https://ysyx.oscc.cc/docs/2407/f/1.html>

记一次有趣的 gcc patch 经历 <https://zhuanlan.zhihu.com/p/1948533594613094277>

刚刚，OpenAI/Gemini共斩ICPC 2025金牌！OpenAI满分碾压横扫全场 <https://mp.weixin.qq.com/s/qjsW2JDhvKQ5G9cylyDZxw>

通过 perf 使用 uprobe <https://zhuanlan.zhihu.com/p/1953361810494292001>

C++ 关于 concept 与 type traits 的优劣是什么？<https://www.zhihu.com/question/542280815/answer/2586569800>

C++ 冰山图 <https://victorpoughon.github.io/cppiceberg/>

认为AI是泡沫的人，需再次领教一下指数的威力 <https://mp.weixin.qq.com/s/TUu5axavU2IzBF8IEbvP_w>
