# CLAUDE.md — Hot100 Agent

## 项目是什么

RAG-based 算法学习助手，强制 **recall（独立复现）而非 recognition（看懂）**。
核心命题：能看懂解法 ≠ 能独立写出来。工具通过冷启动复现 + 间隔重复(SM-2) + 客观判分 + 分级资源策略来逼真实回忆。

**这是核心价值的命门**：一个会把正确代码诊断成有 bug 的工具，比没有还糟。任何改动若可能影响判分/诊断的准确性，必须谨慎对待。

## 技术栈

- **LLM**: DeepSeek API
- **Embedding**: Qwen text-embedding-v3 (via DashScope)
- **Vector store**: ChromaDB（cosine distance，不是 L2）
- **结构化存储**: SQLite
- **UI**: Streamlit（现有）；**正在新增 FastAPI 后端层**
- **语言**: Python

## 架构分层（不许打破）

```
router (FastAPI)  →  service (agent 逻辑)  →  repo (SQLite / ChromaDB)
```

- **FastAPI 只做 I/O 边界**：校验入参 → 调 service 函数 → 返回 JSON。不复制任何 agent 逻辑。
- **service 层必须无 UI 副作用**：不许有 `st.*` / `print` 作为输出手段。函数 = 输入 → return 值。判断标准：单独 import、不启动 Streamlit，能跑通。
- **LLM 通过 tool_use 决策，应用代码执行**。LLM 永远不直接生成或运行 SQL。

## 锁定的架构决策（ADR）

- **ADR-001 分级资源**：首次遇到的题用「代码随想录」；LLM 只在 review 阶段介入。
- **ADR-002 AI 是诊断者不是老师**：Socratic 模式不给完整答案。
- **ADR-003 SM-2 failure-reset**：只有第一次冷启动尝试计分，没有 while-until-AC。
- **ADR-004 判分边界**：**LeetCode AC/WA 是 correctness 的唯一 ground truth；LLM 只判复杂度**，不判对错。已被 dogfooding 的假阴性/假阳性反复验证。

**已拒绝（不要再提议）**：三层多 agent 架构；持久化可推导状态；个性化对话式 RAG 知识库（污染共享课程库会降低检索质量，个性化应走 SQL 聚合）。

## 已知陷阱（改代码前必看）

- **`get_hint` 只能对 WA 调用，AC 代码绝不给 hint**。AC 还诊断 = 制造假 bug，违背核心价值。路由层就要拦死。
- **`grade_attempt` 必须传入 problem_title**，否则 LLM 不知道题目、瞎猜最优复杂度。
- **SQLite 无原生 DATE 类型**，Python 3.12 弃用了默认 date adapter——在类型边界显式 `str()` 转换。

## 当前工作：FastAPI 迁移

目标结构：
```
app/
  main.py        # FastAPI 实例 + 路由注册
  schemas.py     # Pydantic 入参/出参 model
  routers/       # endpoint：校验 → 调 service → 返回
  services/      # 现有 agent 函数，剥离 UI 副作用后搬入
```

- LLM/embedding 调用是 I/O 密集 → endpoint 用 `async def`，换 httpx 异步客户端。
- `run_review_session` 的交互循环（WA → 升级 hint → retry≤4 → reveal）要拆成**无状态**步骤，服务端只存 `(session_id, problem_id, attempt_count)`，客户端拿 session_id 驱动。
- **done 的定义 = 线上能访问的 URL**（Railway/Render），不是本地能跑。

## 我的背景与学习模式

- **已学**：CS61B、计算机网络。**未学**：OS、任何前后端框架。
- 解释时不要假设 OS 或框架知识。FastAPI / Pydantic / async / ASGI 等概念**第一次出现时**用一两句讲清「是什么、为什么需要」，之后默认我已懂。
- 这是**边做边学**：在实现步骤里顺带解释「为什么这样设计」，但不要为了教学而暂停交付——本周优先级是 ship 上线，不是上完一门 FastAPI 课。

## 协作约定

- **直接、基于证据地 challenge，不要 validation**。质疑动机优于附和。
- **盯住范围**：当我在一个任务没收尾时就转向更大的脚手架/架构/学习新东西，直接点出来——这是回避，不是规划。
- 完成的标准以预先约定的 done criteria 为准，"声称完成"不等于完成。
- 偏好更短、更低成本的方案；接受显式的 trade-off。