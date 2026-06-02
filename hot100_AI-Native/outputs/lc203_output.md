# LC203  移除链表元素

好的，我们来逐步分析这道题。

## 1. 思路

这道题的核心是 **单链表的节点删除操作**。删除节点时，需要找到它的前一个节点，让前一个节点的 next 指向待删除节点的 next。  
因为头节点可能被删除，一种常见的技巧是使用 **虚拟头节点（dummy head）**，这样头节点的处理就和普通节点统一，代码更简洁，不容易出错。  
[代码随想录链接](https://programmercarl.com/0203.%E7%A7%BB%E9%99%A4%E9%93%BE%E8%A1%A8%E5%85%83%E7%B4%A0.html)

## 2. Java 代码

```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode removeElements(ListNode head, int val) {
        // 创建虚拟头节点，指向head，避免单独处理头节点删除
        ListNode dummy = new ListNode(0);
        dummy.next = head;
        
        ListNode prev = dummy; // 前驱节点，初始指向虚拟头节点
        ListNode curr = head;  // 当前遍历节点
        
        while (curr != null) {
            if (curr.val == val) {
                // 删除当前节点：前驱节点的next跳过当前节点
                prev.next = curr.next;
            } else {
                // 不删除，移动前驱指针
                prev = curr;
            }
            // 当前指针始终向前移动
            curr = curr.next;
        }
        
        return dummy.next; // 返回真正的头节点
    }
}
```

## 3. 时间复杂度 + 空间复杂度

- **时间复杂度：O(n)** — 我们只遍历链表一次，n 为链表长度。
- **空间复杂度：O(1)** — 只使用了几个额外的指针，没有使用与 n 相关的额外空间。

## 4. 关键点

- **虚拟头节点（dummy head）**：统一处理头节点删除的情况，避免特殊判断。
- **指针移动的时机**：删除节点时，prev 不移动；不删除时，prev 前进到当前节点。
- **单链表删除的本质**：找到前驱，让前驱的 next 指向待删除节点的 next。