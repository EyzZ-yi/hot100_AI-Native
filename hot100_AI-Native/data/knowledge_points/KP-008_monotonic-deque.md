# KP-008: 单调队列（滑动窗口最大值）

## 核心思路
单调队列 = 单调栈 + 一条"队首按区间过期"的规则。

维护一个双端队列（deque），队列中存下标，保证对应值**从队首到队尾单调递减**（求最大）。
- 队首：当前窗口最大值的下标
- 入队时：从队尾移除所有比当前值小的元素（它们永远不会是最大值）
- 滑动时：若队首下标已不在窗口内（`queue.peek() <= i - k`），弹出队首

## 代码模板（LC239 滑动窗口最大值）
```java
Deque<Integer> deque = new ArrayDeque<>(); // 存下标，值单调递减
int[] result = new int[nums.length - k + 1];
for (int i = 0; i < nums.length; i++) {
    // 维护单调性：移除队尾中比 nums[i] 小的
    while (!deque.isEmpty() && nums[deque.peekLast()] < nums[i]) deque.pollLast();
    deque.offerLast(i);
    // 移除过期队首
    if (deque.peekFirst() <= i - k) deque.pollFirst();
    // 窗口满了才记录
    if (i >= k - 1) result[i - k + 1] = nums[deque.peekFirst()];
}
```

## 与单调栈的区别
单调栈不限制窗口大小；单调队列多了一步"队首过期淘汰"。

## 适用场景
- 固定窗口 k 内的最大/最小值（O(n)）

## 关联题目
LC239

## 掌握度历史
LC239：1
