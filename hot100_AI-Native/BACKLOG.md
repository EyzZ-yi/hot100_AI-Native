## 面试官评审标准（参考）

来源：业内面试官的评审反馈

### 维度 1：Evaluation 能力（最重要）
- 测试集选择 / 设计
- TP / FP / TN / FN 在具体场景下的定义
- 多轮采样评测
- 失败模式分类（幻觉 vs 检索 vs prompt）

### 维度 2：工程自动化
- CI/CD 经验
- 测试覆盖
- 测试环境管理

### 维度 3：项目管理能力
- 任务拆解
- 进度追踪
- 决策记录

### 应用到本项目
所有功能必须配套：
1. 至少 5 个 ground truth 测试用例
2. 自动化评测脚本可跑
3. ADR 记录关键决策

## v0.2 核心功能（暑期主战场）

### Feature 1：代码诊断 Agent（核心差异化）
- 输入：题目 ID + 用户代码
- 输出：错误诊断 + Socratic 提示（细节错直接说，概念错引导）
- Prompt 关键：negative constraint（禁止给完整答案）

### Feature 2：用户状态追踪
- SQLite 存储：题目 + 状态 + 自评 + 复习历史
- 用于推荐和复习调度

### Feature 3：复习调度
- 艾宾浩斯简化版
- 自评 1-2 → 1 天后复习
- 自评 3 → 3 天
- 自评 4 → 7 天
- 自评 5 → 14 天

### Feature 4（待数据驱动）：题目推荐
- 基于用户已掌握 + 题目知识点图谱
- 推迟到 v0.3

## 数据架构更新：增加 "教学原则库"（2026-06-04）

### 新数据类型：PP（Pedagogical Principles）
- 内容：如何学/写代码的元方法论
- 区别于 EP（错误模式）和 KP（概念知识）
- 在 agent 诊断后，作为"治疗建议"调用

### 第一条 PP（待写入）
PP-001: 先正确，后优化（来源：2026-06-04 dogfooding）

### 待暑期建库时统一处理
- 提炼自刷题日志的"关键学到的"字段
- 估计 v1 总量：10-20 条

## RAG v0.2 改进计划（2026-06-12 规划）

### v0.2.A（明天 6/13，半天）
- 改 distance metric 为 cosine
- 换 embedding 模型为 BGE-large-zh 或 Qwen3-Embedding
- 跑同样 5 个 query 对比
- 产出：eval/v02a_results.md

### v0.2.B（6/14 - 6/15，视 A 效果而定）
- 如果 A 效果好（召回准确率 > 60%）→ 暂不做 chunking，转去做 KP 内容修订
- 如果 A 效果差（< 60%）→ 做 chunking（按 ## H2 切分）

### v0.2.C（暑期再做）
- Hybrid search（BM25 + 向量）
- Rerank（接 bge-reranker）

### 注意
**不要同时改多个变量**。一次只动一个，留对照基线。

## GustoBot 启发的 v0.3 + v1.0 路线（2026-06-XX）

### 来源
读了 GustoBot README（github.com/skygazer42/GustoBot），是一个三层 multi-agent 智能客服系统。

### 借鉴的设计思想（不抄技术栈，只学方法论）

#### 1. 三层架构（L1 路由 / L2 子图 / L3 工具）
- 当前我的项目：单层 RAG
- v0.3 目标：拆出 L1 + L2 + L3
- L1：意图分类（诊断/题解/复习/推荐）
- L2：每种意图对应的子流程
- L3：原子工具（retrieve_ep / retrieve_kp / get_user_state / call_llm）

#### 2. PostgreSQL 优先兜底 → 改为"SQLite 优先 → RAG 兜底"
- 用户状态查询走 SQLite（确定性）
- 知识检索走 RAG（不确定性）
- 显式区分两者，不让 LLM 编

#### 3. Guardrails 边界控制
- 拒绝超出 hot100 / 代随 / 算法学习的查询
- 显式告知用户边界，建议他们用 Claude / GPT

#### 4. 来源标注
- 每个回答标明引用的 EP-XXX / KP-XXX / PP-XXX
- 提升可追溯性 + 调试方便

### 不学的部分（这些是 GustoBot 的过度工程，不适合我的体量）
- Neo4j 图谱（hot100 关系手工 JSON 标即可）
- Microsoft GraphRAG（数据量不够）
- Map-Reduce 并行（单一查询不需要）
- Reranker 双阈值（v0.2 命中率已经 100%）
- 多模态（不在我的产品范围）

### 实施时间表
- v0.3（暑期前半 7/15-8/4）：三层架构 + Guardrails + 来源标注
- v1.0（暑期后半 8/5-8/25）：兜底策略 + SQLite 用户状态