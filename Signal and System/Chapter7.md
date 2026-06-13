# 笔记

## 取样信号与取样定理

### 离散时间信号——序列

离散时间信号可以通过对连续时间信号进行取样得到，通常采用均匀时间间隔。若时间间隔为$T$，离散时间信号可以用$x(nT)$，或$x(n)$来表示，$n$为整数。

![](img/笔记7.1.png)

### 典型序列

单位函数序列
$$
\delta(k)=\begin{cases}1, &k=0 \\ 0, &k\neq 0\end{cases}
$$

$$
\delta(k-n)=\begin{cases}1, &k=n \\ 0, &k\neq n\end{cases}
$$

![](img/笔记7.2.png)

单位阶跃序列
$$
\varepsilon(k)=
\begin{cases}
1 & k \geq 0 \\
0 & k<0
\end{cases}
$$

$$
\varepsilon(k-n)=
\begin{cases}
1 & k \geq n \\
0 & k<n
\end{cases}
$$

单边指数序列
$$
e^{-k} \varepsilon(k)
$$

![](img/笔记7.4.png)

单边余弦序列
$$
\cos (\beta k) \varepsilon(k)
$$
![](img/笔记7.5.png)

## 取样信号

取样信号利用取样器（开关）实现。取样信号可看作原函数$f(t)$与开关函数$s(t)$的乘积。

$$
f_{S}(t)=f(t) s(t)
$$

对应频域关系为：
$$
f_S(t) \leftrightarrow \frac{1}{2\pi} F(j\omega) * S(j\omega)
$$
其中开关函数$s(t)$ 的取样间隔为$T_{S}$，$f_{S}=1 / T_{S}$称为取样频率。

### 理想取样信号

理想开关函数为周期冲激序列，对应的理想取样信号也称为冲激取样信号。

傅里叶变换对：
$$
f(t) \leftrightarrow F(j\omega),\quad \delta_{T_{S}}(t) \leftrightarrow \omega_{S} \delta_{\omega_{S}}(\omega)
$$

理想取样信号的时域表达式：
$$
f_{\delta}(t)=f(t) \delta_{T_{S}}(t) \leftrightarrow \frac{1}{2\pi} F(j\omega) * \omega_S \delta_{\omega_S}(\omega)
= \frac{1}{T_S} F(j\omega) * \delta_{\omega_S}(\omega)
$$

取样角频率定义：
$$
\omega_{S}=\frac{2 \pi}{T_{S}}
$$

![](img/笔记7.6.png)

### 理想取样信号的频谱特性

理想取样信号的频谱是原函数频谱的周期延拓，周期为$\omega_{S}=2 \pi / T_{S}$，具体特性如下：
- 各周期内的频谱形状与原信号频谱$F(j\omega)$ 相同
- 频谱幅度整体乘上因子$1 / T_{S}$
- 相邻周期频谱的间隔为$\omega_{S}$

理想取样信号的频谱展开式：
$$
F_\delta(j\omega) = \frac{1}{T_S} \sum_{k=-\infty}^{\infty} F\left( j\left(\omega - k\omega_S\right) \right)
$$

![](img/笔记7.7.png)

## 信号的重建

理想取样信号的频谱中，包含频率平移量为零的基带分量，其与原信号频谱形状相同，幅度为$\dfrac{1}{T_S}$。

将理想取样信号通过截止频率为$\dfrac{\omega_{S}}{2}$、通带内幅度为$T_S$、相位为零的理想低通滤波器，即可重建原信号。

### 信号重建的必要条件
要实现无混叠的信号重建，取样信号的频谱中两相邻周期的部分不能重叠，需满足以下条件：
1. 原信号 $F(j\omega)$ 为频带有限信号，即$|\omega| \leq \omega_{m}$
2. 取样角频率大于或等于信号最高角频率的2倍：
$$
\omega_{S} \geq 2 \omega_{m}
$$

当理想低通滤波器的截止频率满足
$$
\omega_{m} \leq \omega_{c} \leq \omega_{s}-\omega_{m}
$$
时，理想低通的输出端可以恢复出原信号。

相关定义：
- Shannon取样频率（Nyquist取样频率）：$2 \omega_{m}$ 或 $2 f_{m}$
- Shannon取样间隔（Nyquist取样间隔）：$1 / 2 f_{m}$ 或 $\pi / \omega_{m}$

### Shannon取样定理
一个在频谱中不包含大于频率$f_{m}$ 的分量的有限频带信号，由对该信号以不大于$1/(2f_m)$ 的时间间隔进行取样的取样值唯一确定。当这样的信号通过截止频率满足$\omega_{m} \leq \omega_{c} \leq \omega_{S}-\omega_{m}$ 的理想低通滤波器后，可以将原信号完全重建。

$$
\omega_{s} \geq 2 \omega_{m}
$$
$$
T_{s} \leq \frac{1}{2 f_{m}}
$$
$$
f_{m}=\frac{\omega_{m}}{2 \pi}
$$
$$
\omega_{s}=\frac{2 \pi}{T_{s}}
$$

