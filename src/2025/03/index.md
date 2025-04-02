---
date: 2025-04-01
title: 败犬のC++每月精选 2025-03
prev:
    text: 败犬のC++每月精选 2025-02
    link: /2025/02
next: false
---

# {{ $frontmatter.title }}

[[toc]]

## 1. C++ 跳出双重循环或跳出 if 的方法

没有很好的做法。

最合理的做法可能是 lambda 包一层，用 return 跳出。

用 goto 容易违反项目规范。

> You suddenly visualize that I am looking over your shoulders and say to yourself: "Dijkstra would not have liked this"

另外，break label 的提案是有的 <https://open-std.org/JTC1/SC22/WG21/docs/papers/2025/p3568r0.html>。

## 2. 异常会导致二进制膨胀

写了异常会多一堆二进制代码来处理异常，一些项目禁止 RTTI 和异常都是这个理由。

例如 LLVM <https://llvm.org/docs/CodingStandards.html#do-not-use-rtti-or-exceptions>：

> Do not use RTTI or Exceptions
>
> In an effort to reduce code and executable size, LLVM does not use exceptions or RTTI (runtime type information, for example, dynamic_cast<>).
>
> That said, LLVM does make extensive use of a hand-rolled form of RTTI that use templates like isa<>, cast<>, and dyn_cast<>. This form of RTTI is opt-in and can be added to any class.

当然允许异常的项目同样也有很多，异常更简单省事。

不用异常可以用 `std::expected` 或类似的设计替代。

***

一个 cppcon 讲了如果返回错误码的代码过多，关闭 rtti 使用异常替换同样的逻辑可以做到更小的二进制体积。<https://www.bilibili.com/video/BV14YyfYhE3C> 第一集

## 3. 静态链接符号未找到，但目标文件有这个符号

是链接顺序的问题。在[往期](/2024/11/25)提到这个现象：

> 主程序没引用静态库里面的符号，可能导致静态库整个被丢弃，里面的全局变量初始化的副作用也会没

可以用 `--whole-archive` 来临时规避，但是会导致二进制膨胀问题。

最佳实践是 `--start-group` `--end-group`。

<https://stackoverflow.com/questions/52435705/whats-difference-between-start-group-and-whole-archive-in-ld>

## 4. C 的资源释放问题

函数退出前要把之前的 malloc 全都 free 了，如果函数复杂就会有大量重复 free。

一般要用 goto 来解决，例如：

```cpp
void func() {
    int *a, *b, *c;
    a = (int *)malloc(sizeof(int));
    if (a == NULL) {
        goto a_fail;
    }
    b = (int *)malloc(sizeof(int));
    if (b == NULL) {
        goto b_fail;
    }
    c = (int *)malloc(sizeof(int));
    if (c == NULL) {
        goto c_fail;
    }
    free(c);
c_fail:
    free(b);
b_fail:
    free(a);
a_fail:
}
```

如果项目禁止了 goto，可以用 attribute cleanup，类似 C++ 的 RAII。

## 5. `unordered_map<string, int>` 不能查找 string_view

下面的代码会报错 `error: no matching function for call to 'xxx::find(std::string_view)'`。

```cpp
#include <iostream>
#include <string>
#include <unordered_map>

int main() {
    std::unordered_map<std::string, int> a;
    a.find(std::string_view());
}
```

虽然 <https://zh.cppreference.com/w/cpp/container/unordered_map/find> 在 C++20 之后支持了模板接口 `template< class K > const_iterator find( const K& x ) const;`，但是 Hash 和 KeyEqual 必须是透明的，所以需要自定义 Hash：

```cpp
#include <iostream>
#include <string>
#include <unordered_map>

struct my_hash : std::hash<std::string>, std::hash<std::string_view> {
    using std::hash<std::string>::operator();
    using std::hash<std::string_view>::operator();
    using is_transparent = void;
};

int main() {
    std::unordered_map<std::string, int, my_hash, std::equal_to<>> a;
    a.find(std::string_view());
}
```

## 6. 如何用可变参数给数组赋值

构造函数比较简单。赋值麻烦一点，要用 integer_sequence。

```cpp
#include <cstdlib>
#include <utility>

template <size_t N>
struct Array {
    int array[N];

    template <typename... Ts>
    Array(Ts... args) : array{std::move(args)...} {}

    template <typename... Ts>
    void assign(Ts... args) {
        [&]<size_t... Is>(std::index_sequence<Is...>) {
            (..., (array[Is] = std::move(args)));
        }(std::index_sequence_for<Ts...>{});
    }
};
```

## 7. 引用的非空 hint

引用不能为空，编译器会根据这点对代码进行优化。

<https://zhuanlan.zhihu.com/p/665536071> 这个就讲了成员函数的 this 如果是 nullptr 会出问题的例子（即使成员函数没有使用 this）。

类似的还有 memcpy 也会有非空的假设 <https://zhuanlan.zhihu.com/p/699259091>。

## 8. 三路运算符 `<=>` 和强序弱序偏序

这些概念把比较运算给规范化了，区分了三种类型：

1. `std::strong_ordering` “严格”地比较大小。
2. `std::weak_ordering` 不“严格”地比较大小，比如按字典序比，但是忽略大小写；或者只看一部分属性，忽略另一部分属性。
3. `std::partial_ordering` 可能有些东西没法比大小，比如 nan。

***

三路运算符解决了什么问题？

定义了 `<=>` 后 `< <= > >=` 这 4 个运算符就能用了，写起来简单。

***

为什么定义了 `<=>` 还要定义 `==`？

性能考虑。例如字符串比较，`==` 只要长度不同就可以直接返回 false，而 `<=>` 还要区分大于小于。

***

如果 `<=>` 和 `==` 冲突了会怎么办？

不影响，因为 `< <= > >=` 由 `<=>` 引出，`!=` 由 `==` 引出，两者没有交集，只是行为会很奇怪。

但是使用了 `std::sort` 之类的标准库函数是未定义行为。

***

推荐阅读

1. <https://hackingcpp.com/cpp/lang/comparisons.html>
2. <https://zhuanlan.zhihu.com/p/350867708>
3. <https://github.com/xiaoweiChen/CXX20-The-Complete-Guide> 第一章

## 9. 重载决议的一个例子

```cpp
#include <cstdio>

template <typename T>
void f(T &&x) {
    printf("1\n");
}

void f(const int &x) { printf("2\n"); }

int main() {
    int x = 1;
    f(x);
}
```

答案是 1，`const int &x` 不是完美匹配（多了个 const）。

那么，在实践上如果有多个行为不一致的函数，怎么匹配想要的函数？

可以加 requires（但不一定是好的实践）。标准库的做法是换函数名，无法换函数名（比如构造函数），在函数形参开头加一个不同的占位参数（比如 `std::optional` 构造函数的 `std::in_place_t`，`std::set` 构造函数的 `std::from_range_t`）。

## 10. deducing this + CRTP 的隐藏坑

给某个类注入一个函数，然后这个类被别人继承，再通过派生类调用注入的函数，这时 self 是别人派生的那个类。

```cpp
#include <iostream>

template <typename Derived>
struct Base {
    void foo(this auto&& self) {
        std::cout << "self is " << typeid(decltype(self)).name() << "\n";
    }
};

struct Derived : Base<Derived> {};

struct FurtherDerived : Derived {};

int main() {
    FurtherDerived fd;
    fd.foo();
}
```

输出是 `self is 14FurtherDerived`，self 推导成了 FurtherDerived 而不是期望的模板参数 Derived。

解决方法是直接不用 deducing this。（也可以给被注入的类加 final，但是不合理，因为增加了约定）

## 11. `vector::push_back` 如果有扩容，为什么先构造传入的元素而非原有元素

```cpp
#include <iostream>
#include <vector>

struct A {
    int x;
    A(int x) : x(x) {}
    A(A&& other) noexcept {
        x = other.x;
        std::cout << "move " << x << "\n";
    }
};

int main() {
    std::vector<A> vec1;
    vec1.push_back(A(1));
    std::cout << "***\n";
    vec1.push_back(A(2));
    return 0;
}
```

输出：

```text
move 1
***
move 2
move 1
```

标准没有规定顺序，实现上的顺序是为了满足“有无扩容表现一致”的要求。

例如 `vec.push_back(vec.front())`，如果先移动原有元素，`vec.front()` 就悬垂引用了。

再例如 `vec.push_back(std::move(vec.front()))`，想想怎么实现 `push_back` 让有扩容和无扩容的表现一致？
