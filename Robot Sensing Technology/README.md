# 《机器人传感技术》复习册

> 魏崃 · 第2至6章 · 信号分析、测试装置特性、传感原理、信号调理与信号处理

使用同目录下 `Robotics` 的 LaTeX 模板与风格：武汉大学校徽封面、樱花粉目录、Definition / Example / Question / Note 框及中文字体。模板原作者为 Zaahir Ali，与 Robotics 的署名一致。

`main.pdf` 为可直接阅读的成品；`main.tex` 为入口，`chapters/` 为正文。复习册涵盖信号分类、时频域描述、傅里叶级数、傅里叶变换性质、典型信号、脉冲序列、采样与随机信号基本概念，并附六组典型例题、频谱图、公式速查和知识自测。

正文按知识体系展开，用“复习重点”提示核心能力，并配方波谐波、正弦强度与矩形窗的紧凑示意图。例题给出完整信号定义、必要参数条件和独立推导；图中用符号标注未知参数、关键坐标及分情形条件。

第3章采用“知识梳理 → 完整例题推导 → 图示分析 → 公式速查与自测”的结构。内容包括静态标定与性能指标、LTI系统、传递函数/频率响应/冲激响应、一阶与二阶特性、参数选择及不失真测试条件，配有四组典型例题。配图涵盖静态误差、一阶与二阶幅相及阶跃响应、共同延迟、多频稳态输出和不同阻尼的比较。

第4章围绕敏感元件、物理效应与传感器选型展开，重点梳理应变片、电容与电感式测量、光电与霍尔效应、光纤传感和无损检测，并联系机器人接触与非接触感知。

第5章包括电桥、调制与解调、滤波器。典型例题给出单臂与双臂电桥的精确输出、全桥交流激励的边带频谱、带载波调幅、动态应变测量带宽、倍频程判断以及一阶低通的多频稳态响应。

第6章包括采样与抗混叠、量化、截断与窗函数、DFT与频率分辨能力、相关分析和功率谱分析，配有参数设计、混叠、相关延迟与频谱计算的完整例题。

正文在 `chapters/02-*.tex` 至 `chapters/06-*.tex`，各章共用入口、连续页码、目录和PDF书签，统一编译到现有 `main.pdf`。

## 编译

在本目录运行（需要 XeLaTeX 与 latexmk）：

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

绘图脚本为 `scripts/generate_figures.py`，需要 Python、NumPy 与 Matplotlib。现有 `img/*.pdf` 可直接用于编译，无须重新运行脚本。

第3章绘图脚本为 `scripts/ch3_figures.py`，同样需要 Python、NumPy 与 Matplotlib。运行 `python3 scripts/ch3_figures.py` 可重新生成第3章矢量图；不需要额外的课程参考PDF参与编译。

第4至6章的矢量图分别由 `scripts/ch4_figures.py`、`scripts/ch5_figures.py`、`scripts/ch6_figures.py` 生成，使用相同的绘图依赖。所有正文与配图均保存在本目录，后续可直接编辑章节源文件并重新编译整册。

原模板：[Template by Zaahir Ali](https://www.overleaf.com/latex/templates/template/cwqbynvjjzbx)。
