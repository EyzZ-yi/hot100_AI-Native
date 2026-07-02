# KP-003: 循环不变量

## 核心思路
在写循环之前，明确并固定区间语义（invariant），在整个循环体内严格遵守。

常见约定：
- `[left, right]`（全闭）：循环条件 `left <= right`，初始 `left=0, right=n-1`
- `[left, right)`（左闭右开）：循环条件 `left < right`，初始 `left=0, right=n`

## 示例（二分查找，左闭右开）
```java
int left = 0, right = nums.length; // right 是开区间边界
while (left < right) {             // 区间非空条件
    int mid = left + (right - left) / 2;
    if (nums[mid] < target) left = mid + 1;
    else right = mid;              // right 赋值为 mid（保持右开）
}
```

## 矩阵模拟（左闭右开每条边）
螺旋矩阵中，每条边都处理 `[start, end)`，由 offset 控制每圈的起始/结束，保证不重复处理角点。

## 适用场景
- 二分查找（必须固定全闭或左闭右开其中一种）
- 矩阵模拟（每条边统一约定）
- 任何含区间操作的题

## 关联题目
LC704, LC59

## 掌握度历史
LC704：首次1→复习5 | LC59：首次2→复习4
