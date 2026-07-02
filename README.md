# Hot100 AI-Native 刷题助手

LeetCode Hot100 的 AI 伴读工具。核心问题：刷题"好像懂了"，一周后默写全忘。

用 SM-2 间隔复习调度、RAG 检索个人错误模式库、DeepSeek 苏格拉底式提示——不给完整答案，逼你自己想出来。

---

## 架构

```
Streamlit 客户端  →  FastAPI 后端  →  SQLite / ChromaDB
```

```
hot100_AI-Native/
├── app/
│   ├── main.py              # FastAPI 入口 + API Key 鉴权
│   ├── schemas.py           # Pydantic 入参/出参
│   ├── routers/practice.py  # 路由层
│   └── services/
│       ├── agent.py         # AI 逻辑：提示生成、评分、Session 状态机
│       ├── db.py            # SQLite（practice_log / review_state / problems）
│       ├── logic.py         # SM-2 算法
│       └── rag_min.py       # RAG：ChromaDB + 阿里云 text-embedding-v3
├── streamlit_app.py         # Streamlit 客户端
├── eval/run_eval.py         # grade_attempt 判分准确率评测（6 个 ground truth）
├── data/
│   ├── error_patterns/      # EP-XXX 错误模式
│   ├── knowledge_points/    # KP-XXX 算法概念
│   └── pedagogical_principles/ # PP-XXX 学习方法论
├── chroma_db/               # 向量库持久化
└── railway.toml             # Railway 部署配置
```

---

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/new-sessions` | 按 study_order 推下一道新题，创建 Session |
| POST | `/sessions` | 今日 SM-2 到期复习（上限 3 题） |
| POST | `/sessions/{id}/submit` | 提交 AC/WA + 代码，返回评分/提示/下一题 |
| POST | `/hints` | 获取提示（WA→Socratic/直接，AC→复杂度优化） |
| POST | `/attempts/grade` | 单独调用复杂度评分（返回 1-4） |
| POST | `/problems/new` | 按 ID 查题目信息 |

Session 状态机由客户端驱动，服务端只存 `(session_id, problem_ids, attempt_count)`。

---

## 本地启动

```bash
cd hot100_AI-Native
source venv/bin/activate

# 终端 1：FastAPI
uvicorn app.main:app --reload

# 终端 2：Streamlit
streamlit run streamlit_app.py
```

`.env`：

```
DEEPSEEK_API_KEY=sk-...
DASHSCOPE_API_KEY=sk-...
# API_KEY=  # 不设则无鉴权，本地开发用
```

---

## Railway 部署

`railway.toml` 已配置好启动命令。还需在 Railway dashboard 完成：

1. 新建 Volume，挂载到 `/data`
2. 设置环境变量：

```
DEEPSEEK_API_KEY=...
DASHSCOPE_API_KEY=...
API_KEY=<随机字符串，保护接口>
DB_PATH=/data/practice.db
CHROMA_PATH=/data/chroma_db
```

Streamlit 客户端本地连线上：

```bash
API_URL=https://your-app.railway.app API_KEY=<同上> streamlit run streamlit_app.py
```

---

## 评测

```bash
# 判分准确率（需要 DEEPSEEK_API_KEY）
python eval/run_eval.py
```

6 个 ground truth 用例，覆盖：WA→1（确定性），O(n²)→2（FP 警戒），O(n) 最优→4（FN 警戒）。

已知 FP：O(n log n) 排序解被误判为 4，待添加 `target_complexity` 字段后修复。

---

## ADR（已锁定的架构决策）

- **ADR-001** 首次新题用代码随想录链接，LLM 只在复习阶段介入
- **ADR-002** AI 是诊断者，Socratic 模式不给完整答案
- **ADR-003** SM-2 failure-reset，只有第一次冷启动计分
- **ADR-004** LeetCode AC/WA 是正确性唯一 ground truth，LLM 只判复杂度

---

## 版本进度

| 版本 | 状态 | 内容 |
|------|------|------|
| v0.1 | 完成 | 原型，6 题 demo |
| v0.2 | 完成 | SQLite + SM-2 + RAG + Streamlit UI |
| v0.3 | 完成 | FastAPI 迁移 + Railway 部署 + 判分 eval |
| v1.0 | 计划中 | 三层 Agent 架构 + Guardrails + 来源标注 |
