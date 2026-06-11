# RAG v0.1 Evaluation Failures

日期：2026-06-12  
模型：paraphrase-multilingual-MiniLM-L12-v2  
数据：16 条（11 KP + 5 EP + 8 PP）  
distance metric：默认 L2（未指定 cosine）

## Failure Cases

### F-001: 二分查找边界查询召回错误
- Query: "我做二分查找老是边界写错"
- Top-1 召回: EP-003_premature-structure-selection (distance 9.98)
- 期望召回: EP-001_boundary-condition-confusion
- 实际 EP-001 排名: #3
- 假设根因: 
  - (a) Distance metric 用了 L2 不是 cosine
  - (b) EP-003 包含"双指针/二分"等关键词，被字面匹配
  - (c) embedding 模型不理解"边界写错"和"边界条件混淆"的强关联

### F-002: 堆查询完全没召回
- Query: "什么时候用堆"
- Top-1: EP-003 (distance 9.83)
- 期望: KP-009_heap-priority-queue
- KP-009 在 top-3 之外
- 假设根因: KP-009 文档较短，关键词"堆"在其他文档中也出现

### F-003 - F-005: ...（类似结构）

## 失败模式分类（待 v0.2 修复）

| 模式 | 数量 | 修复方向 |
|------|------|----------|
| 长文档霸榜 | 3 | 加 chunking + 按章节切分 |
| Distance metric 错误 | 5 | 改用 cosine |
| Embedding 模型语境弱 | 5 | 换 BGE-zh / Qwen embedding |

## v0.2 改进计划
1. 改 cosine distance（低工作量）除了"什么时候用堆"仍然相关性低，其他问题的相关性提高50%
2. 换 embedding 模型为 BGE-large-zh 或 Qwen3-Embedding（中等工作量）
3. 加 chunking（按 H2 切分）（中等工作量）
4. 评估改进效果（重跑 5 个 query 看新结果）