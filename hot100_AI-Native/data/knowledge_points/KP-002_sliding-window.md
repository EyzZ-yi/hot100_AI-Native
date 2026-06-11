# KP-002: 滑动窗口

## 核心思路
维护一个可变大小的窗口 `[left, right)`，right 向右扩展纳入元素，当条件满足时 left 向右收缩，全程只扫描一次（O(n)）。

关键点：收缩条件 `while (sum >= target)` 而不是 `if`——窗口需要尽可能缩小到极限才记录答案。

## 代码模板
```java
int left = 0, sum = 0, minLen = Integer.MAX_VALUE;
for (int right = 0; right < nums.length; right++) {
    sum += nums[right];
    while (sum >= target) {
        minLen = Math.min(minLen, right - left + 1);
        sum -= nums[left++];
    }
}
return minLen == Integer.MAX_VALUE ? 0 : minLen;
```

## 适用场景
- 连续子数组满足某个条件的最短/最长长度
- 固定窗口大小的最大/最小值

## 注意
- 收缩条件是 `≥` 而非 `=`（参见 EP-002：题意误读）
- 快慢指针≠滑动窗口，滑动窗口的 left 可以向右跳多步（参见 EP-003）

## 关联题目
LC209

## 掌握度历史
首次1→复习4
