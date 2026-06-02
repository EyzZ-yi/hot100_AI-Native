# LC24 两两交换链表中的节点

好的，我们一起来分析这道题。  

## 1. 思路

这道题要求交换链表中相邻的两个节点，但不能只交换节点的值，必须修改节点的指针方向。最直接的方法是**使用递归**：每一层处理两个节点，交换后递归地处理后面的节点；另一种常用且空间更省的方式是**使用迭代 + 虚拟头节点**，通过三个指针（prev, node1, node2）调整指向。  

主要思路（迭代）：  
- 创建一个虚拟头节点 `dummy`，指向真正的头节点，方便统一处理头节点的交换。  
- 设置一个指针 `prev` 指向当前已处理完的链表的尾节点（开始是 dummy）。  
- 每次取 `prev` 后面的两个节点（first 和 second），如果没有两个节点，则结束循环。  
- 调整指针：先将 `prev` 指向 second，然后 first 指向 second 原本的下一个节点，最后 second 指向 first，完成一次交换。  
- 移动 `prev` 到 first（即交换后的第二个节点），继续下一轮。  

## 2. Java 代码（带关键步骤注释）

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
    public ListNode swapPairs(ListNode head) {
        // 虚拟头节点，方便处理头节点的变化
        ListNode dummy = new ListNode(0);
        dummy.next = head;
        
        ListNode prev = dummy;
        
        // 当后面至少有两个节点时才进行交换
        while (prev.next != null && prev.next.next != null) {
            ListNode first = prev.next;        // 第1个节点
            ListNode second = prev.next.next;  // 第2个节点
            
            // 交换：prev -> second -> first -> ...
            prev.next = second;                // 步骤1：prev指向second
            first.next = second.next;          // 步骤2：first指向second的下一个
            second.next = first;               // 步骤3：second指向first
            
            // 移动prev到交换后的第二个节点（即first）
            prev = first;
        }
        
        return dummy.next;
    }
}
```

## 3. 时间复杂度 + 空间复杂度

- **时间复杂度**：O(n)，其中 n 是链表的节点数，我们只遍历一次链表。  
- **空间复杂度**：O(1)，只使用了几个指针变量，没有额外占用与 n 相关的空间。  

## 4. 关键点

- 本题考察**链表的指针操作**，特别是**多个节点指针修改的顺序**，如果顺序错误可能导致链表断裂或死循环。  
- 使用 **虚拟头节点（dummy node）** 是链表操作的常用技巧，可以统一处理头节点被交换的情况。  
- 必须区分“修改节点内部值”和“修改节点链接”，这里明确要求只能修改链接。  
- 这道题也可以用递归解决，能帮助加深对递归+链表结构理解，但迭代的空间更优。  
- 对应代码随想录链接：[代码随想录-两两交换链表中的节点](https://programmercarl.com/0024.%E4%B8%A4%E4%B8%A4%E4%BA%A4%E6%8D%A2%E9%93%BE%E8%A1%A8%E4%B8%AD%E7%9A%84%E8%8A%82%E7%82%B9.html)