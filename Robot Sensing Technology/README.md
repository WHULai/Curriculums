# 《机器人传感技术》复习册

> 魏崃 · 第2章：信号分析与描述 · 第3章：测试装置的基本特性

使用同目录下 `Robotics` 的 LaTeX 模板与风格：武汉大学校徽封面、樱花粉目录、Definition / Example / Question / Note 框及中文字体。模板原作者为 Zaahir Ali，与 Robotics 的署名一致。

`main.pdf` 为可直接阅读的成品；`main.tex` 为入口，`chapters/` 为正文。复习册涵盖信号分类、时频域描述、傅里叶级数、傅里叶变换性质、典型信号、脉冲序列、采样与随机信号基本概念，并附六组典型例题、频谱图、公式速查和知识自测。

正文按知识体系展开，用“复习重点”提示核心能力，并配方波谐波、正弦强度与矩形窗的紧凑示意图。例题给出完整信号定义、必要参数条件和独立推导；图中用符号标注未知参数、关键坐标及分情形条件。

第3章采用“知识梳理 → 完整例题推导 → 图示分析 → 公式速查与自测”的结构。内容包括静态标定与性能指标、LTI系统、传递函数/频率响应/冲激响应、一阶与二阶特性、参数选择及不失真测试条件，配有四组典型例题。配图涵盖静态误差、一阶与二阶幅相及阶跃响应、共同延迟、多频稳态输出和不同阻尼的比较。

第3章正文在 `chapters/03-*.tex`，两章共用入口、目录和PDF书签。

## 编译

在本目录运行（需要 XeLaTeX 与 latexmk）：

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

绘图脚本为 `scripts/generate_figures.py`，需要 Python、NumPy 与 Matplotlib。现有 `img/*.pdf` 可直接用于编译，无须重新运行脚本。

第3章绘图脚本为 `scripts/ch3_figures.py`，同样需要 Python、NumPy 与 Matplotlib。运行 `python3 scripts/ch3_figures.py` 可重新生成第3章矢量图；不需要额外的课程参考PDF参与编译。

原模板：[Template by Zaahir Ali](https://www.overleaf.com/latex/templates/template/cwqbynvjjzbx)。
