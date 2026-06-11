# KP-007: 单调栈

## 核心思路
维护一个底大顶小（或底小顶大）的栈，用于在 O(n) 内找到每个元素**左/右侧第一个更大/更小的元素**。

**操作规则（以"找右边第一个更大"为例）**：
- 遍历到 `i`：while 栈顶 < `nums[i]`，弹栈，记录"栈顶的右边第一个更大值 = `nums[i]`"
- 将 `i` 入栈

## 代码模板（每日温度 LC739）
```java
int[] result = new int[temps.length];
Deque<Integer> stack = new ArrayDeque<>(); // 存下标
for (int i = 0; i < temps.length; i++) {
    while (!stack.isEmpty() && temps[i] > temps[stack.peek()]) {
        int idx = stack.pop();
        result[idx] = i - idx;
    }
    stack.push(i);
}
```

## LC84 柱状图最大矩形 — 弹栈三元素
弹出 `mid` 时：
- **高度** = `h[mid]`（只用 mid 自己，不用新栈顶）
- **右边界** = `i`（触发弹栈的当前下标，不是 mid）
- **左边界** = 弹栈后新栈顶 `L`
- **面积** = `h[mid] * (i - L - 1)`（两端开区间）

## 单调栈 vs 单调队列
- 单调栈：找左/右第一个更大/更小（无区间限制）
- 单调队列：在固定窗口内找最大/最小（需要淘汰过期元素）

## 适用场景
- 右边第一个更大值（LC739, LC496）
- 循环数组右边第一个更大（LC503）—— 数组翻倍技巧
- 接雨水（LC42）
- 柱状图最大矩形（LC84）

## 关联题目
LC739, LC496, LC503, LC42, LC84

## 掌握度历史
LC739：1 | LC496：2 | LC503：2 | LC42：2 | LC84：1
