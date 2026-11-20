# 《现代控制理论》复习资料

> 魏崃

复习资料主要参考武汉大学丁李老师的讲义、习题课和纸质练习答案。版式沿用《机器人学》课程笔记及 [Zaahir Ali 的 LaTeX 模板](https://www.overleaf.com/latex/templates/template/cwqbynvjjzbx)，感谢老师的讲授和模板作者的分享。

## 章节与作业

各章先整理知识点，再按原题编号给出题面、对应知识点和分步解析。纸质练习随对应章节编排，保留原编号。

| 章 | 讲义 | 习题课 | 纸质练习 |
| --- | --- | --- | --- |
| 1 | 现代控制理论绪论 | 讲义第 3 页思考题 |  |
| 2 | 控制系统的状态空间模型 | 习题 1–8、讲义思考及指定教材例题 | 一 |
| 3 | 线性系统状态空间表达式的解 | 习题 1–6 | 二、三 |
| 4 | 线性系统的能控性和能观性 | 习题 1–9 | 四、七 |
| 5 | 李雅普诺夫稳定性分析 | 习题 1–5 | 五 |
| 6 | 线性系统综合 | 习题 1–2 | 六 |

第 2 章讲义所指的图 1.7(b) 和例 1-11 按《现代控制理论》第 3 版印刷页码核对。[机械工业出版社样章试读](https://www.cmpedu.com/books/pdf.htm?CHAPTERMODEL=57417)

## 阅读与编译

阅读 [main.pdf](./main.pdf)。章节源文件位于 [chapters](./chapters)，[main.tex](./main.tex) 为编译入口。在本目录下运行两次 XeLaTeX，以更新目录和交叉引用。

```sh
xelatex -halt-on-error main.tex
xelatex -halt-on-error main.tex
```
