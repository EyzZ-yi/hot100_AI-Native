# KP-011: 二叉树遍历（前中后序 + 层序 BFS）

## 前/中/后序遍历（递归）

```java
// 前序：根-左-右
void preorder(TreeNode node, List<Integer> res) {
    if (node == null) return;
    res.add(node.val);
    preorder(node.left, res);
    preorder(node.right, res);
}
```
中序和后序只需调换三行的顺序。

## 层序遍历（BFS）

**关键不变量**：每次进入外层 while 时，队列里恰好装着当前这一整层的全部节点。

```java
Queue<TreeNode> queue = new LinkedList<>();
queue.offer(root);
while (!queue.isEmpty()) {
    int size = queue.size(); // 快照当前层节点数
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

## 触发条件（层序）
题目要求"按层"：分层输出、每层最值/均值、最右节点、树的深度 → 调层序 BFS 模板。

## 关联题目
LC144/94/145（前中后序）, LC102（层序）

## 掌握度历史
LC144/94/145：4 | LC102：1
