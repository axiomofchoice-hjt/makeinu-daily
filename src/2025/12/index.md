---
date: 2026/01/01
title: 败犬のC++每月精选 2025-12
next: false
prev:
  link: /2025/11
  text: 败犬のC++每月精选 2025-11
---

![img](/img/2025-12-index.jpg)

# 败犬のC++每月精选 2025-12

[[toc]]

## 1. 为什么 STL 迭代器是左闭右开区间

答案是：[*Why numbering should start at zero*](https://www.cs.utexas.edu/~EWD/transcriptions/EWD08xx/EWD831.html) Edsger W. Dijkstra, 1982

有一个优点是拆分区间很自然，例如 `std::inplace_merge(BidirIt first, BidirIt middle, BidirIt last);`。

延伸阅读 [为什么 Lua 数组从 1 开始索引](https://stackoverflow.com/questions/2785704/why-do-lua-arraystables-start-at-1-instead-of-0)

## 2. 未定义和未指定有什么区别

未定义没有任何限制，编译器可以做任何事，包括买麦当劳双吉套餐，天降美少女。

未指定的结果都是预期的，只能在几个选项里选择。例如：

- 两个独立变量的地址比大小，结果只能是大于或小于。
- 函数参数的求值顺序。
- 多线程原子读写，读写顺序是未指定的。

对于未定义行为，绝大部分情况是尽可能避免。而对于未指定行为，需要保证所有未指定结果都能正确处理，不依赖未指定结果。

***

另外不要用“常识”判断未定义还是未指定。比如读取未初始化变量，这是未定义行为而非未指定。不过这行为在 C++26 变成了 erroneous behavior (EB)，鼓励编译器报错，如果没报错就还是未定义。

## 3. “防御性编程”鉴赏：shared_ptr 类型的成员变量，在成员函数里复制一份保证存活

```cpp
struct A {
    std::shared_ptr<B> obj_;

    void foo() {
        std::shared_ptr<B> obj = obj_;
        // 其他逻辑（没有析构、delete this 之类的操作）
    }
};
```

先说结论：完全没有必要。

几个 AI 一致认为有必要，说在多线程场景，this 会在别的线程析构，美名其曰“防御性编程”（被指出问题后，甚至反驳说群友没接触过工程）。

成员函数能保证 this 一直有效（除非主动析构或 delete this）。this 有效，它的成员变量自然一直有效。

如果真的有别的线程析构了 this，那这代码就是有 UB，是很危险的。这种“防御性编程”只会掩盖问题，而不是解决问题。

***

群友表示入职后最大的一个提升就是生产上永远不写“防御性代码”。要么有问题要么没问题，什么叫可能有问题。

如果防御性编程指断言、检查，那应该推荐（最多显得有点无聊）。而如果“防御性编程”指拿一个默认行为去掩盖问题，那就是掩耳盗铃。

“你先别管有没有问题，你就说代码能不能跑吧。”

## 4. 裸指针可以用 `optional<T&>` `span` `mdspan` 替代了

众所周知裸指针一开始的功能非常多，智能指针 (C++11) 出现后，裸指针就不再承担所有权功能。

借用功能一部分被引用代替，`optional<T&>` (C++26) 出现后又增加了可空、可重新绑定功能。不过和裸指针差别不大，不是明显的上位替代。

而表达数组的借用有 `span` (C++20) `mdspan` (C++23) 替代，功能上也会更完备。

## 5. 性能和指令数有关系吗

没有关系，就算是动态指令数也不行。

这是因为 cpu 执行是比较复杂的过程。访存指令遇到 cache miss 直接要等上百个周期，多发射流水线拉满的一个周期就能跑好几条。

所以评估性能离不开 benchmark 测时延。

## 6. 为什么不建议过早优化

老生常谈了，因为性能是破坏可读性的一大因素。

最理想的是程序员清楚自己的代码会有多少开销，避开性能上的坑，确保花精力的地方就是性能热点。但是这样的程序员太珍贵了。

其次就是优先保证可读性，分析热点时再优化。这也是日报一直说的可读性优先。

## 7. shallow const 问题（浅 const 问题）

<https://www.zhihu.com/question/839881639>

const 不会往下传递，比如 `int *const` 可以通过这个指针修改 int。

解决思路除了往期讲过的 `std::experimental::propagate_const`，更经典的做法是封装成类来控制，暴露两个成员函数，把 const 传递下去：

```cpp
class A {
   private:
    int* data;

   public:
    int* foo() { return data; }
    const int* foo() const { return data; }
};
```

其他语言也有类似现象，例如 javascript：

```js
const a = [1];
a[0] = 2;
```

例外是 safe rust 的借用检查阻止了这个行为。

## 8. 写 `int* p;` 还是 `int *p;`

喜欢哪个用哪个，用 `std::add_pointer_t<int> p;` 都没人拦着你（并非）。clang-format 提供了 PointerAlignment 支持三种风格（靠左 / 右 / 中间 `int * p;`）。

硬要推荐一个那就靠左 `int* p;`。

`int* p;` 可以把 `int*` 直接读成 int 指针，更符合直觉。

`int *p;` 是因为 C 设计的时候，让定义和使用的写法一致。`int *p;` 就是当你用 `*p` 就能得到一个 int，`int (*p)[10]` 就是当你用 `(*p)[i]` 就能得到一个 int。

对于 `int* p, q;` 的问题，建议一个语句只定义一个变量。

## 9. “可执行”的 C++ 源文件

```cpp
//usr/bin/true ; TMP_OUT=$(mktemp) ; /usr/bin/env c++ "$0" -o "${TMP_OUT}" ; exec -a "$0" "${TMP_OUT}" "$0" ; rm "${TMP_OUT}" ; exit
#include <iostream>

int main(int argc, char** argv) {
    std::cout << argc << std::endl;
    for (int i = 0; i < argc; i++) {
        std::cout << argv[i] << std::endl;
    }
    return 0;
}
```

用 shell 执行就会编译运行代码，用了一些操作让 `argv[0]` 正确传递。

## 10. 推荐阅读

有史以来最烂的编程语言 [youtube 原视频](https://www.youtube.com/watch?v=7fGB-hjc2Gc)，[b 站转载](https://b23.tv/tePLN99)，[翻译后的文字版](https://zhuanlan.zhihu.com/p/1976881130755072953)，其实有很多不专业的地方，建议结合大佬的吐槽来看 <https://www.zhihu.com/question/1977143614883776265/answer/1977614740130907300>

真正意义上的理解 C++ 模板 <https://zhuanlan.zhihu.com/p/655902377>

jetbrains 关于 C++ 的年度总结 <https://lp.jetbrains.com/the-state-of-cpp-2025/>

Performance Hints - Jeff Dean <https://abseil.io/fast/hints.html>

Cpp错误处理杂谈 <https://zhuanlan.zhihu.com/p/643809540>
