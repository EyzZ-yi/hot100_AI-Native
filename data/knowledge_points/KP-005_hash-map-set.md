# KP-005: 哈希表 / Map / Set

## 核心思路
利用哈希结构实现 O(1) 的存在性查询或计数，将"遍历+查找"从 O(n²) 降至 O(n)。

**三种形态**：
1. **数组模拟哈希**：字符集固定（如 26 个字母），用 `int[26]` 代替 HashMap，更快
2. **Set**：只关心"存不存在"（去重、交集）
3. **Map**：关心"存在几次"或"值是什么"（计数、存索引）

## 代码示例

```java
// 数组模拟（字母异位词）
int[] count = new int[26];
for (char c : s.toCharArray()) count[c - 'a']++;
for (char c : t.toCharArray()) count[c - 'a']--;
// 全0则异位词

// Map 存补值（两数之和）
Map<Integer, Integer> map = new HashMap<>();
for (int i = 0; i < nums.length; i++) {
    if (map.containsKey(target - nums[i])) return new int[]{map.get(target - nums[i]), i};
    map.put(nums[i], i);
}

// Map 计数 + 分组（四数相加 II）
Map<Integer, Integer> map = new HashMap<>();
for (int a : A) for (int b : B) map.merge(a + b, 1, Integer::sum);
int count = 0;
for (int c : C) for (int d : D) count += map.getOrDefault(-(c + d), 0);
```

## 适用场景
- 字符计数/异位词：数组模拟
- 集合交集/去重：Set
- 两数之和/四数相加（独立数组）：Map 存一半的和
- 状态循环检测：HashSet 记录访问过的状态（或用 Floyd 判圈替代）

## 关联题目
LC242（数组模拟）, LC349（Set）, LC1（Map 补值）, LC454（Map 计数）, LC202（Set 状态检测）

## 掌握度历史
LC242：3 | LC349：4→5 | LC1：5 | LC454：1→5 | LC202：1→3
