---
date: 2025-06-01
next: false
prev:
  link: /2025/04
  text: 败犬のC++每月精选 2025-04
title: 败犬のC++每月精选 2025-05
---

![img](/img/2025-05-index.png)

# 败犬のC++每月精选 2025-05

[[toc]]

本月的 C++ 话题速览！（2025-05）

## 1. char8_t 与严格别名的问题

### 1.1. 严格别名的一个例子

<https://godbolt.org/z/76Gznhd3c>

```cpp
#include <chrono>
#include <iostream>

void sum_with_aliasing(unsigned char* data, int& result) {
    for (int i = 0; i < 1000000; ++i) {
        result += data[0];
    }
}

void sum_without_aliasing(char8_t* data, int& result) {
    for (int i = 0; i < 1000000; ++i) {
        result += data[0];
    }
}
```

unsigned char 可以有别名，所以不能假设 data 和 result 内存不重叠；char8_t 就可以。

### 1.2. 编译器为什么假设 signed char 有别名

为了兼容 C。

C++ 允许别名的类型是 `char` `unsigned char` `std::byte`，C 是 `char` `unsigned char` `signed char`，这里有一些区别。编译器如果不做这个兼容，C 代码直接移植到 C++ 就寄了。

### 1.3. 为什么要有 char8_t

上面说了 char, unsigned char, signed char 都不能做严格别名优化，只有 char8_t 是独立类型。这样性能会好一些。

<https://www.zhihu.com/question/1904806645999047234/answer/1905396078708228989>

有一说一，这些类型确实很混乱。

## 2. Clang 16 不支持 `constexpr std::string`，到了 17 才支持

这里是解释：

<https://quuxplusone.github.io/blog/2023/09/08/constexpr-string-firewall/>

<https://quuxplusone.github.io/blog/2023/10/13/constexpr-string-round-2/>

而 GCC 至今仍不支持，是 GCC 的 SSO 的实现问题 <https://www.zhihu.com/question/643989678>。

## 3. `std::decay` 和 `std::remove_cvref` 有什么区别

只是移除 cvref 限定的话，没区别。（解释一下，cvref 指的是 const volatile 左值右值引用这几个的组合）

`std::decay` 是模拟 `auto x = (?);` 的推导结果，移除了 cvref 限定只是顺手的事，还会导致数组退化成指针、函数退化成指针。

`std::remove_cvref` 就是单纯的移除 cvref 限定。

所以易得它们的区别：

```cpp
static_assert(std::is_same_v<std::decay_t<int (&)[8]>, int*>);
static_assert(std::is_same_v<std::remove_cvref_t<int (&)[8]>, int[8]>);
```

## 4. 模板编程和模板元编程

一般语境下，模板元编程是“高级”的模板科技（例如编译期计算），为了和用于泛型的模板区分。

发明模板的本意其实也只是一个泛型，元编程是人们发掘出来的 tricky 的用法，被扶正、提供了丰富的标准库支持。

## 5. `const T&` 返回函数中的不具名对象，能不能延长生命周期

```cpp
const std::string &foo() {
    return "A";
    // warning: returning reference to local temporary object
}
```

不能，对象会在函数里析构。

关于返回值生命周期，可以想想调用方和被调用方会不会析构这个对象，就明白了。返回引用，调用方不析构，否则下面代码的全局变量 s 就会出问题：

```cpp
std::string s;
const std::string &foo2() {
    return s;
}
```

所以函数内的不具名对象显然是被调用方负责析构，返回值就会变成悬垂引用。

***

延伸：

1. RVO 的返回值不是引用，调用方会接管生命周期。
2. `T &&foo() { return T{}; }` 也会导致悬垂引用。（更新：原来是“临时量实质化 `T &&foo() { return T{}; }`，生命周期也会交给调用方。”，错误的，这不是临时量实质化）

## 6. 判断一个类型的特定成员函数的返回值类型，但是没法构造这个类型

具体地说，有个模板参数 A，要求 A 存在一个成员函数 `Y operator()(X&)`，X 和 Y 都是具体类型。

可以用 declval：

```cpp
std::is_same_v<Y, decltype(declval<A>()(declval<X&>()))>
```

C++20 可以更简单：

```cpp
requires (A a, X x) {
  { a(x) } -> std::same_as<Y>;
}
```

## 7. parameter 和 argument 的区别

茴香豆问题。虽然定义上 parameter 是形参，argument 是实参，但是很多时候都混用（只有同时出现两者才需要区分）。

比如 <https://eel.is/c++draft/func.wrap.func.general> 里是这样的：

```cpp
template<class R, class... ArgTypes>
  function(R(*)(ArgTypes...)) -> function<R(ArgTypes...)>;
```

这里的 ArgTypes 很显然是形参类型。

<https://docs.python.org/3/faq/programming.html#what-is-the-difference-between-arguments-and-parameters> python 文档里看似区分了两者，但是它说 "kwargs are parameters"：

> foo, bar and kwargs are parameters of func.

## 8. 代码鉴赏：文件拆成两半

```cpp
#include "foo_head.h" // void foo() {
bar();
#include "foo_tail.h" // }
```

逆天代码，不仅可读性差，clangd / format 工具也寄了。

正确做法，定义宏再 include：

```cpp
#define CONTENT bar();
#include "foo.h" // void foo() { CONTENT; }
```

另一种是定义头尾宏：

```cpp
#include "foo.h" // #define FOO_HEAD void foo() {
                 // #define FOO_TAIL }
FOO_HEAD
bar();
FOO_TAIL
```

## 9. C++17 实现无参数的 lambda template

C++20 才有 lambda template：

```cpp
auto lambda = []<typename T>() {
    // use T
};
lambda.operator()<int>();  // 更新：原来的 lambda<int>(); 会编译错误
lambda.operator()<float>();  // 更新：原来的 lambda<float>(); 会编译错误
```

可以手写 std::type_identity（这个也是 C++20 的，但可以自己搓）：

```cpp
auto lambda = [](auto T) {
    // use decltype(T)::type
};
```

## 10. delete this

这个语法提供了紫砂的能力。

delete this 之后不做任何跟 this 相关的事就没事，不过一般都是直接退出那个函数。

场景是什么？引用计数清零要干掉自己的时候。

## 11. 继承标准库的类是不是未定义行为

不是未定义行为哦，不要被网上的说法骗了。

`std::enable_shared_from_this` 的用法就是继承。

继承 `std::istream` `std::ostream` 用来表示自己是个 IO 流。

***

就算继承 `std::vector` 这种也没问题，不过用的可能不多。

<https://www.zhihu.com/question/266674915/answer/3111080042> 有记载：

> 没什么不能用的。标准规定这些容器不允许带final标识符就是让你可以继承这些容器。

***

都看到这了，来关注一下败犬日报吧！

[主站](https://makeinu-daily.pages.dev/) | [知乎专栏](https://www.zhihu.com/column/c_1846629212653506560) | [微信公众号](https://makeinu-daily.pages.dev/img/wechat.png) | [RSS](https://makeinu-daily.pages.dev/feed.rss)
