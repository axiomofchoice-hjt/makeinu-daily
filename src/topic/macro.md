---
date: 2025-09-18
next: false
prev: false
title: 败犬のC++专题 宏魔法篇
---

# 败犬のC++专题 宏魔法篇

[[toc]]

## 1. 前置知识

本文假设你已经了解：

1. 定义和使用宏。
2. `#ifdef` 等条件编译指令。
3. 预定义宏，如 `__FILE__` `__LINE__`。
4. `#` `##` 运算符。
5. 宏的可变参数 `...` 和 `__VA_ARGS__`。

## 2. 宏展开规则

参考文章：[C语言 宏嵌套的展开规则 - 彷徨而立的文章 - 知乎](https://zhuanlan.zhihu.com/p/344240420)

简单来讲是三条规则：

1. 外层宏的定义包含 `#` `##` 运算符，优先展开外层宏。
2. 外层宏的定义不包含 `#` `##` 运算符，优先展开内层宏。
3. 禁止递归：宏展开后，忽略这个宏。

宏展开规则在 [cppref](https://en.cppreference.com/w/cpp/preprocessor/replace) Scanning and Replacement 章节可以验证。

## 3. 宏展开规则举例：行号 `__LINE__` 的字符串形式

我们知道 `__LINE__` 会替换为数字，`#` 可以转换为字符串，但是不能 `#define LINE_STR #__LINE__`（因为 `#` 运算符只作用于形参）。

于是稍作调整：

```cpp
#include <iostream>

#define TO_STRING(x) #x
#define LINE_STR TO_STRING(__LINE__)

int main() {
    std::cout << LINE_STR << std::endl;  // LINE_STR 替换为 "__LINE__"
}
```

没错这样也不行。根据宏展开规则，`LINE_STR` 会替换为 `TO_STRING(__LINE__)`，由于 `TO_STRING` 的定义里包含了 `#` 运算符，所以直接会展开成 `"__LINE__"`。

相信大家读到这就会了，那就是套两层，把 `#` 运算符藏起来就好了：

```cpp
#include <iostream>

#define TO_STRING_(x) #x
#define TO_STRING(x) TO_STRING_(x)
#define LINE_STR TO_STRING(__LINE__)

int main() {
    std::cout << LINE_STR << std::endl;  // LINE_STR 替换为 "8"
}
```

## 4. 宏展开规则举例：变量名包含 `__LINE__` 的宏

这个例子也是类似的。直接这么写是不对的：

```cpp
#define macro(x) int x_##__LINE__ = 0

int main() {
    macro(x);  // 替换为 int x____LINE__ = 0;
}
```

答案是套两层：

```cpp
#define CONCAT_(x, y) x##y
#define CONCAT(x, y) CONCAT_(x, y)
#define macro(x) int CONCAT(x, __LINE__) = 0

int main() {
    macro(x);  // int x3 = 0;
}
```

## 5. 使用宏时，参数里有逗号

`MACRO(std::array<int, 2>)`，会被当成两个参数 `std::array<int` 和 `2>`。

一般可以套个小括号搞定 `MACRO((std::array<int, 2>))`。

如果搞不定，就要用 boost 的宏 `BOOST_IDENTITY_TYPE`（或者参考它的实现）。

## 6. 宏魔法之 for

实现 `TEST(n, f)` 展开为 `f(1), f(2), ..., f(n)`。

这个东西用模版做最合适。如果只能用宏，可以用拼接的方式：

```cpp
#define TEST1(f) f(1)
#define TEST2(f) TEST1(f), f(2)
#define TEST3(f) TEST2(f), f(3)
#define TEST4(f) TEST3(f), f(4)

#define TEST(n, f) TEST##n(f)

extern int f(int);

int g() {
    TEST(4, f);
}
```

还可以借助 boost 实现：<https://godbolt.org/z/387nbc419>

## 7. include 的参数可以是宏

include 的参数可以是宏，可以写成 `#include H_XX` 然后用编译参数传入 `H_XX` 宏。

## 8. 下划线占位符

下划线占位符是 C++26 的语法 <https://wg21.link/p2169>，一个作用是忽略结构化绑定的部分参数：

```cpp
void foo() {
    int _ = 0;
    auto [_, x] = std::make_pair(1, 2);
}
```

这个功能一定程度上可以用宏代替，没错就是用编译器扩展 `__COUNTER__`：

```cpp
#define CONCAT(l, r) l##r
#define IGNORE(count) CONCAT(IGNORE_, count)
#define _ IGNORE(__COUNTER__)

void foo() {
    int _ = 0;
    auto [_, x] = std::make_pair(1, 2);
}
```

## 9. x-macro 和头文件结合

## 10. 根据参数个数的分发

C 语言，有没有办法让 `f(1)` 调用函数 `f1`，`f(1, 2)` 调用函数 `f2` 呢？有的兄弟，有的。这是一段 [linux 的代码](https://github.com/torvalds/linux/blob/d51e783c17bab0c139bf78d6bd9d1f66673f7903/include/linux/args.h)

```cpp
#define __COUNT_ARGS(_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15, _n, X...) _n
#define COUNT_ARGS(X...) __COUNT_ARGS(, ##X, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
```

虽然有上限，不够完美，但很多时候够了。基于这个和上文提到的 CONCAT，我们可以完成如下操作：

```cpp
#include <iostream>

#define CONCAT_(x, y) x##y
#define CONCAT(x, y) CONCAT_(x, y)

#define __COUNT_ARGS(_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, \
                     _13, _14, _15, _n, ...)                                \
    _n
#define COUNT_ARGS(...)                                                        \
    __COUNT_ARGS(, ##__VA_ARGS__, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, \
                 2, 1, 0)

void f1(int a) { std::cout << "f1: " << a << std::endl; }
void f2(int a, int b) { std::cout << "f2: " << a << ", " << b << std::endl; }

#define f(...) CONCAT(f, COUNT_ARGS(__VA_ARGS__))(__VA_ARGS__)

int main() {
    f(1);     // 调用 f1(1)
    f(1, 2);  // 调用 f2(1, 2)
    return 0;
}
```

## 11. 写在最后

能力有限，只能讲几个宏的简单寄巧。[C/C++ 宏编程的艺术 - BOT Man的文章 - 知乎](https://zhuanlan.zhihu.com/p/152354031) 这篇文章讲到更多魔法，包括符号匹配、数值运算等，感兴趣的可以看看。

切记：“如果能不用宏，就不用宏”原则，除了必要场景，宏和任何其他方案对比，都是 0 优势纯劣势。工程代码尽可能优先用模板，然后是宏，最后是代码生成，从而保证代码的可维护性。
