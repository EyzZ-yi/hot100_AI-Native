# Error Patterns (EP)

存放从 practice_log 提炼的"用户会犯的错"。

## 命名规则
EP-XXX_短描述.md
例：EP-001_boundary-condition-confusion.md

## 入库标准
- 至少在 2+ 道题中出现过同类错误
- 包含：触发场景 / 错误表现 / 根因 / 教学策略 / 关联题目

## 用途
作为 RAG 向量库的核心数据，在 agent 诊断时被检索。

## 来源
data/practice_log.md 中"卡点"和"关键学到的"字段