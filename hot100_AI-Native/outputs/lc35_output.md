# LC35 搜索插入位置

好的，我们开始讲解这道二分查找的经典题目。

---

### 1. 思路

题目要求 O(log n) 的时间复杂度，且输入是**排序数组**，这几乎就是明确提示使用**二分查找**。  
我们可以用二分查找直接在数组中搜索目标值：  
- 如果找到，直接返回 mid。  
- 如果没找到，循环退出时，`left` 指针会停在该插入的位置（因为此时 left 是第一个大于等于 target 的索引），直接返回 left 即可。

---

### 2. Java 代码

```java
public int searchInsert(int[] nums, int target) {
    int left = 0;
    int right = nums.length - 1;

    while (left <= right) {  // 标准二分循环
        int mid = left + (right - left) / 2;  // 避免溢出
        if (nums[mid] == target) {
            return mid;          // 找到目标，直接返回
        } else if (nums[mid] < target) {
            left = mid + 1;      // target 在右半部分
        } else {
            right = mid - 1;     // target 在左半部分
        }
    }

    // 循环退出时 left > right，left 就是插入位置
    return left;
}
```

---

### 3. 时间复杂度 + 空间复杂度

- **时间复杂度：O(log n)** —— 二分查找每次将搜索区间缩小一半。
- **空间复杂度：O(1)** —— 只使用了几个变量。

---

### 4. 关键点

- **二分查找模板**：掌握 `while (left <= right)` 的标准写法，以及 `left` 和 `right` 的更新规则。
- **区间不变量的理解**：循环结束时，`left` 总是第一个大于等于 target 的位置，这正好符合插入位置的定义。
- **边界条件处理**：例如 target 比所有元素都大时，left 会停在 `nums.length`，这个索引也是合法的插入位置。

---

如果还有不理解的地方，我可以再举几个例子帮你巩固。