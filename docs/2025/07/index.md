---
date: 2025-08-01
next:
  link: /2025/08
  text: 败犬のC++每月精选 2025-08
prev:
  link: /2025/06
  text: 败犬のC++每月精选 2025-06
title: 败犬のC++每月精选 2025-07
description: 本期日报包含 C++ 语言相关的多个话题，涉及语法特性、标准库、编译期行为、内存管理、面向对象编程等，同时收录了一些编程实践和文章推荐。
__tags__:
- title: '## 1. switch enum，每个枚举值都有 return 但是 MSVC 报 not all control paths return
    a value'
  score: 7/10
  tags:
  - C++
  - 语法特性
  - 基础知识
  - 需改进
  explanation: 讨论 switch 语句中枚举值处理的问题，涉及 std::unreachable 和枚举值的潜在范围，存在事实不全面的问题，需要补充完整解决方案。
- title: '## 2. C++ 和命名参数'
  score: 8/10
  tags:
  - C++
  - 语法特性
  - 工程实践
  - 进阶知识
  explanation: 探讨 C++ 中命名参数的实现方案，包括指派初始化和相关提案，涉及语法特性和工程实践，属于进阶知识。
- title: '## 3. 状态管理，用全局变量实现容易堆屎山'
  score: 7/10
  tags:
  - C++
  - 工程实践
  - 内存管理
  - 基础知识
  explanation: 讨论状态管理的实践，推荐使用 context 参数而非全局变量，涉及内存管理和工程实践，属于基础知识。
- title: '## 4. 变量名包含 `__LINE__` 的宏'
  score: 6/10
  tags:
  - C++
  - 预处理和宏
  - 基础知识
  explanation: 介绍宏拼接 `__LINE__` 的正确方法，涉及预处理和宏，属于基础知识。
- title: '## 5. 为什么虚表里的函数从第 2 项开始'
  score: 8/10
  tags:
  - C++
  - 面向对象编程
  - ABI
  - 进阶知识
  explanation: 解释虚函数表布局和 RTTI 的关系，涉及面向对象编程和 ABI，属于进阶知识。
- title: '## 6. const_cast 什么场景下必须用'
  score: 7/10
  tags:
  - C++
  - 语法特性
  - 类型
  - 基础知识
  explanation: 讨论 const_cast 的适用场景，包括接口兼容性和迭代器处理，涉及类型转换和语法特性，属于基础知识。
- title: '## 7. clang constexpr 过早实例化的问题'
  score: 7/10
  tags:
  - C++
  - 编译期
  - 语法特性
  - 专家知识
  - 需改进
  explanation: 分析 clang 在 constexpr 上下文中的模板实例化问题，涉及编译期行为和语法特性，属于专家知识，存在事实不全面的问题。
- title: '## 8. GCC/Clang 模板语境 lambda 是 dependent expression'
  score: 6/10
  tags:
  - C++
  - 语法特性
  - 泛型编程
  - 专家知识
  explanation: 讨论模板语境中 lambda 表达式被视为 dependent expression 的问题，涉及泛型编程和语法特性，属于专家知识。
- title: '## 9. 指针 `==` 在菱形继承下不能判断是同一对象'
  score: 7/10
  tags:
  - C++
  - 面向对象编程
  - 类型
  - 进阶知识
  explanation: 解释菱形继承中指针比较的歧义问题，涉及面向对象编程和类型系统，属于进阶知识。
- title: '## 10. 死代码需要清理吗'
  score: 6/10
  tags:
  - C++
  - 工程实践
  - 基础知识
  explanation: 讨论死代码清理的必要性，涉及工程实践，属于基础知识。
- title: '## 11. `std::string::c_str()` 的值移动后失效'
  score: 8/10
  tags:
  - C++
  - 内存管理
  - 标准库特性
  - 进阶知识
  explanation: 分析 std::string 移动后 c_str() 失效的问题，涉及内存管理和标准库特性，属于进阶知识。
- title: '## 12. 为什么没有 is_specialization 的模板工具'
  score: 7/10
  tags:
  - C++
  - 泛型编程
  - 元编程
  - 专家知识
  explanation: 探讨 C++ 中缺少 is_specialization 模板工具的原因，涉及泛型编程和元编程，属于专家知识。
- title: '## 13. 群友的名言警句'
  score: 6/10
  tags:
  - 工程实践
  - 其他
  explanation: 收录编程实践相关的名言警句，涉及工程实践，属于其他话题。
- title: '## 14. 一些文章'
  score: 7/10
  tags:
  - 工程实践
  - 性能优化
  - 其他
  explanation: 推荐多篇编程相关文章，涉及工程实践和性能优化，属于其他话题。
---

![img](/img/2025-07-index.webp)

# 败犬のC++每月精选 2025-07

[[toc]]

## 1. switch enum，每个枚举值都有 return 但是 MSVC 报 not all control paths return a value

```cpp
enum class E { A, B, C };

int foo(E e) {
    switch (e) {
        case E::A:
        case E::B:
        case E::C:
            return 1;
    }
}
```

可以在 default（或函数末尾）里写 `std::unreachable()`。如果 C++23 之前可以自己写一个：

```cpp
[[noreturn]]
inline void unreachable() {}
```

虽然这是 MSVC 独有，但是事实上标准允许 enum 的值不在“命名枚举值”的范围内，还是要注意的（最好写 default return）。<https://en.cppreference.com/w/cpp/language/enum.html> 有记载：

> Values of integer, floating-point, and enumeration types can be converted to any enumeration type by using static_cast. Note that the value after such conversion may not necessarily equal any of the named enumerators defined for the enumeration: ...
>
> 翻译：整型、浮点型和枚举类型的值可以通过使用 static_cast 转换为任何枚举类型。请注意，这种转换后的值不一定等于枚举定义的任何命名枚举器：...

## 2. C++ 和命名参数

现在 C++ 的语法允许函数声明之间的形参名不同，比如：

```cpp
void foo(int a, int b);
void foo(int b, int a);
```

所以如果要支持命名参数，不能直接在现有语法上加，肯定要增加新的关键字或符号。现有方案“又不是不能用”。

《C++ 的设计与演化》是这么说的：

> C++ 是面向对象的语言，所以决定不提供这个功能。你的参数如果需要这么写，那请打包成一个对象。

但是这和面向对象没什么关系（C++ 是多范式语言），正经人都不喜欢啰嗦的 `FunBuilder.setA().setB().setC().build()`（更新，这个不啰嗦，啰嗦的是 setter 定义）。

***

那么推荐做法是什么呢？指派初始化。

```cpp
struct Args {
    int a;
    int b;
};

void foo(Args args);

foo({.a = 0, .b = 1});
```

这个指派初始化是 C++20 的，20 之前使用也没什么问题（编译器扩展）。

但是有个缺点是参数必须按顺序初始化。这个需求有一个 linter 下位替代，clang-tidy 的 bugprone-argument-comment。如果要允许乱序的话问题有点大，主要是求值顺序的问题（实参的求值顺序和形参初始化的顺序）。详见乱序指派初始化提案 <https://wg21.link/p3405>。

最后还有个炫技的命名参数实现 <https://godbolt.org/z/16EWPnxfT>（看一乐）。

## 3. 状态管理，用全局变量实现容易堆屎山

大家的共识是函数参数传 context。

但是如果整个程序用同一个 context 也会堆屎山，要保证 context 被使用的范围足够小。

还有 context 的一个问题是成员的生命周期，什么时候有值，什么时候没有值。一般只能靠注释，没有别的好办法。

## 4. 变量名包含 `__LINE__` 的宏

直接这么写是不对的：

```cpp
#define macro(x) int x_##__LINE__ = 0

int main() {
    macro(x);  // int x____LINE__ = 0;
}
```

要给这 x 和 `__LINE__` 套两个宏再拼接：

```cpp
#define CONCAT1(x, line) x##line
#define CONCAT(x, line) CONCAT1(x, line)
#define macro(x) int CONCAT(x, __LINE__) = 0

int main() {
    macro(x);  // int x6 = 0;
}
```

## 5. RTTI 和虚表布局

一般实现上 RTTI 指针在 `vptr[-1]` 的位置。

关了 RTTI 的话，RTTI 指针填的是 0 或 dummy typeinfo。这是为了让 RTTI 不影响 ABI，没开 RTTI 和 开了 的链接到一起也没事，只要没访问 RTTI 仅虚函数调用是没问题的。

还有另外一个问题，为什么 RTTI 不和虚表放一起，而是间接寻址（类似指针）的方式访问？原因是一样的。如果 RTTI 信息和虚表放一起，开关 RTTI 会影响虚表布局。

## 6. const_cast 什么场景下必须用

一种是上游或下游不提供非 const 接口，需要手动转换。

还有 iterator 或 span 有时会遇到。例如写 hash_map find，会有返回 iterator 和 const_iterator 两个版本，const 版本可以直接 `const_iterator{const_cast<T*>(this)->find(key)}`。

## 7. clang constexpr 过早实例化的问题

```cpp
#include <memory>

struct B;

struct A {
    std::unique_ptr<B> b = nullptr;
};

struct B {};
```

这个代码在 clang `-std=c++23` 报错，把标准降到 20 不会。

这是 clang 的一个老问题，`std::unique_ptr<B>` 的析构函数在 C++23 变成了 constexpr，在 `struct B {};` 前实例化（过早实例化），于是要求 B 是一个完整类型。这也能解释 20 前就不会报错。

有些编译器把函数模板实例化放到 TU（翻译单元）结束，也就是 `struct B {};` 后，这样可以不报错。不过这是个 IFNDR (ill-formed no diagnostic required)，实例化位置和顺序标准显然没有规定的。ref <https://timsong-cpp.github.io/cppwp/n4659/temp.point#8>

一个几乎一样的问题：<https://github.com/llvm/llvm-project/issues/111185>

但是还有一个现象是 `std::unique_ptr<B> b = nullptr;` 改成 `std::unique_ptr<B> b{nullptr};` 就不会报错了。虽然两者选择的都是 `unique_ptr(nullptr_t)` 构造函数（为什么 `=` 没有复制，因为 C++17 强制复制消除），但是 clang 实现有细微区别，多了个隐式转换，`{}` 不接受类型窄化就不需要。具体还得看 clang 源码。

## 8. GCC/Clang 模板语境 lambda 是 dependent expression

```cpp
#include <bits/stdc++.h>

template <typename T>
class Switch {
   private:
    T value_;

   public:
    explicit Switch(T value) : value_(value) {}

    template <typename U, typename Fn>
    Switch& Case(Fn&& fn) {
        return *this;
    }
};

int main() {
    // Regular lambda
    auto regularLambda = [](int value) {
        Switch<int>(value)
            .Case<int>([]() {})     // OK: no template keyword needed
            .Case<float>([]() {});  // OK: no template keyword needed
    };

    // Generic lambda
    auto genericLambda = [](auto value) {
        Switch<int>(value)
            .Case<int>([]() {})     // OK: first call works
            .Case<float>([]() {});  // REQUIRED: template keyword needed
    };
}
```

`[](auto value) { ... }` 内部是模板语境，Clang 把模板语境的 lambda（第一个 `[]() {}`）当成 dependent expression，导致 `Switch<int>(value).Case<int>([]() {})` 这个表达式也变成 dependent expression。

删掉 `.Case<int>([]() {})` 或 `.Case<float>([]() {})` 都可以过编译。

不过 MSVC 能过编译。

## 9. 指针 `==` 在菱形继承下不能判断是同一对象

一般来说，判断指针相同可以直接 `==`，因为编译期基类地址对于子类的偏移是确定的（偏移不为 0 的情况是多继承、有虚函数类继承无虚函数类）。

```cpp
#include <cstdio>

struct Base1 {
    int data0;
};
struct Base2 {
    int data1;
};
struct Derived : Base1, Base2 {};

int main() {
    Derived d;
    Derived* derived_ptr = &d;
    Base1* base1_ptr = &d;
    Base2* base2_ptr = &d;

    printf("%p %p %p\n", derived_ptr, base1_ptr, base2_ptr);  // 可能输出 0x7ffcdf034dcc 0x7ffcdf034dcc 0x7ffcdf034dd0
    printf("%d %d\n", derived_ptr == base1_ptr, derived_ptr == base2_ptr);  // 输出 1 1
}
```

但是菱形继承是不行的，因为子类包含了多个基类（类型相同但是地址不同），就会有歧义。

```cpp
#include <cstdio>

struct Base0 {};
struct Base1 : Base0 {
    int data0;
};
struct Base2 : Base0 {
    int data1;
};
struct Derived : Base1, Base2 {};

int main() {
    Derived d;
    Derived* derived_ptr = &d;
    Base0* base0_ptr = static_cast<Base1*>(&d);

    printf("%d\n", derived_ptr == base0_ptr);  // error: 'Base0' is an ambiguous base of 'Derived'
}
```

## 10. 死代码需要清理吗

例如：

```cpp
if (condition) {
    return res;
    break;  // 永远不会执行
}
```

要清理。没啥大毛病，只是 error-prone，就是反向推测你可能想实现的是别的逻辑，但是写错了。

## 11. `std::string::c_str()` 的值移动后失效

```cpp
#include <cstdio>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> a{"123"};
    auto p = a[0].c_str();
    printf("%s\n", a[0].c_str());  // 输出 123
    a.push_back("456");
    printf("%s\n", a[0].c_str());  // 输出 123
    printf("%s\n", p);             // 可能没有输出（GCC 15.1 不加编译参数）
    return 0;
}
```

SSO（小字符串优化）导致的。

按照标准的话，用来移动构造其他对象的 string，所有迭代器和指针都失效了。所以即使不满足 SSO 也不要这么用。

由此看出，用 `vector<string>` 当作 pool 容易触发这个问题，所以更好的实践是整个 `std::hive` 类似的对象池。

与之不同的是，`std::vector::data()` 的值移动后不会失效，<https://zh.cppreference.com/w/cpp/container/vector/vector.html> 的 Notes 章节。

## 12. 为什么没有 is_specialization 的模板工具

提案 <https://wg21.link/P2098R0> 被搁置了，原因是不够通用，没法完美地处理类型参数 + 非类型参数 + 模板模板参数的排列组合。

例如，找不到这么一个 is_specialization_of 的定义：

```cpp
template <typename T, template </* 这里填啥能同时满足下面的要求 */> typename Template> is_specialization_of {};
using T1 = is_specialization_of<std::array<int, 1>, std::array>;
using T2 = is_specialization_of<std::vector<int>, std::vector>;
```

[往期](/2025/05/24)提到的 universal template 提案可以处理这个问题，但是也没过。

C++26 反射能解决，但是模板参数类型得是反射得到的类型（std::meta::info），不能直接填类型和模板。

***

如果只考虑类型模板参数，可以这么写：

```cpp
template <class, template <class...> class>
constexpr bool is_specialization_of_v = false;
template <template <class...> class ClassTmpl, class... Ts>
constexpr bool is_specialization_of_v<ClassTmpl<Ts...>, ClassTmpl> = true;
```

## 13. 群友的名言警句

保持对最佳实践的敏感真的很重要。问题可能千奇百怪，但如果团队平时就尽量去追求最佳实践，那很多都是可以避免的。—— bincat

做项目不是说会调几个库跑个 mvp 出来就行了，出现问题了你得会定位，某些情况下你得自己编下库把断点打到那里，你如果没有通用的相对 low level 的知识，效率会很低。—— hiki

## 14. 一些文章

Don't ask to ask, just ask <https://dontasktoask.com/>

jemalloc 生平，原文 <https://jasone.github.io/2025/06/12/jemalloc-postmortem/> 翻译 <https://zclll.com/index.php/default/jemalloc-postmortem.html>

性能优化的一个完整过程 <https://www.zhihu.com/question/486847589/answer/1925001370940990828>

大脑根本扛不住“频繁决策”：为什么聪明人都在练习“决策节约”？<https://mp.weixin.qq.com/s/32cXjx6Enn9OKUnmJqhcfg>

A Programmer's Reading List <https://www.piglei.com/articles/en-programmer-reading-list-part-one/>

洞悉C++函数重载决议 <https://zhuanlan.zhihu.com/p/561977606>
