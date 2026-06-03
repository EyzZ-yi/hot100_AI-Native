# LC19 删除链表的倒数第 N 个结点

好的，我们一起来详细分析这道 LeetCode 19 题。

## 1. 思路

这道题的关键是**在一次遍历中删除倒数第 N 个节点**。为了实现一次遍历，我们使用“快慢指针”技巧：让快指针先走 n 步，然后快慢指针同时前进，当快指针到达链表末尾时，慢指针恰好指向倒数第 N 个节点的前一个节点（方便删除）。  
我们还需要提前创建一个虚拟头节点（dummy node），这样能统一处理删除头节点的情况，代码会更简洁。  
参考思路：LeetCode 官方题解 + [代码随想录](https://programmercarl.com/0019.%E5%88%A0%E9%99%A4%E9%93%BE%E8%A1%A8%E7%9A%84%E5%80%92%E6%95%B0%E7%AC%ACN%E4%B8%AA%E7%BB%93%E7%82%B9.html)

## 2. Java 代码（带注释）

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
    public ListNode removeNthFromEnd(ListNode head, int n) {
        // 1. 创建虚拟头节点，避免处理头节点删除的边界情况
        ListNode dummy = new ListNode(0, head);
        
        // 2. 初始化快慢指针，都指向虚拟头节点
        ListNode fast = dummy;
        ListNode slow = dummy;
        
        // 3. 快指针先走 n 步
        for (int i = 0; i < n; i++) {
            fast = fast.next;
        }
        
        // 4. 快慢指针同时移动，直到快指针到链表末尾
        while (fast.next != null) {
            fast = fast.next;
            slow = slow.next;
        }
        
        // 5. 此时 slow 指向待删除节点的前一个节点
        slow.next = slow.next.next;   // 执行删除
        
        // 6. 返回真正的头节点（dummy.next）
        return dummy.next;
    }
}
```

## 3. 时间复杂度 + 空间复杂度

- **时间复杂度**：O(L) —— 其中 L 是链表长度，我们只遍历一次链表。
- **空间复杂度**：O(1) —— 只使用了常数额外空间（快慢指针 + 虚拟头节点）。

## 4. 关键点（考察知识点）

- **快慢指针技巧**：用一个固定步差让慢指针定位到倒数第 N 个节点的前驱节点。
- **虚拟头节点**：简化删除头节点等边界条件，统一操作逻辑。
- **链表遍历与节点删除**：熟悉链表基本的节点引用操作与垃圾回收无关的指针修改。
- **一次遍历的思路**：并非必须两次遍历，通过快慢指针提前走 N 步，两个指针正好间隔 N，可以一次完成定位。