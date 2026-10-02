[返回概率讲义目录](../probability_notes.md)

# 第四章线性回归


## 4.1 OLS 回归


1.  一元线性回归系数与截距表达式

一元线性回归模型的基本表达式为：

``` math
Y_i = \beta_0 + \beta_1 X_i + \epsilon_i
```

其中 OLS 估计量的计算公式为：

``` math
\hat{\beta}_1 = \frac{\sum_{i=1}^n (X_i - \bar{X})(Y_i - \bar{Y})}{\sum_{i=1}^n (X_i - \bar{X})^2}, \quad \hat{\beta}_0 = \bar{Y} - \hat{\beta}_1 \bar{X}
```

其中，$`X`$ 和 $`Y`$ 分别是样本数据的均值。

1.  $`R`$ 方的定义

$`R`$ 方用于衡量回归模型的拟合优度，定义为：

``` math
R^2 = \frac{\text{ESS}}{TSS} = 1 - \frac{\text{RSS}}{TSS}
```

其中，$`TSS`$ 为总平方和，$`RSS`$ 为残差平方和，$`ESS`$ 为解释平方和，分别定义为：

``` math
TSS = \sum (Y_i - \bar{Y})^2, \quad RSS = \sum \epsilon_i^2, \quad ESS = \sum (\hat{Y}_i - \bar{Y})^2
```

显然，$`TSS = ESS + RSS`$。

**4. 多元回归的正交性**

在多元回归中，解释变量与残差之间的协方差为零，即：

``` math
Cov(X_i, \epsilon) = 0
```

这表明残差不包含解释变量的信息，回归估计量是无偏的。

**5. 回归估计量的性质（无偏性与方差）**

回归估计量具有以下重要性质：

- **无偏性**：$`\hat{\beta}`$ 的期望值等于真实的回归系数，即：

``` math
E(\hat{\beta} | X) = \beta
```

- **方差**：回归系数的方差为：

``` math
Var(\hat{\beta} | X) = \sigma^2 (X^T X)^{-1}
```

- **残差方差估计**：残差的方差估计为：

``` math
\sigma^2 = \frac{\hat{\sigma}^2}{n - k}
```

其中 $`n`$ 是样本量，$`k`$ 是回归系数的个数。

**6. 统计推断**

**t 检验**

用于检验单个回归系数的显著性，t 统计量为：

``` math
t = \frac{\hat{\beta}_1 - \beta_0}{\sqrt{\hat{\sigma}^2 (X^T X)^{-1}}} \quad t \sim t_{n-k}
```

其中，$`q`$ 是约束条件的数量。

- 整体显著性检验：

``` math
F = \frac{\frac{ESS}{k}}{\frac{RSS}{(n - k)}}
```


## 4.1.1 回归系数关系


> 设 $`Y`$ 对 $`X_1`$ 进行线性回归，回归系数为 $`a_1`$；$`Y`$ 对 $`X_1`$ 和 $`X_2`$ 同时进行回归，回归系数分别为 $`b_1`$ 和 $`b_2`$。问 $`a_1`$ 和 $`b_1`$ 的联联系数？

**解答.** 由一元回归 OLS 公式得

``` math
a_1 = \frac{\text{Cov}(Y, X_1)}{\text{Var}(X_1)}
```

对多元回归，利用 OLS 正交条件：

``` math
\text{Cov}(v, X_1) = 0, \quad \text{Cov}(v, X_2) = 0,
```

其中 $`v`$ 为残差离差 $`Y - \beta_0 + b_1 X_1 + b_2 X_2 + v`$。两边对 $`X_1`$ 取协方差得

``` math
\text{Cov}(Y, X_1) = b_1 \text{Var}(X_1) + b_2 \text{Cov}(X_2, X_1) + \text{Cov}(v, X_1).
```

代入 $`\text{Cov}(v, X_1) = 0`$，可得

``` math
\text{Cov}(Y, X_1) = b_1 \text{Var}(X_1) + b_2 \text{Cov}(X_1, X_2).
```


## 4.1.2 回归系数关系 (2)


> 设有随机变量 $`X_1, X_2`$ 和 $`Y`$，其中 $`X_1`$ 和 $`X_2`$ 的相关系数为 $`\rho`$。将 $`Y`$ 对 $`X_1`$ 进行线性回归，残差为 $`\varepsilon`$；将 $`X_2`$ 进行线性回归，回归系数为 $`\beta_1`$；将 $`Y`$ 对 $`X_1`$ 和 $`X_2`$ 进行线性回归，其中 $`X_2`$ 的回归系数为 $`\beta_2`$。问 $`\rho`$ 与 $`\beta_1`$ 和 $`\beta_2`$ 的关系。

**解答.** 记

``` math
\text{Var}(X_1) = \sigma_1^2, \quad \text{Var}(X_2) = \sigma_2^2, \quad \text{Cov}(X_1, X_2) = \sigma_{12}, \quad \rho = \frac{\sigma_{12}}{\sigma_1 \sigma_2}.
```

先将 $`Y`$ 对 $`X_1`$ 回归：

``` math
Y = aX_1 + \varepsilon, \quad a = \frac{\text{Cov}(Y, X_1)}{\sigma_1^2}.
```

再将 $`X_2`$ 对 $`X_1, X_2`$ 回归，其系数为

``` math
\beta_1 = \frac{\text{Cov}(Y, X_2)}{\sigma_2^2} = \frac{\text{Cov}(Y, X_2) - a \sigma_{12}}{\sigma_2^2} = \frac{\text{Cov}(Y, X_2) \sigma_{12} - \text{Cov}(Y, X_1) \sigma_{12}}{\sigma_1^2 \sigma_{12}}.
```

另一方面，将 $`Y`$ 对 $`X_1, X_2`$ 作多元线性回归，有：

``` math
Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \varepsilon, \quad \text{Cov}(\varepsilon, X_1) = \text{Cov}(\varepsilon, X_2) = 0.
```

由回归正交性，对 $`X_1`$ 取协方差：

``` math
\text{Cov}(Y, X_1) = \beta_1 \sigma_1^2 + \beta_2 \sigma_2^2.
```

对 $`X_2`$ 取协方差：

``` math
\text{Cov}(Y, X_2) = \beta_1 \sigma_1^2 + \beta_2 \sigma_2^2.
```

解该线性方程组。由第一式得

``` math
\beta_1 = \frac{\text{Cov}(Y, X_1) - \beta_2 \sigma_{12}}{\sigma_1^2}.
```

代入第二式：

``` math
\text{Cov}(Y, X_2) = \frac{\text{Cov}(Y, X_1) - \beta_2 \sigma_{12}}{\sigma_2^2}.
```


## 4.1.3 特定条件下的回归系数


> 设随机变量 $`X`$ 和 $`Y`$ 为相互独立的 0 到 1 的均匀分布，求在 $`X + Y > 1`$ 的条件下，$`Y`$ 对 $`X`$ 的回归系数。

**解答.** 记事件 $`A = \{X + Y > 1\}`$，则回归系数为

``` math
\beta = \frac{\text{Cov}(X, Y \mid A)}{\text{Var}(X \mid A)}.
```

先计算期望：

``` math
E[X \mid A] = 2 \int_0^1 x \cdot x \, dx = \frac{2}{3}, \quad E[Y \mid A] = \frac{2}{3}.
```

``` math
E[X^2 \mid A] = 2 \int_0^1 x^2 \, dx = \frac{2}{3}.
```

``` math
E[XY \mid A] = 2 \int_0^1 \int_0^1 xy \, dx \, dy = 2 \int_0^1 x \left( x - \frac{x^2}{2} \right) dx = \frac{5}{12}.
```

从而

``` math
\text{Cov}(X, Y \mid A) = \frac{5}{12} - \left( \frac{2}{3} \right)^2 = -\frac{1}{36}.
```

``` math
\text{Var}(X \mid A) = \frac{1}{2} - \left( \frac{2}{3} \right)^2 = \frac{1}{18}.
```

故得到回归系数

``` math
\beta = \frac{-1/36}{1/18} = -2.
```

**解答.** 设原模型为 $`y = X\beta + \varepsilon`$，则
``` math
\hat{\beta} = (X^T X)^{-1} X^T y.
```

复制样本后，\
``` math
\bar{X} = \begin{pmatrix} X \\ Y \end{pmatrix}, \quad \bar{y} = \begin{pmatrix} y \\ y \end{pmatrix}.
```

于是\
``` math
\hat{\beta}_{\text{new}} = (X^T X)^{-1} X^T \bar{y} = (X^T X)^{-1} (X^T X)^{-1} X^T y = \beta.
```

又\
``` math
\bar{X}^T X = 2X^T X,
```
\
且残差平方和\
``` math
RSS = 2RSS_s,
```
\
故\
``` math
\text{Var}(\hat{\beta}_{\text{new}}) = \sigma^2_{\text{new}} (X^T X)^{-1} \approx \frac{1}{2} \text{Var}(\beta).
```

从而标准误缩小为原来的 $`1/\sqrt{2}`$，故\
``` math
t_{\text{new}} = \sqrt{2} t,
```

$`p`$ 值随之减小。


### 4.1.5 回归系数关系 (3) (v1.1 update)


给定两个线性回归模型\
``` math
y = k_1 x + \varepsilon_1, \quad x = k_2 y + \varepsilon_2,
```
\
试问 $`k_1, k_2`$ 与 1 之间的大小关系。

**解答.** $`\text{Var}(x), \text{Var}(y)`$ 和 $`\text{Cov}(x, y)`$ 分别为样本方差与协方差。由 OLS 公式，
``` math
k_1 = \frac{\text{Cov}(x, y)}{\text{Var}(x)}, \quad k_2 = \frac{\text{Cov}(x, y)}{\text{Var}(y)}.
```

相乘即可得到:\
``` math
k_1 k_2 = \frac{\text{Cov}(x, y)}{\text{Var}(x)} \cdot \frac{\text{Cov}(x, y)}{\text{Var}(y)}.
```

Lasso 回归通过在最小二乘目标中加入 $`\ell_1`$ 正则项进行参数估计。其标准形式为\
``` math
\min_{\beta \in \mathbb{R}^p} \left\{ \frac{1}{2n} \|y - X\beta\|_2^2 + \lambda \|\beta\|_1 \right\},
```
其中 $`\lambda \geq 0`$ 为正则化参数，$`\|\beta\|_1 = \sum_{j=1}^p |\beta_j|`$。\
等价地，也常写作\
``` math
\min_{\beta} \{ \|y - X\beta\|_2^2 + \lambda \|\beta\|_1 \},
```
\
两种形式仅在常数缩放上不同。

**2. 岭回归**

岭回归通过在最小二乘目标中加入 $`\ell_2`$ 平方正则项进行参数估计。其标准形式为\
``` math
\min_{\beta \in \mathbb{R}^p} \left\{ \frac{1}{2n} \|y - X\beta\|_2^2 + \lambda \|\beta\|_2^2 \right\},
```
其中 $`\|\beta\|_2 = \sum_{j=1}^p \beta_j^2`$。\
岭回归目标函数为严格凸函数（当 $`\lambda > 0`$ 时），因此解唯一，并且具有解析解：\
``` math
\beta_{\text{ridge}} = (X^T X + n\lambda I_p)^{-1} X^T y,
```
\
若采用 $`\min_{\beta} \{ \|y - X\beta\|_2^2 + \lambda \|\beta\|_2^2 \}`$ 的目标函数形式，则对应解为\
``` math
\beta_{\text{ridge}} = (X^T X + \lambda I_p)^{-1} X^T y.
```

**3. 估计性质**

**(1) 岭回归的估计性质**

因此当 $`\lambda > 0`$ 时，\
``` math
\mathbb{E}[\hat{\beta}^{\text{ridge}}] \neq \beta^*,
```
\
岭回归是有偏估计。\
其协方差矩阵为\
``` math
\text{Var}(\hat{\beta}^{\text{ridge}}) = \sigma^2 (X^T X + \lambda I_p)^{-1} X^T X (X^T X + \lambda I_p)^{-1}.
```
\
与 OLS 相比，岭回归通过引入偏差降低了估计方差，体现了 bias-variance trade-off。\
此外，当 $`\lambda > 0`$ 时，$`X^T X + \lambda I_p`$ 始终可逆，即使 $`X^T X`$ 奇异（如 $`p > n`$），岭回归仍然有唯一解。

**(2) Lasso 的估计性质**

Lasso 回归目标函数中的 $`l_1`$ 正则项不可微，**一般不存在正则求解解**。\
与岭回归类似，当 $`\lambda > 0`$ 时 Lasso 也是有偏估计。\
Lasso 的方差表达式一般无显式形式，但在合适条件下可显著降低估计方差。另外 Lasso 回归的显著特征是大部分回归系数分量为 0，意味着 Lasso 回归在高维稀疏模型中表现突出。


### 4.2.1 回归系数为 0


**考虑 Lasso 回归**\
``` math
\min_{\beta} \left\{ \frac{1}{2n} \|y - X\beta\|_2^2 + \lambda \| \beta \|_1 \right\},
```
\
问 $`\lambda`$ 满足何种条件时，回归系数 $`\beta = 0`$?

**解答. 记**\
``` math
f(\beta) = \frac{1}{2n} \|y - X\beta\|_2^2.
```

当 $`\beta^* = 0`$ 时，\
``` math
\|\beta\|_2 = \{s \in \mathbb{R}^p : \|\Sigma\|_F \leq 1\}.
```
\
因此 0 为最优解当且仅当存在 $`\|\Sigma\|_F \leq 1`$ 使得\
``` math
0 = -\frac{1}{n} \Sigma_{ij} y_i + \lambda s_i,
```
\
即\
``` math
\frac{1}{n} \Sigma_{ij} y_i = \lambda s_i.
```
\
该式成立当且仅当\
``` math
\lambda \geq \frac{1}{n} \Sigma_{ij} y_i.
```
\
这样我们得到了使得回归系数全部为 0 的 $`\lambda`$ 的范围。


## 4.2.2 岭回归和 OLS 回归


设训练数据矩阵 $`X \in \mathbb{R}^{n \times p}`$，响应向量 $`y \in \mathbb{R}^n`$。考虑岭回归问题\
``` math
\min_{\beta} \{ \|y - X\beta\|_2^2 + \lambda \| \beta \|_2^2 \},
```
\
其中 $`\lambda > 0`$ 为正则化参数。记其最优解为 $`\beta^{\text{ridge}} \in \mathbb{R}^p`$。\
请构造新的训练数据矩阵 $`X'`$ 和响应向量 $`y'`$，使得对 $`(X', y')`$ 进行 OLS 回归所得估计\
``` math
\beta^{\text{OLS}} = \arg \min_{\beta} \|y' - X' \beta\|_2^2
```
\
满足\
``` math
\beta^{\text{OLS}} = \beta^{\text{ridge}}.
```

因此其平方范数可直接分块计算为

``` math
\|y - X\beta\|_2^2 = \left\| \left( y - X\beta \right) \right\|_2^2 = \|y - X\beta\|_2^2 + \|\sqrt{\lambda}\beta\|_2^2 = \|y - X\beta\|_2^2 + \lambda \| \beta \|_2^2.
```

从而问题目标函数完全相同，因此有相同的最优解：

``` math
\beta^{OLS} = \arg \min_{\beta} \|y - X\beta\|_2^2 = \arg \min_{\beta} (\|y - X\beta\|_2^2 + \lambda \| \beta \|_2^2) = \beta^{gradient}.
```
