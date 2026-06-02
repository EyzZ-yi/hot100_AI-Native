## EP-001: BFS visited 标记时机错误

### 触发场景
做 BFS 题目（如 LC207 课程表、LC102 二叉树层序）

### 错误表现
visited 在出队时才标记，导致同一节点多次入队，TLE 或 MLE

### 错误代码示例
```java
while (!queue.isEmpty()) {
    int node = queue.poll();
    visited[node] = true;  // ❌ 出队才标记
    for (int next : graph[node]) {
        if (!visited[next]) queue.offer(next);
    }
}
```

### 正确做法
入队时立刻标记 visited。

### 根因
对"visited 的语义"理解错误：visited 不是"已处理"，是"已规划处理"。

### 关联题目
LC207, LC102, LC994

