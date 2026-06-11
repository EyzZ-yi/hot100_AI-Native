# KP-001: 双指针 / 快慢指针

## 核心思路
用两个指针（同向或对向）在线性结构上扫描，以 O(n) 代替暴力 O(n²)。

**快慢指针（同向）**：快指针寻找目标元素，慢指针指向结果数组的写入位置。

**对向双指针**：左右从两端向中间收缩，适合有序数组的配对/求和问题。

## 代码模板（快慢指针 - 移除元素）
```java
int slow = 0;
for (int fast = 0; fast < nums.length; fast++) {
    if (nums[fast] != val) {
        nums[slow++] = nums[fast];
    }
}
return slow;
```

## 代码模板（对向双指针 - 有序数组平方）
```java
int left = 0, right = nums.length - 1, pos = nums.length - 1;
while (left <= right) {
    if (Math.abs(nums[left]) > Math.abs(nums[right])) {
        result[pos--] = nums[left] * nums[left++];
    } else {
        result[pos--] = nums[right] * nums[right--];
    }
}
```

## 适用场景
- 移除/过滤数组元素（原地）
- 有序数组：平方后排序、两数之和
- 字符串反转
- 链表：找倒数第 N 个节点（快指针先走 N 步）

## 关联题目
LC27（快慢）, LC977（对向）, LC19（链表快慢）, LC206（链表反转双指针）, LC15（排序+对向）

## 掌握度历史
LC27：首次1→复习仍需巩固 | LC977：首次1→复习4 | LC19：首次3→复习5
