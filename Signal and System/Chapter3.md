# 笔记

## 三角 Fourier 级数

当满足Dirichlet条件时，周期为$T$的周期信号$f(t)$可以在区间$ (t₁, t₁+T)$内表示为三角Fourier级数：

$$
\begin{aligned}
f(t) =& \frac{a_0}{2} + a_1 \cos \Omega t + a_2 \cos 2\Omega t + \cdots + a_n \cos n\Omega t + \cdots \\
&+ b_1 \sin \Omega t + b_2 \sin 2\Omega t + \cdots + b_n \sin n\Omega t + \cdots \\
=& \frac{a_0}{2} + \sum_{n=1}^{\infty} \left( a_n \cos n\Omega t + b_n \sin n\Omega t \right)
\end{aligned}
$$

其中 $\Omega = \dfrac{2\pi}{T}$ 为基波频率。

- $\dfrac{a_0}{2}$：直流分量
- $a_1 \cos \Omega t + b_1 \sin \Omega t$：基波分量
- $a_n \cos n\Omega t + b_n \sin n\Omega t \ (n>1)$：n次谐波分量

各分量系数

$$
a_0 = \frac{2}{T} \int_{t_1}^{t_1+T} f(t)\,dt
$$

$$
a_n = \frac{2}{T} \int_{t_1}^{t_1+T} f(t) \cos n\Omega t\,dt
$$

$$
b_n = \frac{2}{T} \int_{t_1}^{t_1+T} f(t) \sin n\Omega t\,dt
$$

$$
n = 1,2,3,\cdots
$$

通常取积分限为$(0,T)$或$(-T/2,T/2)$

直流分量
$$
\overline{f(t)} = \frac{1}{T} \int_{t_1}^{t_1+T} f(t)\,dt = \frac{a_0}{2}
$$

### 误差函数

实际应用中，只能取有限项来进行分析。

有限项Fourier级数：

$$
S_N(t) = \frac{a_0}{2} + \sum_{n=1}^{N} \left( a_n \cos n\Omega t + b_n \sin n\Omega t \right)
$$

误差函数：

$$
\varepsilon_N(t) = f(t) - S_N(t)
$$

均方误差（常用于判定系统性能指标，MSE）：

$$
E_N = \overline{\varepsilon_N^2(t)} = \frac{1}{T} \int_{t_1}^{t_1+T} \varepsilon_N^2(t) \,\mathrm{d}t
$$

$a_0, a_n, b_n$给出最小均方误差意义上的最佳近似。

$$
= \overline{f^2(t)} - \left[ a_0^2 + \frac{1}{2} \sum_{n=1}^{N} \left( a_n^2 + b_n^2 \right) \right]
$$

### 合并同频率项

两种常用表达式：三角型和余弦型

$$
\begin{aligned}
f(t) &= \frac{A_0}{2} + \sum_{n=1}^{\infty} A_n \cos\left( n\Omega t + \varphi_n \right), \quad t \in \left( t_1, t_1 + T \right) \\
&= \frac{a_0}{2} + \sum_{n=1}^{\infty} \left( a_n \cos n\Omega t + b_n \sin n\Omega t \right)
\end{aligned}
$$

$$
A_0 = a_0
$$

偶函数
$$
A_n = \sqrt{a_n^2 + b_n^2}
$$

奇函数
$$
\varphi_n = -\operatorname{arctg}\frac{b_n}{a_n}
$$

偶函数
$$
a_n = A_n \cos\varphi_n
$$

奇函数
$$
b_n = -A_n \sin\varphi_n
$$

在一定时间间隔内，任意一个代表信号的函数$f(t)$可以用一个直流分量和一系列谐波分量之和来表示。

## 频谱图

$A_n \sim nΩ$幅度频谱图（通常说频谱指幅度频谱），其中$A_0$为2倍直流分量。

$\varphi_n \sim nΩ$相位频谱图。

周期信号的频谱只出现在$nΩ$等离散频率点，是离散谱。

## 指数Fourier级数

周期为$T$的周期信号$f(t)$可以在区间$ (t₁, t₁+T)$内用指数Fourier级数表示为：

$$
f(t) = \sum_{n=-\infty}^{\infty} c_n \mathrm{e}^{jn\Omega t}
$$

基波频率
$$
\Omega = \frac{2\pi}{T}
$$

$$
c_n = \frac{1}{T} \int_{t_1}^{t_1+T} f(t) \mathrm{e}^{-jn\Omega t} \,\mathrm{d}t
$$

# 例题

## 例题1

> 利用周期性矩形脉冲与周期性三角脉冲的傅里叶级数展开式，求如图波形所示信号的傅里叶级数。
>
> ![](img/例题3.1.jpg)