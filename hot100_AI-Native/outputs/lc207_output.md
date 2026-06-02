# LC207 课程表

好的，我们一起来分析这道经典的图论问题。

---

## 1. 思路

这道题本质上是要判断课程之间的前置依赖关系是否构成了 **有向环**。如果存在环，就说明无法完成所有课程。  
最常用的方法是 **拓扑排序**：每次从图中找入度为 0 的节点（代表没有前置课程需要先修），然后把它“删除”，更新它指向的所有课程的入度，重复这个过程。如果最后所有节点都能被处理，说明图无环；否则有环。  
在代码实现中，我们先用邻接表建图、记录每个节点的入度，然后用队列辅助进行 BFS 式的拓扑排序。

---

## 2. Java 代码

```java
class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        // 1. 构建入度数组和邻接表
        int[] indegree = new int[numCourses];
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) {
            adj.add(new ArrayList<>());
        }

        // 2. 填充入度和邻接表
        for (int[] pair : prerequisites) {
            int course = pair[0];
            int pre = pair[1];
            indegree[course]++;           // 课程 course 的入度 +1
            adj.get(pre).add(course);     // pre -> course
        }

        // 3. 将所有入度为 0 的课程入队
        Queue<Integer> queue = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (indegree[i] == 0) {
                queue.offer(i);
            }
        }

        // 4. BFS 拓扑排序，记录已完成的课程数
        int count = 0;
        while (!queue.isEmpty()) {
            int current = queue.poll();
            count++;
            // 对当前课程的所有后继课程，入度减 1
            for (int next : adj.get(current)) {
                indegree[next]--;
                if (indegree[next] == 0) {
                    queue.offer(next);
                }
            }
        }

        // 5. 如果完成的课程数等于总课程数，说明可以学完
        return count == numCourses;
    }
}
```

---

## 3. 时间复杂度 + 空间复杂度

- **时间复杂度**：O(V + E)  
  V 为课程数（numCourses），E 为先修关系数量（prerequisites 的长度）。建图和遍历每条边各一次。
- **空间复杂度**：O(V + E)  
  需要邻接表存储图，以及入度数组和队列。

---

## 4. 关键点

- **有向图的环检测**：核心考点是判断依赖关系是否成环。
- **拓扑排序**：BFS 实现方式（Kahn 算法），以及如何用“入度”表示前置依赖。
- **图的基本表示**：邻接表的构建，以及如何通过入度数组实现层层剥离。

这道题是“图论 + 拓扑排序”的经典代表，掌握它对解决类似的任务调度、依赖关系问题很有帮助。