---
date: 2026/04/01
title: 败犬のC++每月精选 2026-03
next: false
prev:
  link: /2026/02
  text: 败犬のC++每月精选 2026-02
---

![img](/img/2026-03-index.png)

# 败犬のC++每月精选 2026-03

[[toc]]

## 1. “正方形继承长方形”悖论

周刊群偷点话题。

长方形-正方形是违反里氏替换的典型例子。如果正方形继承了长方形，setW、setH 也会继承过来，显然语义不对。

数学上的正方形是长方形，is-a 关系成立，但不代表对象语义的 is-a 成立。里氏替换要求子类必须满足父类的行为契约，这里就违反了。

正确做法是 Square 和 Rectangle 都继承 Shape。

## 2. MSVC std::format 编译期检查只对部分预定义的执行字符集生效

又是编码的坑。

编译期检查，比如类型不匹配 `std::format("{:d}", 42.0);` 或参数数量不对。

因为 std::format 要在编译期检查找占位符 `{` 0x7B 和 `}` 0x7D，有些多字节编码就可能在字符的后几个字节出现 0x7B / 0x7D 导致问题。

Windows 默认执行字符集绑定 Active Code Page，由于 Active Code Page 可变，所以支持 std::format 编译期检查就是要支持所有字符集，这不现实，于是就直接不做了。

所以要指定 `/utf-8`。UTF-8 的非 ASCII 字符可以保证每个字节最高位是 1，可以逐个字节解析，很容易实现。

GCC / Clang 基本上统一了 UTF-8 编码，就很少碰到这个问题。

## 3. std::gcd 的欧几里得算法和 stein 算法

<https://codeforces.com/blog/entry/137056>

欧几里得算法大家应该比较熟，是不断取模；新版 GCC 且标准 C++20 之后用了 stein 算法，不断去除公共 2 因子并相减。

stein 算法平均意义上更快，取模的开销太大了。但是特定输入比如 `gcd(1, 0x7fffffff)`，stein 要循环个 31 次，欧几里得 1-2 次就做完了。

上面文章作者大概就是被这种输入 hack 了。

## 4. noexcept 标记自定义函数能优化性能吗

noexcept 优化性能的例子，基本上只有移动构造或赋值。一般来说移动构造与移动赋值有 noexcept 保证时，vector 等有强异常安全保证的 STL 容器会使用移动，否则使用拷贝。也就是说，不加 noexcept，很多情况下移动构造等于白写。

除此之外影响很小。在零成本异常模型（如 Itanium ABI）下，理论上可以做到完全不影响非异常路径的代码。没错就是连一行代码都不会多。

例如：

```cpp
void foo();
void foo_noexcept() noexcept;

int bar() {
    try {
        foo();
    } catch (...) {
        return 1;
    }
    return 0;
}

int bar_noexcept() {
    try {
        foo_noexcept();
    } catch (...) {
        return 1;
    }
    return 0;
}

// bar():
//         sub     rsp, 8
//         call    foo()
//         xor     eax, eax
// .L1:
//         add     rsp, 8
//         ret
//         jmp     .L2

// bar() (.cold):
// .L2:
//         mov     rdi, rax
//         call    __cxa_begin_catch
//         call    __cxa_end_catch
//         mov     eax, 1
//         jmp     .L1

// bar_noexcept():
//         sub     rsp, 8
//         call    foo_noexcept()
//         xor     eax, eax
//         add     rsp, 8
//         ret
```

可以看到 bar 和 bar_noexcept 的汇编几乎一样，只是多了 `bar() (.cold)` 这个异常路径，对非异常路径是没有影响的。

注意我说了“理论上”，实际上会出现本来能做的优化，加了或去掉 noexcept 就不优化了的情况，可以属于编译器 bug。

## 5. OI 国家集训队论文提到了 Cache Thrashing

<https://github.com/Fesdrer/NOIpaper> 2024 年。

一个大数组，如果反复访问步长是 2 的幂的地址，在组相联映射的机器，读写压力全在一个缓存组。这就会导致缓存不断被“驱逐”。

## 6. 模板参数里的右移符号

```cpp
std::array<int, 10 >> 2> a;    // error
std::array<int, (10 >> 2)> a;  // ok
```

不加括号就会被识别为模板的尖括号。

这是因为 [Maximal munch 规则](https://en.cppreference.com/w/cpp/language/translation_phases.html#Maximal_munch):

> If the next two characters are `>>` and one of the `>` character can complete a template identifier, the character is treated as a preprocessing token alone instead of being part of the preprocessing token `>>`.

如果第一个 `>` 可以匹配尖括号 `<...>`，那它就是尖括号而不是右移的一部分。这样 `vector<vector<int>>` 就不用写成 `vector<vector<int> >`。

## 7. stop_callback 谁来执行

```cpp
#include <print>
#include <stop_token>
#include <thread>

using namespace std::literals;

void task(std::stop_token token, int num) {
    auto id = std::this_thread::get_id();
    std::println("call task({})", num);

    std::stop_callback cb1{token, [num, id] -> void {
                               std::println("- STOP1 requested in task({}, {})", num, id == std::this_thread::get_id());
                           }};
    std::this_thread::sleep_for(9ms);

    std::stop_callback cb2{token, [num, id] -> void {
                               std::println("- STOP2 requested in task({}, {})", num, id == std::this_thread::get_id());
                           }};
    std::this_thread::sleep_for(4ms);
}

int main() {
    std::jthread thread{[](std::stop_token token) -> void {
        for (int i = 0; i < 2; i++) task(token, i);
    }};

    std::this_thread::sleep_for(20ms);
    std::println();
}
```

输出是：

```text
call task(0)
call task(1)

- STOP1 requested in task(1, false)
- STOP2 requested in task(1, true)
```

首先第一个 task 执行时，stop_callback 直到析构也没有 `request_stop()`，所以不会执行 stop_callback。

第二个 task 执行时，主线程析构了 jthread，此时就会 `request_stop()` 然后 `join()`。这个动作正好发生在 cb1 构造后 cb2 构造前。

<https://zh.cppreference.com/w/cpp/thread/stop_callback.html>:

> Callback functions registered via stop_callback's constructor are invoked either in the same thread that successfully invokes `request_stop()` for a std::stop_source of the stop_callback's associated std::stop_token; or if stop has already been requested prior to the constructor's registration, then the callback is invoked in the thread constructing the stop_callback.

意思是构造结束的 stop_callback 会在发起 `request_stop()` 的线程调用。`request_stop()` 后的 stop_callback 会在这个线程直接执行。

所以就能看到输出 false, true。

## 8. 群友写 gpu 的 sgemm 有感

> 之前太习惯乱序执行，寄存器重命名之类的优化手段了，以至于完全没意识到 gpu 上没这些东西。cpu 上写我就把流水大概排一排就行，到时候乱序一下性能没差别；gpu 上就必须精细，cpu 上我想办法解真依赖就行，但是 gpu 上我还要解假依赖……
>
> 感觉这些问题如果是初步接触 gpu 编程的人反而不容易忽略，但是我在 cpu 上写多了，下意识就认为这种地方不影响性能。
>
> 比如说你在 cpu 上处理一个序列，每次循环先读，再算，最后写回，读->算中间有延迟对吧，但是靠乱序其实就无所谓，反正下一圈循环的读可以提前执行，延迟自动就没了。所以我根本没在意过这个延迟。gpu 上就不一样，没有乱序，所以要么显式填充无关的运算指令要么多开线程靠调度掩盖延迟，反正得显式处理。
>
> 再比如 cpu 上遇到假依赖我都下意识忽略的，反正它自己会寄存器重命名，但是 gpu 就不行，真假依赖都要处理。

—— CuKing

## 9. 为什么大模型长上下文注意力涣散

事实上，一些大模型支持 1M / 2M 上下文，但是可能几百k 长度时就开始注意力涣散了。

一个原因是 attention softmax 稀释，序列太长导致 softmax 分母太大。这个问题可以用 sparse attention 缓解。

除此之外，位置编码退化、训练因素也会有影响。

## 10. 关于 AI 工作流的群友说法

人不要在中间暂停火车，让它等你 review 完。而是要用沙箱 / git 把火车变成可撤回的，人做延后审计，不要阻碍 AI 的工作流。

要投入大量时间去建设工作流，而不是 case by case 的去做 —— 不过这个事情也只是有几个月的价值。未来 agent 厂商会把这件事做好的。但现在程序员能做的最有价值的事情一定是这个。

现在大家很多 FOMO 情绪，但实际上如果你不是属于创业者这一部分的话，焦虑是不大的。因为现在大家生产力差距很大，是因为工具链的不完善，龙虾和 AI coding 工具都不完善，所以用的好的人和用不好的人差距很大。但到未来稳定状态，这些东西一定都会很完善，变得非常易用。真正拉开差距的不在你学会新技能多快。还是在于整个软件行业的视野和用户视角。

## 11. 一些文章

[1865年《红旗法案》的幽灵，仍在今天游荡](https://mp.weixin.qq.com/s/JdWcWiBuYoRUwGOsEKogmQ) “但这种担忧本质上仍是在用旧秩序的‘个体责任制’去套用新物种。正如我们不再要求航空公司为每一场飞行颠簸找一个具体的人为过失，而是建立系统性的航空安全审计与高额保险补偿机制。”

[Weak AVL：一种新的平衡二叉搜索树](https://lancern.xyz/posts/2026/01/wavl)

[Agentic Engineering in 2026.3: one 🦞 to rule them all](https://mp.weixin.qq.com/s/FQC_G26_CPSMokx_NSH6tA) 群主力荐的文章。

[c语言怎么“简单”表示9个变量互不相等?](https://www.zhihu.com/question/597274781/answer/3042727874) 双调排序。

[如何评价anthropic在可解释性方面工作？](https://www.zhihu.com/question/1911022705769152635/answer/2004915744811529185)

[对话 Google 首席 Jeff Dean：概率性执行的 Agent 时代，Infra 必须重塑！](https://mp.weixin.qq.com/s/8TYMn2DVE6vTo4xL64CkJA)
