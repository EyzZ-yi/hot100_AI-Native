# KP-006: 栈的应用

## 核心思路
栈是"最近优先"结构，适用于：
- **括号/配对**：最近打开的必须最先关闭
- **相邻消除**：遇到匹配就弹栈消除
- **用两个栈模拟队列**（摊还思想）

## 特征信号 → 选栈
| 特征 | 结构 |
|------|------|
| 嵌套/配对/最近优先 | 栈 |
| 先进先出/层序 | 队列 |

## 代码示例

```java
// 有效括号（LC20）
Deque<Character> stack = new ArrayDeque<>();
Map<Character, Character> map = Map.of(')', '(', ']', '[', '}', '{');
for (char c : s.toCharArray()) {
    if (!map.containsKey(c)) { stack.push(c); continue; }
    if (stack.isEmpty() || stack.peek() != map.get(c)) return false;
    stack.pop();
}
return stack.isEmpty();

// 用栈实现队列（LC232）—— 懒搬运
// 只有 out 为空时才把 in 全倒入 out，平均 O(1)
```

## 适用场景
- 括号有效性（LC20）
- 相邻重复项删除（LC1047）
- 用两个栈模拟队列——懒搬运（LC232）

## 关联题目
LC20, LC1047, LC232

## 掌握度历史
LC20：1 | LC1047：4 | LC232：2
