# LC349 两个数组的交集

好的，我们一起来分析这道经典的哈希表应用题目。

## 1. 思路

这道题要求两个数组的交集，且输出结果中元素唯一，因此自动想到使用哈希集合（HashSet）来去重和快速查找。  
理由：哈希集合的查找操作是 O(1)，我们需要从第一个数组建立一个去重的集合，然后遍历第二个数组时，检查每个元素是否出现在第一个集合中，如果出现则加入结果集合。  
核心思想是：用集合代替数组，只保留唯一值，避免重复和顺序无关。

思路参考：  
[代码随想录 - 两个数组的交集](https://programmercarl.com/0349.%E4%B8%A4%E4%B8%AA%E6%95%B0%E7%BB%84%E7%9A%84%E4%BA%A4%E9%9B%86.html)

---

## 2. Java 代码

```java
import java.util.HashSet;
import java.util.Set;

class Solution {
    public int[] intersection(int[] nums1, int[] nums2) {
        // 1. 用 set1 存储 nums1 的所有元素（自动去重）
        Set<Integer> set1 = new HashSet<>();
        for (int num : nums1) {
            set1.add(num);
        }

        // 2. 遍历 nums2，用 resultSet 记录交集元素
        Set<Integer> resultSet = new HashSet<>();
        for (int num : nums2) {
            if (set1.contains(num)) {
                resultSet.add(num);
            }
        }

        // 3. 将结果集转换成 int[]
        int[] result = new int[resultSet.size()];
        int index = 0;
        for (int num : resultSet) {
            result[index++] = num;
        }
        return result;
    }
}
```

---

## 3. 时间复杂度 + 空间复杂度

- **时间复杂度：O(m + n)**  
  - 遍历 nums1 建立 set1：O(m)  
  - 遍历 nums2 查找交集：O(n)  
  - 哈希集合的 add 和 contains 都是 O(1)

- **空间复杂度：O(m + n)**  
  - 最坏情况下 set1 存 m 个元素，resultSet 存 min(m,n) 个元素  
  - 输出数组不计入额外空间（但通常也考虑结果集大小）

---

## 4. 关键点

- 哈希集合（HashSet）的快速查找与去重特性  
- 将数组元素转为集合，避免手动处理重复  
- 输出不要求顺序，所以集合天然合适  
- 典型面试题，适合考察集合与数组的转换，以及集合的基本操作