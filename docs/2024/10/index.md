---
date: 2024-11-01
title: 败犬のC++每月精选 2024-10
prev: false
next:
  text: 败犬のC++每月精选 2024-11
  link: /2024/11
description: 本期日报包含多个 C++ 相关话题，涵盖性能优化、内存管理、类型转换、跨语言接口、缓存优化、动态库问题和工程实践等
__tags__:
- title: '## 1. 线程安全哈希表 benchmark'
  score: 8/10
  tags:
  - C++
  - 性能优化
  - STL
  - 进阶知识
  explanation: 介绍 boost 的线程安全哈希表 benchmark 结果，涉及性能优化和 STL 容器，属于进阶知识。
- title: '## 2. std::vector 扩容系数 1.5 为什么比 2 好'
  score: 9/10
  tags:
  - C++
  - 内存管理
  - 性能优化
  - STL
  - 进阶知识
  explanation: 分析 std::vector 扩容系数选择 1.5 而非 2 的原因，涉及内存管理和性能优化，属于进阶知识。
- title: '## 3. 两个在不同命名空间，但是字段完全一样的结构体，可以直接强制类型转换吗'
  score: 7/10
  tags:
  - C++
  - 类型
  - 内存管理
  - 基础知识
  - 需改进
  explanation: 讨论不同命名空间相同结构体的类型转换问题，涉及严格别名和未定义行为，建议使用 bitcast/memcpy，属于基础知识。需改进：解释不够全面，缺少具体实现示例。
- title: '## 4. c 如何提供接口让 cpp 传 lambda 进去'
  score: 8/10
  tags:
  - C++
  - 函数
  - 内存管理
  - 工程实践
  - 进阶知识
  explanation: 展示 C 接口如何接收 C++ lambda 的两种实现方式，涉及函数对象和内存管理，属于进阶知识。
- title: '## 5. 为什么以前的人不注重缓存'
  score: 6/10
  tags:
  - 硬件相关
  - 性能优化
  - 基础知识
  - 内容较主观
  explanation: 讨论历史缓存优化意识，涉及硬件发展和 cache oblivious 算法，属于基础知识。内容较主观：基于历史推测，缺乏具体数据支撑。
- title: '## 6. 一个库申请的内存到另一个库释放，发生了崩溃'
  score: 9/10
  tags:
  - C++
  - 内存管理
  - 编译构建和调试
  - 进阶知识
  explanation: 分析跨动态库内存释放崩溃的原因，涉及 ODR 违背和符号可见性，属于进阶知识。
- title: '## 7. Java 能不能鸭子类型'
  score: 6/10
  tags:
  - 其他
  - 基础知识
  - 需改进
  explanation: 讨论 Java 实现鸭子类型的可能性，通过反射实现。属于基础知识。需改进：与 C++ 关联性较弱，解释不够深入。
- title: '## 8. 头文件用了 libcurl 头文件，需要 pimpl 隐藏 libcurl 吗'
  score: 8/10
  tags:
  - C++
  - 工程实践
  - 编译构建和调试
  - 进阶知识
  explanation: 讨论头文件依赖管理，建议使用前置声明和 unique_ptr 避免暴露第三方库细节，属于进阶知识。
- title: '## 9. C++ 升个版本有那么难吗'
  score: 7/10
  tags:
  - C++
  - 工程实践
  - 基础知识
  - 内容较主观
  explanation: 讨论 C++ 版本升级的技术债务问题，强调定期升级的重要性，属于基础知识。内容较主观：基于个人经验的观点表达。
---

![img](/favicon.jpg)

# {{ $frontmatter.title }}

[[toc]]

## 1. 线程安全哈希表 benchmark

![img](/img/2024-10-16-0.webp)

完整 benchmark 见 <https://www.boost.org/doc/libs/develop/libs/unordered/doc/html/unordered.html#benchmarks_boostconcurrent_flat_map>

boost 的项目足够新，后发优势，可以抄其他项目的优秀设计，flat_hashmap 性能可能是知名实现里最好的。

## 2. std::vector 扩容系数 1.5 为什么比 2 好

我们知道，std::vector 在容量不够时会申请新的一块空间，这个空间大小 = 原来的大小乘以扩容系数。MSVC 是 1.5，GCC / Clang 是 2。

唯一正解：实测 1.5 比 2 性能好！

***

folly 文档是这么写的：1.5 不一定能实现内存复用，但存在复用的概率；而 2 不存在理论复用的可能。这里的内存复用是怎么一回事呢？

我们考虑一个简单的场景：不断给一个 vector push_back 操作。

假设一开始 vector 容量是 V，扩容系数 p，那么接下来的 n 次扩容容量分别是：$V,Vp,Vp^2,...,Vp^n$。

接下来一次扩容，会申请 $Vp^{n+1}$ 的容量（并且这次申请我们打算复用之前用过的内存）。此时之前已经释放了 $V,Vp,Vp^2,...,Vp^{n-1}$ 的内存（注意 $Vp^n$ 还没释放），这些内存加起来大于等于即 $Vp^{n+1}$ 就可以内存复用。

$$V+Vp+Vp^2+...+Vp^{n-1}=\dfrac{V(p^n-1)}{p-1}\ge Vp^{n+1}$$

考虑 n 趋向于无穷大：

$$\dfrac{Vp^n}{p-1}\ge Vp^{n+1}$$

$$\dfrac{1}{p-1}\ge p$$

$$p(p-1)\le 1$$

$$\dfrac{-\sqrt{5}+1}{2}\le p \le \dfrac{\sqrt{5}+1}{2}$$

$p \le 1.618$ 就是这么来的。

***

但是实际上内存分配器行为并不是那样的，内存复用在大多数情况都没有说服力（内存分配器一般会把大小近似的内存块放一起，导致复用的内存几乎不可能是同一个 vector 扩容留下的）。

我们知道，扩容系数越小内存占用期望降低，内存利用率越高；扩容系数越大扩容次数变少，扩容开销降低。之所以后来的很多设计采用了 1.5 而不是 2，因为 1.5 是两种因素的平衡点，是从大量实践中找到的。<https://groups.google.com/g/comp.lang.c++.moderated/c/asH_VojWKJw?pli=1>

## 3. 两个在不同命名空间，但是字段完全一样的结构体，可以直接强制类型转换吗

<https://zh.cppreference.com/w/cpp/language/reinterpret_cast>：“在实际上不代表适当类型的对象的泛左值（例如通过 reinterpret_cast 所获得）上进行代表非静态数据成员或非静态成员函数的成员访问将导致未定义行为。”

虽然是未定义行为但也不会出什么问题。最好可以 bitcast / memcpy，这是标准行为。

严格别名的 reinterpret_cast 都是 ub。

## 4. c 如何提供接口让 cpp 传 lambda 进去

提供 `void* context, void(*func)(void*)` 接口，类似 FunctionRef，有一些 C 库就是这样干的。

示例：

```cpp
#include <functional>
#include <iostream>

void registerCallback(void* context, void (*func)(void*)) { func(context); }

struct Content {
    std::function<void()> bind;
    static void call(void* self) { static_cast<Content*>(self)->bind(); }
};

int main() {
    int x = 233;
    auto lambda = [x]() { std::cout << x << std::endl; };
    Content content{lambda};

    registerCallback(&content, Content::call);
    return 0;
}
```

更进一步，想要消除 function 分配堆内存开销，以及 C 函数内也需要上下文，示例如下：

```cpp
#include <iostream>

// C 接口，参数为回调函数和上下文
extern "C" void c_world(void (*func)(void*, void*), void* context) {
    const char* msg = "world";
    func(&msg, context);
}

// 适配 C 接口，允许传入 C++ 仿函数
template <typename Func>
void invoke_c_style(void (*c_func)(void (*)(void*, void*), void*), Func f) {
    auto callback = [](void* data, void* context) {
        auto& func = *static_cast<Func*>(context);
        func(data);
    };
    c_func(callback, &f);
}

int main() {
    std::string message = "Hello, ";
    invoke_c_style(c_world, [&](void* c_msg) {
        std::cout << message << *static_cast<const char**>(c_msg) << "!\n";
    });
}
```

## 5. 为什么以前的人不注重缓存

因为那会确实差距不算大吧，而且还有各种 cache line 不一样所以考虑 cache oblivious 的情况。

<https://colin-scott.github.io/personal_website/research/interactive_latency.html>

一个底层的东西一般得好几年才会被上面的感觉到。

关于 cache oblivious，大多数 CPU 都是 64 字节 cache line，可能远古时期有小于 64 的；IBM 可能有 128 的机器。

## 6. 一个库申请的内存到另一个库释放，发生了崩溃

谁申请谁释放，这个原则可以规避这类问题。

***

我们来分析一下为什么崩溃：

内存申请释放一般走 glibc / musl 之类的库。

glibc 这样的库，它的 malloc 依赖它里面定义的全局变量状态；这样的全局变量出现多份就会出现上述问题。

不光是 malloc，别的函数比如 fopen 这种分配句柄的，都得一个全局的变量（状态）来记录已经分配的内存 / 句柄。把 A 变量分配的 handle 交给 B 变量释放，就会 crash。

根本原因是 ODR 违背导致的，跨动态库使用变量导致 crash。

所以问题就变成，静态链接 / 动态链接的符号可见性以及符号合并的情况了。要想知道啥时候链接器不合并，就去查动态库符号可见性；静态链接符号合并规则和动态链接符号合并规则不同。

***

模板隐式实例化也会有类似问题。动态库和主程序各一份实例化（实例化的时候只能看见自己的 malloc free 啥的），而且未合并。

值得注意的是，隐式实例化在静态链接的时候一定是会合并的，但是动态链接的时候则情况非常复杂了。

***

扩展阅读：<https://zhuanlan.zhihu.com/p/692886292>

## 7. Java 能不能鸭子类型

普通的继承：声明的时候得写明它继承了 Duck 类。

鸭子类型：只要这个类实现了 fly()，它就是鸭子。

Go 和动态类型语言（Python, JS）都是采用鸭子类型。（C++ 的 proxy 库可能也是？）

Java 可以通过反射来完成。

## 8. 头文件用了 libcurl 头文件，需要 pimpl 隐藏 libcurl 吗

问题的代码如下：

```cpp
#include <curl/curl.h>

#include <queue>

namespace Test {
class Client {
   public:
    struct TaskPackage {
        CURL *curl{nullptr};
        curl_slist *curlHeaders{nullptr};
    };

   private:
    std::queue<TaskPackage> m_queue{};
};
}  // namespace Test
```

不需要 pimpl。

头文件前置声明所需要的所有东西（CURL, curl_slist），源文件再 include curl.h。

如果 Client 这个类里面某个字段的类型是 libcurl 里面定义的，那就把这个字段定义成 unique_ptr。

这样头文件不需要感知任何 libcurl 里面定义的类型。

## 9. C++ 升个版本有那么难吗

正常情况下版本就是要规律更新的啊，语言也好依赖也好。锁死在某个旧版本是会欠技术债的。

一万年不升级，突然有一天想升，那当然全是问题；如果有完善的 CI，定期升小版本，基本每次升级一片绿，稍微改几个 deprecated 的接口，不是多恐怖的事情。

之所以叫债，就是因为它总有一天要还的。

当然这种事情是技术团队负责人而不是普通打工人应该做的。
