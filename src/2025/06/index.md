---
date: 2025-07-01
next:
  link: /2025/07
  text: 败犬のC++每月精选 2025-07
prev:
  link: /2025/05
  text: 败犬のC++每月精选 2025-05
title: 败犬のC++每月精选 2025-06
---

![img](/img/2025-06-index.png)

# 败犬のC++每月精选 2025-06

[[toc]]

本月的 C++ 话题速览！（2025-06）

## 1. 项目有个宏把所有成员函数定义成虚函数，方便 mock

很多项目都有。

具体的例子是：

```cpp
#ifndef NDEBUG
#define DEBUG_VIRTUAL virtual
#else
#define DEBUG_VIRTUAL
#endif

class A {
public:
    DEBUG_VIRTUAL void foo() {
        // 这是A的原本逻辑
    }
};

class MockA : public A {
public:
    DEBUG_VIRTUAL void foo() override {
        // 这是MockA的逻辑
    }
};

class B {
public:
    void target(A& a) {
        a.foo(); // 调用A的foo方法
        //... 其他逻辑
    }
};

void testB() {
    B b;
    MockA mockA;

    EXPECT_EQ(b.target(mockA), xxx);
}
```

## 2. 自己实现 `std::hash<std::pair<int, int>>` 的特化会有问题吗

只要不打开 std 就不是未定义行为。不过这个未定义行为用的人很多，所以其实不是很严重的问题。

打开 std 的写法：

```cpp
namespace std {  // 这行是未定义行为
template <>
struct hash<pair<int, int>> { ... };
}
```

不打开 std 的写法：

```cpp
template <>
struct std::hash<std::pair<int, int>> { ... };
```

但是，对 pair 这种标准库类型进行特化，实践上并不好，应该自己封装一个类型。

至于怎么实现 pair 的哈希算法，可以参考 boost::hash, boost::hash_combine。

## 3. tcp 校验和会不会因为 hash 碰撞导致误判，git commit 呢

会，但是概率很小。

tcp 校验和主要防止比特翻转，需要至少翻转 2 位（翻转的位置也有要求）才能误判，这导致概率很小。

git commit 的哈希用的是 SHA-1，位数足够多，生成 1e24 个 sha1 才有可能碰撞，git 仓库顶天有 1e10 个 object，所以很难碰撞。

git 为了分布式就必须用 hash，所以只能是尽量减小碰撞概率。

## 4. C++23 的效率与 C++20 相比，提升大不大

not even wrong，标准和效率几乎完全不相关。（高版本有些求值顺序定死了会影响效率，但是可以忽略）

真正影响效率的是编译器版本。

## 5. 是不是需要 io 的时候用异步才有效率提升

不一定。举个例子，一个计算密集型任务，一个访存密集型任务，前者算完一部分后者才能开始，这样也可以异步。（也可以是跨 NUMA 访存、异构访存等更耗时的操作，这样效果明显一点。IO 没有指明的话一般不包含访存）

## 6. std::replace 传元素引用的坑

```cpp
#include <iostream>
#include <algorithm>
#include <string>

int main() {
    std::string s = "a1b2a3";
    std::replace(s.begin(), s.end(), s[0], '9');
    std::cout << s << "\n";
}
```

可能的结果是 "91b2a3" (GCC 15.1 无编译参数)，只替换了 `s[0]`。因为 `std::replace` 的第三个参数是 `const T&`，这个值在函数里发生了改变。

正确方法：

```cpp
std::replace(s.begin(), s.end(), (char)s[0], '9');
// 或者
std::replace(s.begin(), s.end(), +s[0], '9');
// 或者
char target = s[0];
std::replace(s.begin(), s.end(), target, '9');
```

这个是真的坑，很多 algorithm 函数都传引用。cppref 的 Notes 也提到了这点。<https://en.cppreference.com/w/cpp/algorithm/replace.html>

> Because the algorithm takes old_value and new_value by reference, it can have unexpected behavior if either is a reference to an element of the range [first, last).

同款问题 <https://www.zhihu.com/question/630025869>。

## 7. `C x();` 是函数声明不是变量定义

```cpp
struct C {};

int main() {
    C x();  // 函数声明
}
```

大概每个新手都会踩一遍这个坑吧。

most vexing parse，即有歧义一律按函数声明处理。

<https://eel.is/c++draft/dcl.ambig.res>

## 8. C++26 的反射什么时候能用

据说 GCC 下个大版本可以用。

Clang 有设计缺陷，目前的架构不允许一边实例化模板一边进行常量求值，要重构 / 重写，工作量巨大。

MSVC 特性已经落后了。

## 9. 不用 delete 是好实践吗

没问题，new 得到的对象可以 `std::unique_ptr` 帮忙 delete。

用 `std::make_unique` 的话，new 也可以不用（除了 placement new）。

特殊情况，不想让 `std::make_unique` 给对象初始化（避免初始化开销），就要用 `std::make_unique_for_overwrite` (C++20) 。

## 10. 一些文章

C++ 中文周刊 2025-06-02 第185期 <https://zhuanlan.zhihu.com/p/1913050890824324660>

Track Errors First <https://www.bugsink.com/blog/track-errors-first/>

如果你是一个C++面试官，你会问哪些问题？ - 码小虎的回答 <https://www.zhihu.com/question/451327108/answer/1919026750731551704>（注：一般不会问，因为面试官首先得会）

C++ 中文周刊 2025-06-22 第186期 <https://zhuanlan.zhihu.com/p/1920296120623564306>（有详细的 c++26 的新进展）

Reflection for C++26!!! - YKIKO的文章 <https://zhuanlan.zhihu.com/p/1919923607997518115>

***

都看到这了，来关注一下败犬日报吧！

[主站](https://makeinu-daily.pages.dev/) | [知乎专栏](https://www.zhihu.com/column/c_1846629212653506560) | [微信公众号](https://makeinu-daily.pages.dev/img/wechat.png) | [RSS](https://makeinu-daily.pages.dev/feed.rss)
