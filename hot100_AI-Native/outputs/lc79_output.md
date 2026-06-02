# LC79 单词搜索

好的，我们一起来分析这道经典的搜索题。

## 1. 思路（为什么用这个方法）

这道题要在一个二维网格中找一条路径，拼出给定的单词，所以本质是一个**路径搜索**问题。由于相邻单元格只能是上下左右，而且每个单元格不能重复使用，最直接高效的方法就是**深度优先搜索（DFS）+ 回溯**。DFS 负责沿着一个方向试探性地往下走，回溯则处理走不通时退回上一步，回到上一个状态。

同时，为了避免在网格中重复走过同一格子，我们使用“临时标记”来占用当前格子，DFS 完再恢复，这就是回溯标记。

## 2. Java 代码（带关键步骤注释）

```java
public class Solution {
    public boolean exist(char[][] board, String word) {
        int m = board.length;
        int n = board[0].length;
        
        // 遍历所有格子作为起点
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (dfs(board, word, i, j, 0)) {
                    return true;  // 从任意起点找到了完整路径
                }
            }
        }
        return false;
    }

    /**
     * 深度优先搜索
     * @param board 网格
     * @param word  目标单词
     * @param i     当前行索引
     * @param j     当前列索引
     * @param index 当前匹配到 word 的第几个字符
     */
    private boolean dfs(char[][] board, String word, int i, int j, int index) {
        // 边界条件：如果 index 已经等于单词长度，说明之前已经全部匹配成功
        if (index == word.length()) {
            return true;
        }
        
        // 超出边界 或 当前字符不匹配 或 已经使用过（标记为 '#')，直接返回 false
        if (i < 0 || i >= board.length || j < 0 || j >= board[0].length 
            || board[i][j] != word.charAt(index)) {
            return false;
        }
        
        // 关键：标记当前格子为已使用，防止重复走
        char temp = board[i][j];
        board[i][j] = '#';  
        
        // 往上下左右四个方向继续匹配下一个字符
        boolean found = dfs(board, word, i+1, j, index+1)    // 下
                     || dfs(board, word, i-1, j, index+1)    // 上
                     || dfs(board, word, i, j+1, index+1)    // 右
                     || dfs(board, word, i, j-1, index+1);   // 左
        
        // 回溯：恢复原始字符
        board[i][j] = temp;
        
        return found;
    }
}
```

## 3. 时间复杂度 + 空间复杂度

- **时间复杂度**：`O(m * n * 4^L)`，其中 m 是行数，n 是列数，L 是单词长度。每个起点最多尝试 4^L 种路径（四个方向不断扩展），不过实际剪枝后会远小于这个上界。
- **空间复杂度**：`O(L)`，递归调用栈的最大深度是单词长度 L（不考虑修改输入数组）。

## 4. 关键点（考察什么知识点）

- **深度优先搜索（DFS）** + **回溯（Backtracking）**：用于在网格中探索所有可能路径。
- **原地标记法**：通过修改 board 来区分“已使用”和“未使用”，避免额外空间。
- **边界与剪枝**：遇到越界、字符不匹配、已经使用过的格子时立即返回，减少无效搜索。
- **方向遍历**：典型的上、下、左、右四个方向递归写法。