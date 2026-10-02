[返回概率讲义目录](../probability_notes.md)

# 第三章随机过程：布朗运动


### 3.1 布朗运动的基本概念


**1. 布朗运动的概念**

称随机过程 $`\{W_t\}_{t \geq 0}`$ 为一维布朗运动（或标准布朗运动），若满足：

1.  $`W_0 = 0`$;

2.  具有独立增量；

3.  对任意 $`0 \leq s < t`$，有 $`W_t - W_s \sim \mathcal{N}(0, t - s)`$；

4.  路径几乎处处连续。

布朗运动具有如下性质：

1.  $`\mathbb{E}[W_t] = 0`$，$`\text{Var}(W_t) = t`$；

2.  $`\text{Cov}(W_s, W_t) = \min(s, t)`$；

3.  $`(W_t)`$ 为鞅；

4.  增量平稳：$`W_t - W_s \overset{d}{=} W_{t-s}`$。

**2. 反射原理**

设 $`\{W_t\}_{t \geq 0}`$ 为标准布朗运动，实数 $`\alpha > 0`$，则任意 $`t > 0`$，

则 $`W_t`$ 仍为布朗运动。由对称性可得结论。\
对任意 $`a > 0, t > 0`$,

``` math
\mathbb{P} \left( \sup_{0 \leq s \leq t} W_s < a \right) = 1 - 2\mathbb{P}(W_t \geq a).
```

**3. Itô 引理**

设 $`\{W_t\}_{t \geq 0}`$ 为布朗运动，$`X_t`$ 满足

``` math
dX_t = \mu(X_t)dt + \sigma(X_t)dW_t,
```

其中 $`\mu, \sigma`$ 光滑。若 $`f(t, x) \in C^1, C^2`$，则

``` math
df(t, X_t) = \left( f_t + \mu f_x + \frac{1}{2} \sigma^2 f_{xx} \right)(t, X_t)dt + \sigma(t, X_t)f_x(t, X_t)dW_t.
```

关键在于二阶项：$`(dW_t)^2 = dt, \quad dW_t = (dt)^2 = 0.`$

**4. Itô 等距 (Itô Isometry)**

设 $`\phi_t`$ 为适应且平方可积过程，则

``` math
\mathbb{E} \left[ \left( \int_0^t \phi_s \, dw_s \right)^2 \right] = \mathbb{E} \left[ \int_0^t \phi_s^2 \, ds \right].
```

若 $`\phi_t \in L^2[0, t]`$，则

``` math
\int_0^t \phi_s \, dw_s \sim \mathcal{N} \left( 0, \int_0^t \phi_s^2 \, ds \right).
```

Itô Isometry 常用于计算某些随机过程的方差。


### 3.1.1 基本计算


``` math
X = TW_t - \int_0^T t dW_t = \int_0^T (T - t) dW_t, \tag{3.1}
```

利用 Itô Isometry 可得

``` math
\text{Var}(X) = \mathbb{E}[X^2] = \int_0^T (T - t)^2 dt = \frac{T^3}{3}.
```

对 $`Y`$ 利用 Itô Isometry,

``` math
\text{Var}(Y) = \mathbb{E}[Y^2] = \int_0^T t^2 dt = \frac{T^3}{3}.
```

然后求 $`\text{Cov}(X, Y)`$，由 (3.1) 有

``` math
\text{Cov}(X, Y) = \mathbb{E}[XY] = \mathbb{E}\left[TW_T \int_0^T t dW_t\right] - \mathbb{E}\left[\left(\int_0^T t dW_t\right)^2\right].
```

其中

``` math
\mathbb{E}\left[TW_T \int_0^T t dW_t\right] = T \mathbb{E}\left[\int_0^T 1 dW_s \int_0^T t dW_t\right] = T \int_0^T t dt = \frac{T^3}{2}.
```

上述利用了 Itô 积分的另一性质：

``` math
\mathbb{E}\left[\int_0^T \int_0^T f(t, s) dW_t dW_s\right] = \int_0^T f(t, t) dt.
```

另一方面，

``` math
\mathbb{E}\left[\left(\int_0^T t dW_t\right)^2\right] = \text{Var}(Y) = \frac{T^3}{3}.
```

因此，

``` math
\text{Cov}(X, Y) = \mathbb{E}\left[TW_T \int_0^T t dW_t\right] - \mathbb{E}\left[\left(\int_0^T t dW_t\right)^2\right] = \frac{T^3}{2} - \frac{T^3}{3} = \frac{T^3}{6}.
```

最终我们有

``` math
\text{Corr}(X, Y) = \frac{\text{Cov}(X, Y)}{\sqrt{\text{Var}(X)\text{Var}(Y)}} = \frac{1}{2}.
```

**解答.** 将 $`t`$ 时刻的坐标记为 $`B_t = (X_t + 1, Y_t + 1)`$，其中 $`X_t`$ 与 $`Y_t`$ 为相互独立的一维标准布朗运动，满足 $`X_0 = Y_0 = 0`$。令
``` math
\tau := \inf\{t \geq 0 : X_t = -1\}.
```

则题目所求为 $`\mathbb{P}(Y_{\tau} + 1 > 0)`$。\
对标淮布朗运动 $`X_t`$，由反射原理得对任意 $`t > 0`$，\
``` math
\mathbb{P}(\tau \leq t) = \mathbb{P}(\min_{0 \leq s \leq t} X_s \leq -1) = 2\mathbb{P}(X_t \leq -1) = 2 \Phi \left( -\frac{1}{\sqrt{t}} \right),
```

其中 $`\Phi`$ 为标准正态分布函数。对 $`t`$ 求导得到 $`\tau`$ 的密度\
``` math
f_\tau(t) = \frac{1}{\sqrt{2\pi t^3}} \exp \left( -\frac{1}{2t} \right), \quad t > 0. \tag{3.2}
```

由于 $`Y_t`$ 与 $`\tau`$ 独立，且 $`Y_t \sim N(0, t)`$，故 $`Y_\tau`$ 的概率密度函数为\
``` math
g(y) = \int_0^\infty \frac{1}{\sqrt{2\pi t}} \exp \left( -\frac{y^2}{2t} \right) \cdot f_\tau(t) \, dt = \int_0^\infty \frac{1}{2\pi t^{1/2}} \exp \left( -\frac{1 + y^2}{2t} \right) \frac{1}{t} \, dt.
```

作代换 $`u = \frac{1}{t}`$，积分可得\
``` math
g(y) = \frac{1}{\pi (1 + y^2)}.
```

因此 $`Y_\tau`$ 为标准 Cauchy 分布。于是\
``` math
\mathbb{P}(Y_\tau > -1) = \int_{-\infty}^\infty \frac{1}{\pi (1 + y^2)} dy = \frac{1}{\pi} \left[ \arctan y \right]_{-\infty}^\infty = \frac{1}{\pi} \left( \frac{\pi}{2} + \frac{\pi}{4} \right) = \frac{3}{4}.
```

最终我们得到\
``` math
\mathbb{P}(Y_\tau + 1 > 0) = \frac{3}{4}.
```

**解答.** 记 $`X = W_{1/2}, Y = W_2 - W_{1/2}`$，则
``` math
X \sim \mathcal{N} \left( 0, \frac{1}{2} \right), \quad Y \sim \mathcal{N} \left( 0, \frac{3}{2} \right),
```

其中 $`X`$ 与 $`Y`$ 独立。\
令 $`Z = X + Y`$，题目所求即为 $`\mathbb{E}[X|Z=1]`$。不难有\
``` math
\text{Var}(Z) = 2, \quad \text{Cov}(X, Z) = \frac{1}{2}.
```

将 $`X`$ 对 $`Z`$ 进行回归可得\
``` math
X = \beta Z + \epsilon
```

其中\
``` math
\beta = \frac{\text{Cov}(X, Z)}{\text{Var}(Z)} = \frac{1}{4}.
```

且 $`\epsilon`$ 为均值为 0 的正态分布并与 $`Z`$ 独立。\
于是有\
``` math
\mathbb{E}[X|Z=1] = \mathbb{E}\left[\frac{1}{4}Z + \epsilon | Z = 1\right] = \frac{1}{4}.
```


## 3.2 鞅与停时


**1. 布朗运动的典型鞅**

设 $`\{W_t\}_{t \geq 0}`$ 为标准布朗运动，则以下表达式均为鞅，读者可自行验证：\
1. $`W_t`$。\
2. $`W_t^2 - t`$。

1.  时间反演型随机 $`t > 0`$:

``` math
tW_{1/t},
```

是关于 $`t`$ 的均匀分布，$`W_t: s \geq 1/t`$ 的鞅。


## 3.2.1 布朗运动停时问题


> 设 $`W_t`$ 为标准布朗运动。实数 $`a, b`$ 均大于 0，当 $`W_t`$ 首次到达 $`a`$ 或 $`-b`$ 时停止。试求：
>
> 1.  停止在 $`a`$ 内的概率；
>
> 2.  停止时间的期望。

**解答.** 设停时

``` math
\tau = \inf\{t \geq 0: W_t = a \text{ 或 } W_t = -b\}.
```

由于 $`W_t`$ 是鞅，由可选停时定理，

``` math
\mathbb{E}[W_\tau] = \mathbb{E}[W_0] = 0.
```

设 $`p = \mathbb{P}(W_\tau = a)`$，则

``` math
\mathbb{E}[W_\tau] = ap - b(1 - p) = 0,
```

解得停止在 $`a`$ 的概率为

``` math
p = \frac{b}{a + b}.
```

由于 $`W_\tau^2 - t`$ 是鞅，同理有

``` math
\mathbb{E}[W_\tau^2 - \tau] = 0,
```

即

``` math
\mathbb{E}[W_\tau^2] = \mathbb{E}[W_\tau^2] = 0.
```

代入 $`p = \frac{b}{a+b}`$，得

``` math
\mathbb{E}[r] = a^2 \frac{b}{a+b} + b^2 \frac{a}{a+b} = ab
```
