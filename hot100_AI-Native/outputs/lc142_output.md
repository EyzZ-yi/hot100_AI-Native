# LC142 环形链表 II

好的，这道题是关于检测链表环以及找到环的入口，是经典的“快慢指针”应用。

---

## 1. 思路

这道题有两个关键步骤：  
第一步，用快慢指针判断链表是否有环（快指针每次走两步，慢指针每次走一步，如果相遇说明有环）。  
第二步，当快慢指针相遇后，再从头和相遇点各用一个指针同步前进，它们相遇的位置就是环的入口。  
这个思路基于数学推导：从头到环入口的距离 = 从相遇点到环入口的距离。  

代码随想录参考链接：  
[代码随想录 - 环形链表II](https://programmercarl.com/0142.%E7%8E%AF%E5%BD%A2%E9%93%BE%E8%A1%A8II.html)

---

## 2. Java 代码（带注释）

```java
public class Solution {
    public ListNode detectCycle(ListNode head) {
        // 边界条件：空链表或只有一个节点，不可能有环
        if (head == null || head.next == null) return null;

        ListNode slow = head;
        ListNode fast = head;

        // 第一步：用快慢指针判断是否有环
        while (fast != null && fast.next != null) {
            slow = slow.next;        // 慢指针走一步
            fast = fast.next.next;   // 快指针走两步

            // 快慢指针相遇，说明有环
            if (slow == fast) {
                // 第二步：找到环的入口
                ListNode index1 = head;  // 从头开始
                ListNode index2 = slow;  // 从相遇点开始

                // 两个指针同步前进，相遇处就是环入口
                while (index1 != index2) {
                    index1 = index1.next;
                    index2 = index2.next;
                }
                return index1; // 返回环入口节点
            }
        }

        // 循环结束说明无环
        return null;
    }
}
```

---

## 3. 时间复杂度 + 空间复杂度

- **时间复杂度**：O(n)  
  快慢指针相遇前最多遍历整个链表，找环入口也最多遍历一次，总体是线性复杂度。

- **空间复杂度**：O(1)  
  只使用了几个指针变量，没有额外占用与链表长度相关的空间。

---

## 4. 关键点

- **快慢指针法**：判断是否有环的经典方法，快指针每次走两步，慢指针每次走一步，如果相遇则一定有环。
- **数学推导**：从头到环入口的距离 = 从相遇点到环入口的距离，从而实现找到环入口。
- **链表边界处理**：空链表或只有一个节点的链表不可能有环。
- **不要修改链表结构**：题目要求不允许修改链表，解法符合要求。