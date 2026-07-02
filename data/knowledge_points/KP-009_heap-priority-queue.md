# KP-009: 堆 / 优先队列

## 核心思路
堆可以在 O(log k) 内维护"前 K 个最大/最小"元素，总复杂度 O(n log k)。

**小根堆维护前 K 大**：堆大小保持 ≤ k，堆顶是当前 K 大中最小的。新元素入堆后若堆大小超 k，弹出堆顶（最小的）。

## 代码模板（前 K 高频元素 LC347）
```java
// 统计频率
Map<Integer, Integer> freq = new HashMap<>();
for (int n : nums) freq.merge(n, 1, Integer::sum);

// 小根堆（按频率），大小维持 k
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
for (Map.Entry<Integer, Integer> e : freq.entrySet()) {
    pq.offer(new int[]{e.getKey(), e.getValue()});
    if (pq.size() > k) pq.poll();
}

// 收集结果
int[] result = new int[k];
for (int i = k - 1; i >= 0; i--) result[i] = pq.poll()[0];
```

## 特征信号
- "前 K 个"、"TopK"、"第 K 大/小" → 堆

## 适用场景
- 前 K 高频元素
- 流式数据中第 K 大元素

## 关联题目
LC347

## 掌握度历史
LC347：3
