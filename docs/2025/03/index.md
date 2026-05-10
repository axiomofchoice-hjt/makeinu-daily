---
date: 2025-04-01
next:
  link: /2025/04
  text: 败犬のC++每月精选 2025-04
prev:
  link: /2025/02
  text: 败犬のC++每月精选 2025-02
title: 败犬のC++每月精选 2025-03
description: 本期日报包含 C++ 话题，涵盖语言特性、标准库、性能优化、内存管理、编译构建等多个方面
__tags__:
- title: '## 1. C++ 跳出双重循环或跳出 if 的方法'
  score: 7/10
  tags:
  - C++
  - 工程实践
  - 基础知识
  - 需改进
  explanation: 讨论 C++ 中跳出多重循环的方法，提到 lambda 和 goto 的优缺点，但内容不够全面，缺少实际代码示例和性能对比，需要改进。
- title: '## 2. 异常会导致二进制膨胀'
  score: 8/10
  tags:
  - C++
  - 性能优化
  - 错误处理
  - 工程实践
  - 进阶知识
  explanation: 分析异常机制对二进制体积的影响，对比 LLVM 禁用异常的做法和替代方案，属于性能优化和工程实践的进阶知识。
- title: '## 3. 静态链接符号未找到，但目标文件有这个符号'
  score: 8/10
  tags:
  - C++
  - 编译构建和调试
  - 工程实践
  - 进阶知识
  explanation: 解释静态链接时符号查找问题，分析链接顺序的影响，提供 --whole-archive 和 --start-group 的解决方案，属于编译构建的进阶知识。
- title: '## 4. C 的资源释放问题'
  score: 7/10
  tags:
  - C++
  - 内存管理
  - 工程实践
  - 基础知识
  explanation: 讨论 C 语言中资源释放的复杂性，对比 goto 和 attribute cleanup 的解决方案，涉及内存管理和工程实践的基础知识。
- title: '## 5. `unordered_map<string, int>` 不能查找 string_view'
  score: 9/10
  tags:
  - C++
  - 标准库特性
  - STL
  - 语法特性
  - 进阶知识
  explanation: 分析 unordered_map 查找 string_view 的问题，解释透明 Hash 和 KeyEqual 的要求，提供自定义
    Hash 的解决方案，属于标准库特性的进阶知识。
- title: '## 6. 如何用可变参数给数组赋值'
  score: 8/10
  tags:
  - C++
  - 语法特性
  - 编译期
  - 泛型编程
  - 进阶知识
  explanation: 展示使用可变参数模板和 integer_sequence 实现数组赋值的方法，涉及编译期编程和泛型编程的进阶知识。
- title: '## 7. 引用的非空 hint'
  score: 8/10
  tags:
  - C++
  - 性能优化
  - 语法特性
  - 进阶知识
  explanation: 分析引用非空假设对编译器优化的影响，举例说明成员函数 this 指针和 memcpy 的非空假设，属于性能优化的进阶知识。
- title: '## 8. 三路运算符 `<=>` 和强序弱序偏序'
  score: 9/10
  tags:
  - C++
  - 语法特性
  - 标准库特性
  - 基础知识
  explanation: 详细解释三路运算符和比较类别（强序、弱序、偏序），分析其解决的问题和性能考虑，属于语法特性的基础知识。
- title: '## 9. 重载决议的一个例子'
  score: 8/10
  tags:
  - C++
  - 语法特性
  - 函数
  - 泛型编程
  - 进阶知识
  explanation: 通过具体示例分析重载决议规则，讨论完美匹配和 const 限定符的影响，提供实践中的解决方案，属于函数重载的进阶知识。
- title: '## 10. deducing this + CRTP 的隐藏坑'
  score: 8/10
  tags:
  - C++
  - 语法特性
  - 面向对象编程
  - 泛型编程
  - 专家知识
  explanation: 揭示 deducing this 与 CRTP 结合时的类型推导问题，分析继承链中的 self 类型推导，属于面向对象编程的专家知识。
- title: '## 11. `vector::push_back` 如果有扩容，为什么先构造传入的元素而非原有元素'
  score: 9/10
  tags:
  - C++
  - STL
  - 标准库特性
  - 内存管理
  - 进阶知识
  explanation: 分析 vector push_back 扩容时的元素构造顺序，解释标准未规定但实现一致性的要求，涉及自引用场景的安全性考虑，属于 STL
    的进阶知识。
---

![img](/img/2025-03-index.webp)

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
