# PP-008: BFS 层序队列不变量

## 触发场景
用 BFS 做树/图的层序遍历，需要按层分组输出时。

## 原则内容
**不变量**：每次进入外层 `while` 时，队列里恰好装着、且只装着**当前这一整层的全部节点**。  
实现方式：进入 while 后**立即快照** `size = queue.size()`，用 for 循环精确消费 size 个节点。

## 底层理由
BFS 天然保证同层节点先于下层节点入队，但不用 `size` 快照的话无法区分"当前层结束"的边界。`size` 快照相当于在队列里画了一条层分隔线。

## 应用方式
```java
while (!queue.isEmpty()) {
    int size = queue.size(); // ← 不变量的保证
    List<Integer> level = new ArrayList<>();
    for (int i = 0; i < size; i++) {
        TreeNode node = queue.poll();
        level.add(node.val);
        if (node.left != null) queue.offer(node.left);
        if (node.right != null) queue.offer(node.right);
    }
    result.add(level);
}
```

## 触发条件（何时用层序模板）
题目包含：分层输出、每层最值/均值、最右节点、树的最大深度 → 直接套此模板。

## 关联题目
LC102

## 来源
LC102"关键学到的"；配合 KP-011（树遍历）
