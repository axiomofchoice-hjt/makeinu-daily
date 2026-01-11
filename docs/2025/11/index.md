---
date: 2025/12/01
title: 败犬のC++每月精选 2025-11
next:
  link: /2025/12
  text: 败犬のC++每月精选 2025-12
prev:
  link: /2025/10
  text: 败犬のC++每月精选 2025-10
description: 本期日报包含 C++ 语言特性、标准库、ABI、性能优化、内存管理、编译构建、工程实践等多个话题，以及一些外部技术文章链接。
__tags__:
- title: '## 1. O(N) 原地合并两个有序数组'
  score: 7/10
  tags:
  - C++
  - 算法
  - 性能优化
  - 进阶知识
  explanation: 讨论 O(N) 原地合并有序数组的算法理论，提及稳定性和论文实现，属于算法和性能优化的进阶知识。
- title: '## 2. 标准库的 map 有没有非红黑树的实现'
  score: 8/10
  tags:
  - C++
  - STL
  - 基础知识
  explanation: 分析 std::map 的接口设计为何与红黑树绑定，并讨论其他数据结构（如 B 树、AVL 树）为何不适用，属于 STL 的基础知识。
- title: '## 3. double 有多少位十进制有效数字'
  score: 9/10
  tags:
  - C++
  - 基础知识
  - 硬件相关
  explanation: 解释 double 的 IEEE 754 格式，通过尾数位数估算有效数字为 15，涉及硬件表示的基础知识。
- title: '## 4. 右值引用传参时发生了什么'
  score: 8/10
  tags:
  - C++
  - 语法特性
  - 基础知识
  explanation: 通过代码示例说明 prvalue、xvalue 和 lvalue 在右值引用传参时的转换过程，属于 C++ 值类别的基础知识。
- title: '## 5. `std::vector<std::atomic<T>>` 会发生什么'
  score: 8/10
  tags:
  - C++
  - STL
  - 内存管理
  - 并发编程
  - 基础知识
  explanation: 解释由于 std::atomic 不可复制/移动，导致 std::vector 的某些操作（如 push_back、resize）编译失败，涉及
    STL、内存管理和并发编程的基础知识。
- title: '## 6. bool 值表示'
  score: 9/10
  tags:
  - C++
  - ABI
  - 硬件相关
  - 基础知识
  - 需改进
  explanation: 讨论 bool 在内存和寄存器中的值表示，引用 System V ABI 说明 false 为 0、true 为 1，但指出标准未强制规定，属于
    ABI 和硬件相关的基础知识。需改进：部分表述（如“函数内部寄存器用非 0 表示 true”）可能引起混淆，建议更清晰地区分 ABI 规定与编译器实现。
- title: '## 7. `/usr` 是否曾经是 user 的简写'
  score: 6/10
  tags:
  - 其他
  - 内容较主观
  explanation: 探讨 Unix 文件系统中 /usr 目录名称的由来，引用维基百科和 System V 手册，但结论缺乏权威证实，内容较主观。
- title: '## 8. 为什么 `int a[10]; int* p = a + 11;` 是未定义行为，`int* p = reinterpret_cast<int*>(114514);`
    不是未定义行为'
  score: 8/10
  tags:
  - C++
  - 语法特性
  - 内存管理
  - 基础知识
  explanation: 对比指针算术（数组越界）与整数到指针的 reinterpret_cast 在未定义行为上的差异，引用 cppref 说明规则，属于语法特性和内存管理的基础知识。
- title: '## 9. fstream 打开文件，路径不能是 string_view'
  score: 7/10
  tags:
  - C++
  - 标准库特性
  - 工程实践
  - 基础知识
  explanation: 解释 std::string_view 因缺乏空终止符而不能直接用于 fstream 打开文件，涉及标准库特性和工程实践的基础知识。
- title: '## 10. 关于怎么 using 导入库的内容'
  score: 6/10
  tags:
  - C++
  - 工程实践
  - 内容较主观
  explanation: 提出使用命名空间别名（如 namespace fs = std::filesystem）而非 using 声明来导入库内容，属于工程实践建议，内容较主观。
- title: '## 11. 一些文章'
  score: 7/10
  tags:
  - 其他
  explanation: 列举多个外部技术文章链接，涵盖 Linux 系统调用、Shader 编程、C++ 周刊、epoll/IOCP 比较、TensorCore
    论文等，主题分散，标签为其他。
---

![img](/img/2025-11-index.png)

# 败犬のC++每月精选 2025-11

[[toc]]

## 1. O(N) 原地合并两个有序数组

如果是 $O(N\log N)$ 原地合并，只要堆排序就行了。如果还想要稳定（保持原有的顺序），[cppref](https://zh.cppreference.com/w/cpp/algorithm/ranges/inplace_merge.html) 就有记载方法。

O(N) 可以吗？还真可以（但是会失去稳定性），*Practical In-Place Merging* 这篇论文，以及这个[源码](https://keithschwarz.com/interesting/code/?dir=inplace-merge)。比较复杂，知道理论存在就好了。

## 2. 标准库的 map 有没有非红黑树的实现

之前日报说过，`std::map` 接口都是直接对照红黑树量身定制的。

比如 B / B+ 树插入删除会导致迭代器失效，就做不到。

splay, treap 复杂度不对。（当然 splay 也不满足读操作线程安全）

AVL 树应该满足要求，但考虑到性能和内存占用应该不会有人用。

## 3. double 有多少位十进制有效数字

15。

众所周知 double 有 1 bit 符号位，11 bit 指数位，52 bit 尾数位，决定有效数字的是尾数。

一个估算思路是求 double 能精确表示的整数范围。由于 IEEE 754 规定尾数之前还有一个隐含的“1”，所以答案是 $(111...1)_2$（一共 53 个 1）即 $2^{53} - 1\approx 9×10^{15}$。这样就大致得到 15 个有效数字了。

（注意这只是一个估算，严谨证明留作课后习题）

## 4. 右值引用传参时发生了什么

```cpp
#include <utility>

void foo(int&&) {}

int bar() { return 0; }

int main() {
    foo(114);
    foo(bar());
    int x = 514;
    foo(std::move(x));
}
```

`foo(114)` 中的 114 是一个 prvalue（纯右值），先发生了临时量实质化，实质化是指 prvalue 转换为了 xvalue（将亡值）。然后传给 foo。

`foo(bar())` 的 `bar()` 也是 prvalue，发生的事情同上。

`foo(std::move(x))` 里的 std::move 将 lvalue（左值）转换为 xvalue，然后传给 foo。

## 5. `std::vector<std::atomic<T>>` 会发生什么

```cpp
#include <atomic>
#include <vector>

int main() {
    std::vector<std::atomic<int>> a(10);
    a[0] = 1;
    a.pop_back();
    a.clear();
    // a.push_back(2);  // 编译报错
    // a.resize(2);     // 编译报错
}
```

可以用但有限制。

我们知道 std::atomic 不可复制不可移动。由于 push_back 和 resize 之类的操作会导致 vector 扩容，就需要复制或移动元素，所以这些操作都会编译失败。

## 6. bool 值表示

bool 的值表示，就是存储的值是 0 1 还是其他，这是 ABI 定义的。例如 system v abi 规定了 false 用 0 表示，true 用 1 表示（后面有参考和解释）。

c++ 标准定义了 bool 只可能包含两个值 false true，以及 false true 转换为整数会变成 0 1。但是 false true 的表示没有规定，它们是 100 和 200 也符合标准。

因此这个说法是错误的：“bool 值表示是 0 和非 0，可以为 0..255 中间的任意值”。

***

再举个编译器优化的例子：

```cpp
#include <bit>

bool foo(bool a)
{
    auto x = std::bit_cast<char>(a);
    return x == 0 || x == 1;
}

// foo(bool):
//         mov     al, 1
//         ret
```

上面例子用 clang 21.1.0 `-std=c++20 -O3` 编译，bar 直接返回了 1，可见在这个 ABI 限制下 bool 不可能是非 01 值。

***

同时，严格来说标准是不保证 bool memset 为 0 的效果的，不过恰好所有实现都把全零当成 false，所以 memset 0 总是能用的。

***

关于 abi 的解释，[system v abi (x86-64)](https://gitlab.com/x86-psABIs/x86-64-ABI) 有记载：

> Booleans, when stored in a memory object, are stored as single byte objects the value
of which is always 0 (false) or 1 (true). When stored in integer registers (except for
passing as arguments), all 8 bytes of the register are significant; any nonzero value is
considered true.
>
> 翻译：布尔值存储在内存对象中时，以单字节对象的形式存储，其值始终为 0（假）或 1（真）。而存储在整数寄存器中时（作为参数传递的情况除外），寄存器的全部 8 个字节都有效；任何非零值都被视为真。

这部分有点奇怪。system v abi 突然规定函数内部寄存器用非 0 表示 true，可是 abi 是接口，不应该规定函数内部怎么实现。除此之外都有，false 用 0 表示，true 用 1 表示。

itanium c++ abi 没找到相关规定，应该是因为不需要重复定义了。

## 7. `/usr` 是否曾经是 user 的简写

网上很多人说 `/usr` 一开始表示 user，后来 `/usr` 内容转移到 `/home`，于是给 usr 一个 Unix System Resources 的解释。

但是没有权威资料证明 usr 是 user，只能说大概率是这样。

维基有 `/usr` 的由来，但没说全称是什么 <https://en.wikipedia.org/wiki/Unix_filesystem#Principles>：

> In the original Bell Labs Unix, a two-disk setup was customary, where the first disk contained startup programs, while the second contained users' files and programs. This second disk was mounted at the empty directory named usr on the first disk, causing the two disks to appear as one filesystem, with the second disk’s contents viewable at /usr.
>
> 在最初的贝尔实验室 Unix 系统中，通常采用双磁盘配置，第一块磁盘存放启动程序，第二块磁盘存放用户文件和程序。第二块磁盘挂载在第一块磁盘上名为 /usr 的空目录下，使得两块磁盘看起来像是一个文件系统，用户可以通过 /usr 访问第二块磁盘的内容。

（就算 `/usr` 存放 user 文件，也不能证实 `/usr` 是 user）

而群友又翻了 System V 的手册，有的东西确实会把 user 缩写成 usr，比如 SIGUSR1。

## 8. 为什么 `int a[10]; int* p = a + 11;` 是未定义行为，`int* p = reinterpret_cast<int*>(114514);` 不是未定义行为

偷点周刊群话题。

这是加法 UB 了。指针算术是有要求的，大致意思是数组里指针的加减不能移出数组范围 `[begin, end]`（包括末尾元素的后一个）。（[cppref](https://en.cppreference.com/w/cpp/language/operator_arithmetic.html) 里的 Pointer arithmetic 章节）

而整数转换到指针是任何条件都不 UB 的。（[cppref](https://en.cppreference.com/w/cpp/language/reinterpret_cast.html) 里的 A value of any integral or enumeration type can be converted to a pointer type）

***

还有个令人费解的操作，就是 `int* p = a + 11;` 改成 `int* p = reinterpret_cast<int*>(reinterpret_cast<size_t>(a) + 11 * sizeof(int));` 就不是未定义行为了，看似一样的行为实则不然。

（c++ 为什么这么设计，群友没说）

## 9. fstream 打开文件，路径不能是 string_view

众所周知 string_view 末尾不保证有 `\0`。系统调用 open 需要 `\0` 结尾，所以 string_view 必须拷贝并末尾添加 `\0` 才能使用，这个过程是有开销的。而体现开销最好的方式就是让用户手动转换成 `std::string` 或 `fs::path`，这就是“显式优于隐式”的哲学。<https://cplusplus.github.io/LWG/issue3430>

## 10. 关于怎么 using 导入库的内容

个人更倾向于展开最后一层命名空间。例如：

```cpp
namespace A::B::C {
    void f();
}

namespace C {
    using namespace A::B::C;
}
// 或者
namespace C = A::B::C;
```

`namespace fs = std::filesystem;` 这样的经典写法就是这个方式。

我认为 `using std::string;` 的写法即使在源文件里也应该避免。如果头文件 struct 里 `std::string`，源文件又是 string，不能确定是不是同一个东西，会增加心智负担。

## 11. 一些文章

[Linux系统调用Hook：从内核机制到实际落地](https://mp.weixin.qq.com/s/xFjQvBDEuTGkzAw49PCWAQ)

[【译】Shader艺术编码入门介绍(An introduction to Shader Art Coding)](https://www.bilibili.com/video/BV1DM4y1n7eB/)

[直达链接的油猴脚本](https://greasyfork.org/en/scripts/412612-open-the-f-king-url-right-now)

[C++ 中文周刊 2025-11-15 第189期](https://zhuanlan.zhihu.com/p/1973122845740660645)

[cppstat](https://cppstat.dev/) 可以看 C++ 标准的编译器支持情况。cppref 还在维护，更新没那么及时。

[技术派-epoll和IOCP之比较](https://zhuanlan.zhihu.com/p/106957967)

[MMA-Sim: Bit-Accurate Reference Model of Tensor Cores and Matrix Cores](https://arxiv.org/html/2511.10909v1) 讲 TensorCore 的 MMA 是怎么算的论文。
