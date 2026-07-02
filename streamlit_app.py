"""
Hot100 算法练习 — Streamlit 客户端

本地开发（同时启动 FastAPI）:
    uvicorn app.main:app --reload &
    streamlit run streamlit_app.py

连接 Railway 线上:
    API_URL=https://your-app.railway.app streamlit run streamlit_app.py
"""

import os
import streamlit as st
import httpx

API_URL = os.getenv("API_URL", "http://localhost:8000")
_API_KEY = os.getenv("API_KEY", "")


def post(path: str, **kwargs):
    headers = {"x-api-key": _API_KEY} if _API_KEY else {}
    # trust_env=False：不走系统代理（ClashX 等会把 localhost 请求拦截导致 502）
    with httpx.Client(base_url=API_URL, timeout=60, trust_env=False) as client:
        r = client.post(path, headers=headers, **kwargs)
        r.raise_for_status()
        return r.json()


def init_state():
    defaults = {
        "phase": "start",       # "start" | "practice" | "done"
        "session_id": None,
        "problem": None,        # {problem_id, title, source, total}
        "message": None,        # hint / reveal / AC优化提示
        "score": None,
        "pending_next": None,   # None | {problem_id, title, source} | "done"
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


# ── 开始页 ────────────────────────────────────────────────────────────────────

def start_phase():
    st.title("Hot100 算法练习")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("新题")
        st.caption("按 study_order 自动选下一道未学题")
        if st.button("开始新题", use_container_width=True):
            try:
                data = post("/new-sessions")
                _enter_practice(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    st.info("所有题目已完成，没有新题了。")
                else:
                    st.error(e.response.text)
            except Exception as e:
                st.error(f"连接失败：{e}")

    with col2:
        st.subheader("复习")
        st.caption("自动选取今日到期的题")
        if st.button("开始今日复习", use_container_width=True):
            try:
                data = post("/sessions")
                _enter_practice(data)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    st.info("今日没有到期复习题，或已达每日上限（3题）。")
                else:
                    st.error(e.response.text)
            except Exception as e:
                st.error(f"连接失败：{e}")


def _enter_practice(session_data: dict):
    st.session_state.session_id = session_data["session_id"]
    st.session_state.problem = session_data
    st.session_state.message = None
    st.session_state.score = None
    st.session_state.pending_next = None
    st.session_state.phase = "practice"
    st.rerun()


# ── 练习页 ────────────────────────────────────────────────────────────────────

def practice_phase():
    p = st.session_state.problem

    if st.button("← 返回"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    # 题目标题 + 来源链接
    header = f"题 {p['problem_id']}：{p['title']}"
    if p.get("total", 1) > 1:
        header += f"　（今日复习共 {p['total']} 题）"
    st.title(header)
    if p.get("source"):
        st.markdown(f"[📖 参考资料]({p['source']})")

    st.divider()

    # 待确认状态：reveal 或下一题
    if st.session_state.pending_next is not None:
        _show_pending()
        return

    # hint 提示
    if st.session_state.message:
        st.warning(st.session_state.message)
        if st.session_state.score is not None:
            st.caption(f"得分：{st.session_state.score}")

    # 提交区
    code = st.text_area(
        "贴入你的代码",
        height=280,
        placeholder="在 LeetCode 提交后，把代码贴到这里",
    )
    lc_result = st.radio("LeetCode 判题结果", ["wa", "ac"], horizontal=True)

    if st.button("提交", type="primary", disabled=not code.strip()):
        with st.spinner("判分中…"):
            try:
                result = post(
                    f"/sessions/{st.session_state.session_id}/submit",
                    json={"lc_result": lc_result, "code": code},
                )
                _handle_submit(result)
            except httpx.HTTPStatusError as e:
                st.error(f"提交失败：{e.response.text}")


def _show_pending():
    """显示 reveal / next_problem / done 的过渡状态。"""
    msg = st.session_state.message
    score = st.session_state.score
    pending = st.session_state.pending_next

    if msg:
        st.info(msg)
    if score is not None:
        st.caption(f"本题得分：{score}")

    if pending == "done":
        if st.button("✅ 完成今日练习", type="primary"):
            st.session_state.phase = "done"
            st.rerun()
    else:
        label = f"继续 → 题 {pending['problem_id']}：{pending['title']}"
        if st.button(label, type="primary"):
            st.session_state.problem = {
                **st.session_state.problem,
                "problem_id": pending["problem_id"],
                "title": pending["title"],
                "source": pending.get("source"),
            }
            st.session_state.message = None
            st.session_state.score = None
            st.session_state.pending_next = None
            st.rerun()


def _handle_submit(result: dict):
    action = result["next_action"]
    st.session_state.message = result.get("message")
    st.session_state.score = result.get("score")

    if action == "hint":
        st.rerun()
    elif action == "done":
        st.session_state.pending_next = "done"
        st.rerun()
    else:  # "next_problem" | "reveal"
        st.session_state.pending_next = {
            "problem_id": result["next_problem_id"],
            "title": result["next_title"],
            "source": result.get("next_source"),
        }
        st.rerun()


# ── 完成页 ────────────────────────────────────────────────────────────────────

def done_phase():
    st.title("今日完成！")
    st.success("所有题目已完成，明天见。")
    if st.button("返回首页"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# ── 入口 ──────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(page_title="Hot100 练习", layout="centered")
    init_state()

    phase = st.session_state.phase
    if phase == "start":
        start_phase()
    elif phase == "practice":
        practice_phase()
    elif phase == "done":
        done_phase()


if __name__ == "__main__":
    main()
