# 《现代控制理论》复习资料

> 魏崃

复习资料主要参考武汉大学丁李老师的讲义、习题课和纸质练习答案。版式沿用《机器人学》课程笔记及 [Zaahir Ali 的 LaTeX 模板](https://www.overleaf.com/latex/templates/template/cwqbynvjjzbx)，感谢老师的讲授和模板作者的分享。

## 章节与题目

各章按讲义的知识主题分节，讲义例题、习题课题目与纸质练习均放在相关主题内。每道题给出完整题设和所求问题，需要读图的题目附相应图示。随后列出考点并分步解析。同一模型有多个小问或解法时合并展示，保留对应的原题号。同号而题设不同的讲义例题用标题或页码区分。

| 章 | 复习主题 | 习题课 | 纸质练习 |
| --- | --- | --- | --- |
| 1 | 反馈、经典控制、状态空间描述 | 讲义思考 1、2 |  |
| 2 | 模拟结构图、机理建模、输入输出实现、坐标变换、传递函数与系统连接 | 习题 1–8 | 一 |
| 3 | 定常与时变响应、矩阵指数、阶跃与零输入响应 | 习题 1–6 | 二、三 |
| 4 | 能控、能观、对偶、结构分解、规范形与最小实现 | 习题 1–9 | 四、七 |
| 5 | 平衡态、第一法与第二法、线性稳定性、雅可比矩阵法与变量梯度法 | 习题 1–5 | 五 |
| 6 | 状态与输出反馈、极点配置、解耦、全维状态观测器 | 习题 1–2 | 六 |

第 2 章的指定练习按《现代控制理论》第 3 版第 17 页图 1.7(b) 和第 39 页例 1-11 核对，题面、框图和解析均收录在册。[机械工业出版社样章试读](https://www.cmpedu.com/books/pdf.htm?CHAPTERMODEL=57417)

## 阅读与编译

从 PDF 目录可以直接跳到各复习主题。[阅读 main.pdf](./main.pdf)

章节源文件位于 [chapters](./chapters)，[main.tex](./main.tex) 为编译入口。使用包含 TikZ、PGFPlots 和 Circuitikz 的 TeX 环境，在本目录下运行两次 XeLaTeX 以更新目录和交叉引用。

```sh
xelatex -halt-on-error main.tex
xelatex -halt-on-error main.tex
```

### 能控性与能观性手册

汇总连续线性系统的状态能控性、输出能控性和状态能观性判据，附公式速查、例题与自测。[阅读 PDF](./controllability-observability-handbook.pdf) · [查看 LaTeX 源文件](./controllability-observability-handbook.tex)

在本目录下运行两次 XeLaTeX 编译手册。

```sh
xelatex -halt-on-error controllability-observability-handbook.tex
xelatex -halt-on-error controllability-observability-handbook.tex
```

### 能控性、能观性、规范形与最小实现手册

按第 4 章的记号汇总定常系统的能控与能观判据、结构分解、四种规范形和最小实现。附公式速查、完整例题及自测答案。[阅读 PDF](./state-space-structure-realization-handbook.pdf) · [查看 LaTeX 源文件](./state-space-structure-realization-handbook.tex)

在本目录下运行两次 XeLaTeX 编译手册。

```sh
xelatex -halt-on-error state-space-structure-realization-handbook.tex
xelatex -halt-on-error state-space-structure-realization-handbook.tex
```

### 第 5 章 李雅普诺夫稳定性考前解题复习册

按 150 分钟复习路线组织，逐步解出讲义例 5-1 至 5-12 和习题课第 1 至 5 题。重点是选判据、展开计算、检查零导数集合，以及写出局部或大范围稳定性的结论。[阅读 PDF](./lyapunov-stability-exam-review.pdf) · [查看 LaTeX 源文件](./lyapunov-stability-exam-review.tex)

在本目录下运行两次 XeLaTeX 编译复习册。

```sh
xelatex -halt-on-error lyapunov-stability-exam-review.tex
xelatex -halt-on-error lyapunov-stability-exam-review.tex
```
