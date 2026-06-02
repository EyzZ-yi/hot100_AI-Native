# LC139 单词拆分

好的，我们来看这道经典的 LeetCode 139 题「单词拆分」。

---

## 1. 思路

这道题本质上是一个**完全背包问题**，可以看作是「能否用字典里的单词拼出整个字符串」。  
因为单词可以重复使用，并且我们关心的是**字符串的某个前缀能否被拼出来**，所以用**动态规划（DP）**非常合适：  
我们定义 `dp[i]` 表示字符串 `s` 的前 `i` 个字符（即 `s[0..i-1]`）能否被字典中的单词拼接而成，最终答案就是 `dp[n]`。

---

## 2. Java 代码（带关键注释）

```java
import java.util.List;
import java.util.HashSet;
import java.util.Set;

class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        // 将字典转为 HashSet，方便 O(1) 判断单词是否存在
        Set<String> dict = new HashSet<>(wordDict);
        int n = s.length();
        
        // dp[i] 表示字符串 s 的前 i 个字符能否被拆分
        boolean[] dp = new boolean[n + 1];
        dp[0] = true; // 空字符串可以被认为是可以拼出来的
        
        // 遍历每个位置作为子串的结尾
        for (int i = 1; i <= n; i++) {
            // 枚举可能的分割点 j
            for (int j = 0; j < i; j++) {
                // 如果前 j 个字符能拼出来，并且 s[j..i-1] 在字典中
                if (dp[j] && dict.contains(s.substring(j, i))) {
                    dp[i] = true;
                    break; // 已经找到一种拆分方式，不需要继续尝试其他 j
                }
            }
        }
        
        return dp[n];
    }
}
```

---

## 3. 时间复杂度 & 空间复杂度

- **时间复杂度**：O(n² × m)  
  - 外层循环 i 从 1 到 n，内层循环 j 从 0 到 i-1，总共约 n²/2 次。  
  - 每次需要截取子串 `s.substring(j, i)`，这个操作是 O(m) 的（m 为子串长度），最坏情况下为 O(n)。  
  - 因此最坏 O(n³)。  
  *优化*：用哈希集合 + 限制单词最大长度，可以把截取复杂度降到 O(L)，整体 O(n²)。

- **空间复杂度**：O(n + 字典大小)  
  - dp 数组长度为 n+1，哈希集合存储字典单词。

---

## 4. 关键点

- **动态规划状态定义**：`dp[i]` 表示前缀 `s[0..i-1]` 是否可拆分。
- **状态转移**：`dp[i] = dp[j] && s[j..i-1] in dict`，找任意一个 j 使得条件成立即可。
- **完全背包思想**：字典中的单词可以重复使用，顺序无关，只关心能否组成当前前缀。
- **剪枝优化**：一旦找到可行的 j，立即 break，提高效率。
- **考察知识点**：动态规划 + 哈希集合快速查找 + 字符串截取与组合。

---

这样你就可以清晰地理解并讲解这道“单词拆分”问题了。