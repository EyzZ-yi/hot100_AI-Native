# LC707 设计链表

好的，我们一起来分析这道题。  

## 1. 思路  
这道题是设计一个基础的数据结构——链表，可以选择单链表或双链表实现。使用单链表配合一个虚拟头节点（dummy head），可以简化插入和删除时处理头节点的逻辑。核心是维护一个长度变量和一个虚拟头节点，通过遍历到指定位置来完成增删查的操作。  
这样写更规范，也方便在面试中快速实现、减少边界条件的 bug。  
参考链接：https://programmercarl.com/0707.%E8%AE%BE%E8%AE%A1%E9%93%BE%E8%A1%A8.html  

## 2. Java 代码（带关键注释）

```java
class MyLinkedList {
    // 定义链表节点内部类
    class ListNode {
        int val;
        ListNode next;
        ListNode(int val) {
            this.val = val;
        }
    }
    
    private ListNode dummyHead; // 虚拟头节点
    private int size;           // 链表长度

    public MyLinkedList() {
        dummyHead = new ListNode(0); // 虚拟节点，不存有效数据
        size = 0;
    }
    
    // 获取第 index 个节点的值，下标从 0 开始，无效返回 -1
    public int get(int index) {
        if (index < 0 || index >= size) {
            return -1;
        }
        ListNode cur = dummyHead.next;
        for (int i = 0; i < index; i++) {
            cur = cur.next;
        }
        return cur.val;
    }
    
    // 在头部添加节点
    public void addAtHead(int val) {
        addAtIndex(0, val);
    }
    
    // 在尾部添加节点
    public void addAtTail(int val) {
        addAtIndex(size, val);
    }
    
    // 在第 index 个节点前插入新节点
    public void addAtIndex(int index, int val) {
        if (index > size) return;
        if (index < 0) index = 0;
        
        ListNode prev = dummyHead;
        for (int i = 0; i < index; i++) {
            prev = prev.next;
        }
        ListNode newNode = new ListNode(val);
        newNode.next = prev.next;
        prev.next = newNode;
        size++;
    }
    
    // 删除第 index 个节点
    public void deleteAtIndex(int index) {
        if (index < 0 || index >= size) return;
        
        ListNode prev = dummyHead;
        for (int i = 0; i < index; i++) {
            prev = prev.next;
        }
        prev.next = prev.next.next;
        size--;
    }
}
```

## 3. 时间复杂度 + 空间复杂度  
- **时间复杂度**：  
  - `get`, `addAtIndex`, `deleteAtIndex`：O(n)（n 为链表长度，需要遍历到目标位置）  
  - `addAtHead`, `addAtTail`：O(1) 或 O(n)（`addAtHead` 借助 `addAtIndex(0,val)` 也是 O(1)，“addAtTail”在本写法中是 O(n) ，因为需要遍历到末尾）  
- **空间复杂度**：O(n)，存储 n 个节点  

## 4. 关键点  
这道题主要考察：  
- 基础链表节点类的定义和使用  
- 虚拟头节点（dummy node）的技巧，简化边界操作  
- 对索引边界条件的判断（有效范围、等于size、小于0的合法性）  
- 增删操作时指针的改变顺序，防止断链