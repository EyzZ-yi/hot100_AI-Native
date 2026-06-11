# PP-007: 状态机"终止 vs 循环"用 Floyd 判圈或 HashSet

## 触发场景
问题描述为"某个操作会无限重复 or 最终停止"，需要判断是否进入循环。

## 原则内容
对于状态机 `s → f(s) → f(f(s)) → ...`，判断是否进入循环有两种方法：
1. **HashSet**：记录所有访问过的状态，若 state 已在 set 中 → 有环
2. **Floyd 判圈（快慢指针）**：快指针每次走 2 步（`f(f(s))`），慢指针走 1 步（`f(s)`），相遇则有环；O(1) 空间

## 底层理由
状态空间有限时，"不终止"等价于"进入环"，Floyd 判圈是检测环的经典工具。LC202 的关键洞见：各位数字平方和最终 < 243（3位数上界），状态空间有限，必然终止或成环。

## 应用方式
```java
// LC202 快乐数（HashSet 版）
Set<Integer> seen = new HashSet<>();
while (n != 1 && seen.add(n)) n = sumOfSquares(n);
return n == 1;

// Floyd 版
int slow = n, fast = sumOfSquares(n);
while (fast != 1 && slow != fast) {
    slow = sumOfSquares(slow);
    fast = sumOfSquares(sumOfSquares(fast));
}
return fast == 1;
```

## 关联题目
LC142（链表环检测）, LC202（快乐数状态机）

## 来源
LC202"关键学到的"；配合 KP-010（Floyd 判圈）
