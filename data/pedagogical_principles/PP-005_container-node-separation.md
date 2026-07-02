# PP-005: 链表设计中容器与节点分离

## 触发场景
需要封装链表 API（设计链表、LRU 缓存等）时，把节点类和容器类混写在一起。

## 原则内容
**节点**（`ListNode`）只负责 `val` 和 `next`（或 `prev`）。  
**容器**（`MyLinkedList`）持有 `size` 和 `dummyHead`，所有对外 API 由容器暴露。

## 底层理由
节点和链表是两个不同的抽象层次。混在一起时，`size` 的维护、边界检查会散落在节点操作里，互相干扰，逻辑难以追踪。分离后每一层的职责清晰，修改不越界。

## 应用方式
```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

class MyLinkedList {
    private int size;
    private ListNode dummyHead;
    MyLinkedList() { dummyHead = new ListNode(0); size = 0; }
    // addAtHead, addAtTail, addAtIndex, get, deleteAtIndex ...
}
```

## 关联题目
LC707

## 来源
LC707"关键学到的"；可推广到所有需要封装的链表/树数据结构
