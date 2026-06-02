# LC209 长度最小的子数组

好的，我们一起来分析这道经典的滑动窗口题目。

---

## 1. 思路

这道题要求我们找到**和 ≥ target** 的**最短连续子数组**。因为数组元素都是正整数，我们可以用 **滑动窗口** 的方法：维护一个窗口，当窗口内元素和小于 target 时，右指针向右扩展；当和 ≥ target 时，尝试缩小左指针，并更新最短长度。  
为什么用滑动窗口？因为我们需要高效找到满足条件的最短子数组，而滑动窗口可以在 **O(n)** 时间内完成，无需暴力枚举所有子数组。

参考：代码随想录 - [长度最小的子数组](https://programmercarl.com/0209.%E9%95%BF%E5%BA%A6%E6%9C%80%E5%B0%8F%E7%9A%84%E5%AD%90%E6%95%B0%E7%BB%84.html)

---

## 2. Java 代码（带关键注释）

```java
class Solution {
    public int minSubArrayLen(int target, int[] nums) {
        int left = 0;
        int sum = 0;
        int minLen = Integer.MAX_VALUE; // 初始化为最大值

        // 滑动窗口：right 是窗口右边界
        for (int right = 0; right < nums.length; right++) {
            sum += nums[right]; // 扩大窗口

            // 当窗口内 sum >= target 时，尝试缩小窗口
            while (sum >= target) {
                // 更新最小长度
                minLen = Math.min(minLen, right - left + 1);
                // 缩小窗口：移除左边界元素
                sum -= nums[left];
                left++;
            }
        }

        // 如果 minLen 仍为初始值，说明没有符合条件的子数组
        return minLen == Integer.MAX_VALUE ? 0 : minLen;
    }
}
```

---

## 3. 时间复杂度 + 空间复杂度

- **时间复杂度：O(n)**  
  每个元素最多被 left 和 right 指针各访问一次，总共 2n 次操作，因此为 O(n)。

- **空间复杂度：O(1)**  
  只使用了常数个额外变量（left, sum, minLen），不依赖输入规模。

---

## 4. 关键点

- **滑动窗口技巧**：通过双指针维护一个动态窗口，避免重复计算子数组和。
- **窗口收缩条件**：当窗口内元素和满足条件时，及时收缩左边界，寻找更短解。
- **正整数特性**：元素均为正数，保证了窗口扩展时和只会增加，收缩时只会减少，这是滑动窗口能正确工作的前提。
- **初始值处理**：用 `Integer.MAX_VALUE` 作为最小长度初始值，最后判断是否更新过来决定返回 0 还是结果。