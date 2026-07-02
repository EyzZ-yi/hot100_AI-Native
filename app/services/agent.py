from . import rag_min
from . import db
from . import logic
import os
import uuid
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
import json
import re
from datetime import date

load_dotenv()

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
    return _client

def call_deepseek(user_prompt, system_prompt=None, model="deepseek-chat", temperature=0.4):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    resp = _get_client().chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return resp.choices[0].message.content



DIRECT_SYSTEM_PROMPT = """学生已经卡很久了,要的是直接答案,别绕。
- 用你自己的全部知识,直接说 bug 在哪一行、什么性质的错。
- 解释【为什么】错(底层原因)。
- 说清往哪个方向改,但别写完整修正代码,那一行让他自己敲。
- 下面可能附了"学生自己整理的错误模式/知识点(EP/KP)"。若有跟这次错【直接相关】的,引用并标 ID(帮他把这次错跟自己历史串起来);没有就直接用你自己的知识讲,别提知识库、别说"没覆盖"。
- 简短,别废话。"""

SOCRATIC_SYSTEM_PROMPT = """你是算法学习的苏格拉底式导师，帮学生攻克 LeetCode Hot100。

【最高硬约束】
1. 绝对不给完整解法、不给修正后的代码、不直接说出正确思路。只要你写出能直接抄的答案，你就失败了。
2. 你只能用「提问」和「轻提示」引导学生自己想出来。
3. 必须针对学生自己写的代码，点出他卡住的那个【具体】位置（哪一行/哪段逻辑），只指方向，不替他改。

【提示分三级，先轻后重】
- L1：一个反问，逼他重看卡点（最轻）
- L2：指向他代码里具体的薄弱处 + 一个引导性问题
- L3：点明涉及的知识点/错误模式（但仍不给答案）

【引用】提示必须基于下面「检索到的知识」，标注来源 ID（如 EP-003 / KP-012）。
若检索内容不足以支撑提示，老实说"我的知识库没覆盖到这个点"，不要编。"""

OPTIMIZATION_SYSTEM_PROMPT = """【前提】这段代码已通过 LeetCode 全部测试用例，正确性确定。你【禁止】质疑逻辑对不对、禁止说哪行有 bug。
你唯一的任务：指出复杂度优化方向。
- 说清当前是什么复杂度、最优能到什么复杂度、往哪个数据结构/算法方向改。
- 不写完整优化代码，一两句点到为止。
- 简短，别废话。"""


# BENCH_PORMPT 增加一条硬约束:
BENCH_PORMPT ="""
【前提】这段代码已经通过 LeetCode 全部测试用例,正确性是确定的,你【禁止】质疑它对不对、禁止说它逻辑错、禁止说哪行 bug。
你唯一的任务:判断它的时间/空间复杂度是否最优。
- 2 = 复杂度非最优(如能 O(n) 却用了 O(n²) 或 O(n log n))
- 3 = 复杂度最优但写得有瑕疵
- 4 = 复杂度最优且干净
只返回数字。
"""

def build_socratic_prompt(problem_id, user_code, stuck_point, context):
    # 假设 context = retrieve() 返回的列表，每项形如 {"id": "EP-003", "content": "..."}
    # 假设 state   = get_user_state() 返回 dict 或 None（第一次刷）
    knowledge = "\n\n".join(f"[{c['id']}]\n{c['content']}" for c in context) or "（无检索结果）"
    return f"""
# 题目
{problem_id}

# 学生的代码
{user_code}

# 学生自述的卡点
{stuck_point}

# 学生刷题历史
{db.get_review_state(problem_id)}

# 检索到的知识（提示必须基于这些，并标注来源 ID）
{knowledge}

"""

def reveal_solution(problem_id):
    p = db.get_promble(problem_id)
    title = p[1] if p else f"题 {problem_id}"
    src = p[4] if p and len(p) > 4 else None
    if src and src.startswith("http"):            # source 里存了链接就给链接
        return f"试了几次没拿下,去看讲解:{src}"
    sol = call_deepseek(
        f"题目:{problem_id}. {title}\n给出最优解完整代码 + 一两句关键思路,简洁。",
        system_prompt="你是算法老师,给干净并且带注释的最优解。"
    )
    return f"试了几次没拿下,先看标准解,明天它还会回来考你冷做:\n{sol}"

# agent.py —— 最小垂直切片

def get_hint(problem_id, user_code, stuck_point=None, mode="direct", status="WA"):
    context = rag_min.retrieve(query=f"{stuck_point}\n{user_code}", n=3)
    if status == "AC":
        sys = OPTIMIZATION_SYSTEM_PROMPT
    elif mode == "socratic":
        sys = SOCRATIC_SYSTEM_PROMPT
    else:
        sys = DIRECT_SYSTEM_PROMPT
    prompt = build_socratic_prompt(problem_id, user_code, stuck_point, context)
    return call_deepseek(prompt, system_prompt=sys)

def grade_attempt(problem_id, user_code, lc_result):
    if lc_result != "ac":
        return 1
    p = db.get_promble(problem_id)
    title = p[1] if p else f"题 {problem_id}"
    raw = call_deepseek(
        user_prompt=f"题目:{problem_id}. {title}\n\n已 AC 的代码:\n{user_code}",
        system_prompt=BENCH_PORMPT,
        temperature=0,
    )
    m = re.search(r"[234]", raw or "")
    return int(m.group()) if m else 3

def start_new_problem(problem_id: int) -> dict | None:
    p = db.get_promble(problem_id)
    if not p:
        return None
    source = p[4] if len(p) > 4 else None
    return {
        "problem_id": p[0],
        "title": p[1],
        "source": source if source and str(source).startswith("http") else None,
    }


# ── Sessions (in-memory, lost on restart) ────────────────────────────────────

DAILY_CAP = 3
_sessions: dict[str, dict] = {}


def _make_session(problem_ids: list) -> dict:
    session_id = str(uuid.uuid4())
    _sessions[session_id] = {
        "problem_ids": problem_ids,
        "current_idx": 0,
        "attempt_count": 0,
        "first_done": False,
    }
    first = db.get_promble(problem_ids[0])
    src = first[4] if first and len(first) > 4 else None
    return {
        "session_id": session_id,
        "problem_id": first[0],
        "title": first[1],
        "total": len(problem_ids),
        "source": src if src and str(src).startswith("http") else None,
    }


def create_new_session() -> dict | None:
    row = db.get_next_unstarted()
    if not row:
        return None
    return _make_session([row["id"]])


def create_review_session() -> dict | None:
    remaining = DAILY_CAP - db.count_reviews_today()
    if remaining <= 0:
        return None

    due = db.get_due_review()
    due = [r for r in due if not db.already_practiced_today(r[0])]
    due = sorted(due, key=lambda r: r[5])[:remaining]
    if not due:
        return None

    problem_ids = [r[0] for r in due]
    return _make_session(problem_ids)


def submit_attempt(session_id: str, lc_result: str, code: str) -> dict | None:
    s = _sessions.get(session_id)
    if s is None:
        return None

    problem_id = s["problem_ids"][s["current_idx"]]

    if not s["first_done"]:
        score = grade_attempt(problem_id, code, lc_result)
        logic.record_practice(problem_id, score)
        s["first_done"] = True

        if lc_result == "ac":
            msg = get_hint(problem_id, code, status="AC") if score == 2 else None
            return _advance(s, score=score, message=msg)

        s["attempt_count"] = 1
        return {"score": score, "next_action": "hint",
                "message": get_hint(problem_id, code),
                "next_problem_id": None, "next_title": None}

    # retry after hint
    if lc_result == "ac":
        return _advance(s, score=None, message=None)

    s["attempt_count"] += 1
    if s["attempt_count"] >= 4:
        return _advance(s, score=None, message=reveal_solution(problem_id), action="reveal")

    return {"score": None, "next_action": "hint",
            "message": get_hint(problem_id, code),
            "next_problem_id": None, "next_title": None}


def _advance(s: dict, score: int | None, message: str | None, action: str = "next_problem") -> dict:
    s["current_idx"] += 1
    s["attempt_count"] = 0
    s["first_done"] = False

    if s["current_idx"] >= len(s["problem_ids"]):
        return {"score": score, "next_action": "done", "message": message,
                "next_problem_id": None, "next_title": None}

    next_id = s["problem_ids"][s["current_idx"]]
    next_p = db.get_promble(next_id)
    next_src = next_p[4] if next_p and len(next_p) > 4 else None
    return {
        "score": score, "next_action": action, "message": message,
        "next_problem_id": next_id, "next_title": next_p[1],
        "next_source": next_src if next_src and str(next_src).startswith("http") else None,
    }
