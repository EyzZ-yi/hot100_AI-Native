# KP-010: Floyd 判圈算法（快慢指针）

## 核心思路
用快慢指针检测链表/状态序列中是否存在环，以及找到环的入口。

- **快指针**每次走 2 步，**慢指针**每次走 1 步
- 若有环，快慢指针必然相遇
- 相遇后，将一个指针重置到 head，两指针同步走，再次相遇处即**环入口**

## 代码模板（链表判环 + 找入口）
```java
ListNode slow = head, fast = head;
// 1. 判断是否有环
while (fast != null && fast.next != null) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow == fast) {
        // 2. 找入口
        ListNode index = head;
        while (index != slow) {
            index = index.next;
            slow = slow.next;
        }
        return slow; // 环入口
    }
}
return null;
```

## 快乐数（LC202）的应用
快乐数本质是状态机：`n → f(n) → f(f(n)) → ...`，要么终止（到 1），要么进入循环。
用 HashSet 记录访问过的值，或用 Floyd 判圈（把 `f(n)` 当"走一步"）。

## 适用场景
- 链表判环 + 找环入口（LC142）
- 状态机"终止 vs 无限循环"（LC202）

## 关联题目
LC142, LC202

## 掌握度历史
LC142：首次5→复习3（循环移动未掌握） | LC202：首次1→复习3
