# KP-004: 链表 Dummy 节点 & 容器-节点分离

## 核心思路
**Dummy 节点**：在 head 前插入一个哨兵节点，使 head 拥有前驱，从而统一"用 `cur.next` 操作"的逻辑，消除对 head 的特判。

```java
ListNode dummy = new ListNode(0);
dummy.next = head;
ListNode cur = dummy;
// ... 操作 cur.next
return dummy.next;  // 返回新 head
```

**容器-节点分离**（LC707）：
- `ListNode`：只持有 `val` 和 `next`
- `MyLinkedList`（容器）：持有 `size` 和 `dummyHead`，所有 API 通过容器暴露

## 何时加 dummy
- 需要：所有**可能修改 head**的操作（删除节点、头部插入、合并链表）
- 不需要：**不修改 head** 的操作（反转、遍历只读）——加了反而引入混淆（参见 EP-004）

## 关联题目
LC203（删除节点）, LC707（设计链表）, LC24（两两交换，需要 dummy 统一起点）
LC206（反转，不需要 dummy）

## 掌握度历史
LC203：首次1→复习2→复习3 | LC707：首次1 | LC24：首次1→复习4
