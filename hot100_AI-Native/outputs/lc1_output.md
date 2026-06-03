# LC1 两数之和

好的，我们开始讲解 LeetCode 第 1 题 “两数之和”。

---

## 1. 思路

这道题最简单的做法是两层循环暴力枚举，但是时间复杂度很高。更优的方法是用 **哈希表**（HashMap），因为题目只要求找“一对”数，且每种输入只有一个答案。  
我们可以在遍历数组时，将已经看过的数字及其下标存到哈希表中，对于当前数字 `nums[i]`，检查 `target - nums[i]` 是否已存在于哈希表中：如果存在，直接返回两个下标，否则把当前数字和下标加入哈希表。  
这种方法只需要遍历一次数组，非常高效。

> 代码随想录链接：  
> [https://programmercarl.com/0001.两数之和.html](https://programmercarl.com/0001.两数之和.html)

---

## 2. Java 代码（带注释）

```java
import java.util.HashMap;
import java.util.Map;

public class Solution {
    public int[] twoSum(int[] nums, int target) {
        // 创建一个哈希表，用于存储“值 -> 下标”的映射
        Map<Integer, Integer> map = new HashMap<>();
        
        // 遍历数组
        for (int i = 0; i < nums.length; i++) {
            // 计算当前元素需要的另一个加数
            int complement = target - nums[i];
            
            // 检查哈希表中是否已经存在这个补数
            if (map.containsKey(complement)) {
                // 如果存在，返回这两个下标
                return new int[] { map.get(complement), i };
            }
            
            // 如果不存在，将当前元素及其下标加入哈希表
            map.put(nums[i], i);
        }
        
        // 根据题目保证存在答案，不会执行到这里
        return new int[] {};
    }
}
```

---

## 3. 时间复杂度 + 空间复杂度

- **时间复杂度：O(n)**  
  我们只遍历数组一次，每次哈希表操作（查找、插入）是 O(1)。
- **空间复杂度：O(n)**  
  最坏情况下，哈希表中存储 n 个元素。

---

## 4. 关键点

这道题考察的核心知识点是：
- **哈希表（HashMap）** 的灵活运用，利用其 O(1) 查找来降低时间复杂度。
- 理解什么时候用“空间换时间”来优化暴力解法。
- 思路的转化：将寻找两个数的和，转化为寻找一个数的“补数”是否出现过。

总结：典型的一道 **哈希表 + 一次遍历** 题目，也是后续很多题目的基础思路。