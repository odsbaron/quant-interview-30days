# 二叉树母题专项：在线阅读版

来源：本地资料 `hot100/二叉树母题专项Notebook.ipynb`。这是便于浏览的派生正文，保留来源中的题面与说明；不代表逐题答案或当前公司规则已核验。

[返回资料索引](../README.md)

只保留学习正文与代码；未运行代码，已排除输出、执行状态和无关网络/计费/凭证单元。示例可能包含解法，先独立完成当天任务，再对照阅读。

# 二叉树母题专项 Notebook（可运行 + 拓展题干）

覆盖遍历、深度、层序、BST 验证与 LCA。

## 如何高效使用这份 Notebook

1. 先读每题的“触发信号”，先会判题型。
2. 再读“快速理解”，明确状态变量与流程。
3. 运行代码单元，看样例输出与断言。
4. 最后做拓展题，按提示完成迁移。


```python
# 统一输出函数：把每个样例的输入、输出、期望展示出来，方便对照。
def show_case(title, inp, out, expected=None):
    print(f"[{title}]")
    print("input :", inp)
    print("output:", out)
    if expected is not None:
        print("expect:", expected)
    print("-" * 60)
```

```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(level):
    if not level or level[0] is None:
        return None
    root = TreeNode(level[0])
    q = deque([root])
    i = 1
    while q and i < len(level):
        node = q.popleft()
        if i < len(level) and level[i] is not None:
            node.left = TreeNode(level[i])
            q.append(node.left)
        i += 1
        if i < len(level) and level[i] is not None:
            node.right = TreeNode(level[i])
            q.append(node.right)
        i += 1
    return root
```

## 母题：94. 二叉树中序遍历

### 快速理解

**题干**
- 给定二叉树根节点 root，返回其中序遍历结果，顺序为左子树 -> 根节点 -> 右子树。

**触发信号**
- 树遍历基础题
- 左-中-右顺序

**代码阅读顺序**
1. 先看函数签名（参数和返回值）。
2. 看初始化变量（这些变量就是状态）。
3. 看主循环/递归（状态如何变化）。
4. 看返回语句（最终答案从哪里来）。

**手动模拟建议**
- 用一个最小样例跟着变量变化走 3~5 步。
- 重点观察：指针移动、哈希变化、栈/队列进出、DP 状态转移。

**复杂度（学习版估计）**
- 请结合代码结构自行评估（常见为 O(n)~O(n log n)）。


```python
# ==============================
# 母题：94. 二叉树中序遍历
# 这段代码分两部分：
# 1) 上半部分是算法函数；
# 2) 下半部分是样例与断言，便于你直接运行验证。
# ==============================

# 函数入口：inorder_traversal。先关注输入参数，再看返回值。
def inorder_traversal(root):
    ans = []
    # 函数入口：dfs。先关注输入参数，再看返回值。
    def dfs(node):
        # 分支判断：不同条件走不同处理路径。
        if not node:
            return
        dfs(node.left)
        ans.append(node.val)
        dfs(node.right)
    dfs(root)
    # 返回当前函数结果。
    return ans

root = build_tree([1, None, 2, 3])
out = inorder_traversal(root)
expected = [1, 3, 2]
show_case("Inorder Traversal", {"tree": [1, None, 2, 3]}, out, expected)
# 断言校验：若失败会抛异常，说明逻辑需要排查。
assert out == expected
# 输出提示，帮助你确认该题样例已通过。
print("母题通过")
```

### 拓展题（题干 + 提示）

**拓展题 1：144. 二叉树的前序遍历**
- 题干：返回节点值的前序遍历（中左右）。
- 提示：
  - 递归版直接改访问顺序。
  - 迭代版可用栈，先压右再压左。

**拓展题 2：145. 二叉树的后序遍历**
- 题干：返回节点值的后序遍历（左右中）。
- 提示：
  - 递归版最直观。
  - 迭代可前序变形后再反转结果。


## 母题：104. 二叉树的最大深度

### 快速理解

**题干**
- 给定二叉树 root，返回从根节点到最远叶子节点的最长路径上的节点数。

**触发信号**
- 求树高度
- DFS/BFS 都可

**代码阅读顺序**
1. 先看函数签名（参数和返回值）。
2. 看初始化变量（这些变量就是状态）。
3. 看主循环/递归（状态如何变化）。
4. 看返回语句（最终答案从哪里来）。

**手动模拟建议**
- 用一个最小样例跟着变量变化走 3~5 步。
- 重点观察：指针移动、哈希变化、栈/队列进出、DP 状态转移。

**复杂度（学习版估计）**
- 请结合代码结构自行评估（常见为 O(n)~O(n log n)）。


```python
# ==============================
# 母题：104. 二叉树的最大深度
# 这段代码分两部分：
# 1) 上半部分是算法函数；
# 2) 下半部分是样例与断言，便于你直接运行验证。
# ==============================

# 函数入口：max_depth。先关注输入参数，再看返回值。
def max_depth(root):
    # 分支判断：不同条件走不同处理路径。
    if not root:
        # 返回当前函数结果。
        return 0
    # 返回当前函数结果。
    return 1 + max(max_depth(root.left), max_depth(root.right))

# 准备测试样例：每组包含输入和期望输出。
cases = [
    ([3,9,20,None,None,15,7], 3),
    ([1,None,2], 2),
]
# 逐个运行样例，观察输出并与预期对比。
for level, expected in cases:
    out = max_depth(build_tree(level))
    show_case("Max Depth", {"tree": level}, out, expected)
    # 断言校验：若失败会抛异常，说明逻辑需要排查。
    assert out == expected
# 输出提示，帮助你确认该题样例已通过。
print("母题通过")
```

### 拓展题（题干 + 提示）

**拓展题 1：111. 二叉树的最小深度**
- 题干：返回从根到最近叶子节点的最短路径节点数。
- 提示：
  - 注意单子树节点不能直接取 min(left,right)。
  - 可用 BFS 首次遇到叶子即答案。

**拓展题 2：543. 二叉树的直径**
- 题干：求树中任意两节点最长路径长度（边数）。
- 提示：
  - 后序 DFS 返回高度，同时更新 left_height + right_height。
  - 全局变量维护最大直径。


## 母题：102. 二叉树的层序遍历

### 快速理解

**题干**
- 给定二叉树 root，按从上到下、从左到右的层序遍历返回每一层的节点值。

**触发信号**
- 按层输出节点
- 队列 BFS 模板

**代码阅读顺序**
1. 先看函数签名（参数和返回值）。
2. 看初始化变量（这些变量就是状态）。
3. 看主循环/递归（状态如何变化）。
4. 看返回语句（最终答案从哪里来）。

**手动模拟建议**
- 用一个最小样例跟着变量变化走 3~5 步。
- 重点观察：指针移动、哈希变化、栈/队列进出、DP 状态转移。

**复杂度（学习版估计）**
- 通常为 O(V+E) 或 O(m*n)（图/网格 BFS），空间与队列规模相关。


```python
# ==============================
# 母题：102. 二叉树的层序遍历
# 这段代码分两部分：
# 1) 上半部分是算法函数；
# 2) 下半部分是样例与断言，便于你直接运行验证。
# ==============================

from collections import deque

# 函数入口：level_order。先关注输入参数，再看返回值。
def level_order(root):
    # 分支判断：不同条件走不同处理路径。
    if not root:
        # 返回当前函数结果。
        return []
    q = deque([root])
    ans = []
    # 当条件成立时持续推进，直到边界条件触发退出。
    while q:
        size = len(q)
        level = []
        # 循环推进状态：每一步都在逼近最终答案。
        for _ in range(size):
            node = q.popleft()
            level.append(node.val)
            # 分支判断：不同条件走不同处理路径。
            if node.left:
                q.append(node.left)
            # 分支判断：不同条件走不同处理路径。
            if node.right:
                q.append(node.right)
        ans.append(level)
    # 返回当前函数结果。
    return ans

root = build_tree([3,9,20,None,None,15,7])
out = level_order(root)
expected = [[3], [9, 20], [15, 7]]
show_case("Level Order Traversal", {"tree": [3,9,20,None,None,15,7]}, out, expected)
# 断言校验：若失败会抛异常，说明逻辑需要排查。
assert out == expected
# 输出提示，帮助你确认该题样例已通过。
print("母题通过")
```

### 拓展题（题干 + 提示）

**拓展题 1：199. 二叉树的右视图**
- 题干：返回从右侧看到的节点值。
- 提示：
  - 层序遍历每层取最后一个节点。
  - 也可 DFS 先右后左并记录首次层号。

**拓展题 2：637. 二叉树的层平均值**
- 题干：返回每一层节点值的平均值。
- 提示：
  - 层序遍历时同步累加本层和。
  - 注意浮点除法。


## 母题：98. 验证二叉搜索树

### 快速理解

**题干**
- 给定二叉树 root，判断它是否是合法的二叉搜索树，即左子树所有值小于根、右子树所有值大于根，且左右子树也分别满足该性质。

**触发信号**
- BST 有序性判断
- 中序遍历应严格递增

**代码阅读顺序**
1. 先看函数签名（参数和返回值）。
2. 看初始化变量（这些变量就是状态）。
3. 看主循环/递归（状态如何变化）。
4. 看返回语句（最终答案从哪里来）。

**手动模拟建议**
- 用一个最小样例跟着变量变化走 3~5 步。
- 重点观察：指针移动、哈希变化、栈/队列进出、DP 状态转移。

**复杂度（学习版估计）**
- 请结合代码结构自行评估（常见为 O(n)~O(n log n)）。


```python
# ==============================
# 母题：98. 验证二叉搜索树
# 这段代码分两部分：
# 1) 上半部分是算法函数；
# 2) 下半部分是样例与断言，便于你直接运行验证。
# ==============================

# 函数入口：is_valid_bst。先关注输入参数，再看返回值。
def is_valid_bst(root):
    pre = [None]
    # 函数入口：dfs。先关注输入参数，再看返回值。
    def dfs(node):
        # 分支判断：不同条件走不同处理路径。
        if not node:
            # 返回当前函数结果。
            return True
        # 分支判断：不同条件走不同处理路径。
        if not dfs(node.left):
            # 返回当前函数结果。
            return False
        # 分支判断：不同条件走不同处理路径。
        if pre[0] is not None and node.val <= pre[0]:
            # 返回当前函数结果。
            return False
        pre[0] = node.val
        # 返回当前函数结果。
        return dfs(node.right)
    # 返回当前函数结果。
    return dfs(root)

# 准备测试样例：每组包含输入和期望输出。
cases = [
    ([2,1,3], True),
    ([5,1,4,None,None,3,6], False),
]
# 逐个运行样例，观察输出并与预期对比。
for level, expected in cases:
    out = is_valid_bst(build_tree(level))
    show_case("Validate BST", {"tree": level}, out, expected)
    # 断言校验：若失败会抛异常，说明逻辑需要排查。
    assert out == expected
# 输出提示，帮助你确认该题样例已通过。
print("母题通过")
```

### 拓展题（题干 + 提示）

**拓展题 1：230. 二叉搜索树中第 K 小的元素**
- 题干：返回 BST 中第 k 小的节点值。
- 提示：
  - 中序遍历天然有序。
  - 计数到第 k 个即可返回。

**拓展题 2：701. 二叉搜索树中的插入操作**
- 题干：向 BST 插入新值并保持其性质。
- 提示：
  - 递归或迭代沿着比较方向向下走。
  - 在空位处挂上新节点。


## 母题：236. 二叉树的最近公共祖先

### 快速理解

**题干**
- 给定二叉树 root 以及两个节点 p、q，返回它们的最近公共祖先节点。

**触发信号**
- 两节点公共祖先问题
- 后序 DFS 汇总信息

**代码阅读顺序**
1. 先看函数签名（参数和返回值）。
2. 看初始化变量（这些变量就是状态）。
3. 看主循环/递归（状态如何变化）。
4. 看返回语句（最终答案从哪里来）。

**手动模拟建议**
- 用一个最小样例跟着变量变化走 3~5 步。
- 重点观察：指针移动、哈希变化、栈/队列进出、DP 状态转移。

**复杂度（学习版估计）**
- 请结合代码结构自行评估（常见为 O(n)~O(n log n)）。


```python
# ==============================
# 母题：236. 二叉树的最近公共祖先
# 这段代码分两部分：
# 1) 上半部分是算法函数；
# 2) 下半部分是样例与断言，便于你直接运行验证。
# ==============================

# 函数入口：lowest_common_ancestor。先关注输入参数，再看返回值。
def lowest_common_ancestor(root, p, q):
    # 分支判断：不同条件走不同处理路径。
    if not root or root == p or root == q:
        # 返回当前函数结果。
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    # 分支判断：不同条件走不同处理路径。
    if left and right:
        # 返回当前函数结果。
        return root
    # 返回当前函数结果。
    return left if left else right

root = build_tree([3,5,1,6,2,0,8,None,None,7,4])
p = root.left
q = root.left.right.right
out = lowest_common_ancestor(root, p, q).val
expected = 5
show_case("Lowest Common Ancestor", {"tree": "sample", "p": 5, "q": 4}, out, expected)
# 断言校验：若失败会抛异常，说明逻辑需要排查。
assert out == expected
# 输出提示，帮助你确认该题样例已通过。
print("母题通过")
```

### 拓展题（题干 + 提示）

**拓展题 1：235. 二叉搜索树的最近公共祖先**
- 题干：在 BST 中求两节点最近公共祖先。
- 提示：
  - 利用 BST 性质：若都小于根去左，都大于根去右。
  - 首次分叉点即 LCA。

**拓展题 2：1123. 最深叶节点的最近公共祖先**
- 题干：返回所有最深叶节点的最近公共祖先。
- 提示：
  - 后序返回子树高度和对应 LCA。
  - 左右高度相同则当前节点为 LCA。


## 复盘建议

1. 能否复述这题的触发信号与核心状态变量？
2. 能否手写核心循环/递归并通过样例？
3. 能否把同套路迁移到两道拓展题？
4. 卡住时优先回看注释，再看拓展题提示。
