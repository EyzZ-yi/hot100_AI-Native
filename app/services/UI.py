import streamlit as st
import agent
import db
import logic

st.set_page_config(page_title="Hot100 AI 练习", layout="centered")
st.title("Hot100 AI 练习助手")

# ─── 侧边栏 ──────────────────────────────────────────────────────
with st.sidebar:
    st.header("训练模式")
    mode = st.radio("训练模式选择", ["复习到期题", "学新题", "自由提问"], label_visibility="collapsed")
    st.divider()

    with st.expander("添加题目"):
        with st.form("add_problem_form", clear_on_submit=True):
            ap_id    = st.number_input("题号 *", min_value=1, step=1)
            ap_title = st.text_input("题目名称 *")
            ap_diff  = st.selectbox("难度", ["", "Easy", "Medium", "Hard"])
            ap_tags  = st.text_input("标签（逗号分隔）")
            ap_src   = st.text_input("代随链接（可选）")
            ap_order = st.number_input("学习顺序（可选）", min_value=0, step=1, value=0)
            submitted = st.form_submit_button("添加", type="primary", use_container_width=True)
            if submitted:
                if not ap_title.strip():
                    st.error("题目名称不能为空")
                else:
                    added = db.add_problem(
                        id=int(ap_id),
                        title=ap_title.strip(),
                        difficulty=ap_diff,
                        tags=ap_tags.strip(),
                        source=ap_src.strip() or None,
                        study_order=int(ap_order) if ap_order else None,
                    )
                    if added:
                        st.success(f"已添加 #{int(ap_id)}")
                    else:
                        st.warning(f"#{int(ap_id)} 已存在，跳过")

    st.divider()
    if st.button("重置当前会话"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


def problem_title(pid):
    p = db.get_promble(pid)
    return p[1] if p else f"题 {pid}"


# ════════════════════════════════════════════════════════════════
# 模式 1：复习到期题
# ════════════════════════════════════════════════════════════════
if mode == "复习到期题":

    DAILY_CAP = 8  # 每天最多复习题数

    # 初始化本次复习会话
    if "rev_due" not in st.session_state:
        already_done_today = db.count_reviews_today()
        remaining = DAILY_CAP - already_done_today
        due = db.get_due_review()
        due = [r for r in due if not db.already_practiced_today(r[0])]
        due = sorted(due, key=lambda r: r[5])[:max(remaining, 0)]
        st.session_state.rev_due = due
        st.session_state.rev_idx = 0
        st.session_state.rev_attempts = 0
        st.session_state.rev_hint = ""
        st.session_state.rev_done = []  # [(pid, score), ...]

    due = st.session_state.rev_due
    idx = st.session_state.rev_idx

    if not due:
        already_done_today = db.count_reviews_today()
        if already_done_today >= DAILY_CAP:
            st.success(f"今天复习已达上限 {DAILY_CAP} 道，明天再来！")
        else:
            st.success("今天没有到期的题，好好休息！")
        st.stop()

    if idx >= len(due):
        st.success(f"今日复习完成！共 {len(st.session_state.rev_done)} 道。")
        if st.session_state.rev_done:
            st.table([{"题号": d[0], "得分": f"{d[1]}/4"} for d in st.session_state.rev_done])
        if st.button("再来一轮"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
        st.stop()

    row = due[idx]
    pid = row[0]
    attempts = st.session_state.rev_attempts

    st.progress(idx / len(due), text=f"进度 {idx}/{len(due)}")
    st.subheader(f"{pid}. {problem_title(pid)}")
    st.caption(f"已尝试 {attempts}/3 次")

    if st.session_state.rev_hint:
        with st.expander("提示", expanded=True):
            st.markdown(st.session_state.rev_hint)

    code = st.text_area("冷启动默写最优解", height=280, key=f"rev_code_{idx}_{attempts}")
    lc = st.radio("LeetCode 提交结果", ["ac", "wa"], horizontal=True, key=f"rev_lc_{idx}_{attempts}")

    col_submit, col_skip = st.columns([3, 1])
    with col_submit:
        submitted = st.button("提交", key=f"rev_sub_{idx}_{attempts}", type="primary", use_container_width=True)
    with col_skip:
        skipped = st.button("跳过", key=f"rev_skip_{idx}", use_container_width=True)

    if skipped:
        st.session_state.rev_idx += 1
        st.session_state.rev_attempts = 0
        st.session_state.rev_hint = ""
        st.rerun()

    if submitted:
        with st.spinner("评分中..."):
            score = agent.grade_attempt(pid, code, lc)

        if score is None:
            st.error("评分失败，自动记 2 分跳过。")
            if attempts == 0:
                logic.record_practice(pid, 2)
            st.session_state.rev_done.append((pid, 2))
            st.session_state.rev_idx += 1
            st.session_state.rev_attempts = 0
            st.session_state.rev_hint = ""
            st.rerun()

        # 只在第一次提交时写入数据库
        if attempts == 0:
            logic.record_practice(pid, score)

        new_state = db.get_review_state(pid)
        next_review = new_state[5] if new_state else "未知"

        if score >= 4 or attempts >= 2:
            st.session_state.rev_done.append((pid, score))
            if score < 4:
                with st.spinner("获取解析..."):
                    sol = agent.reveal_solution(pid)
                st.session_state.rev_hint = sol
            st.session_state.rev_idx += 1
            st.session_state.rev_attempts = 0
            st.session_state.rev_hint = "" if score >= 4 else st.session_state.rev_hint
            if score >= 4:
                st.success(f"得分 {score}/4 | 下次复习 {next_review}")
                st.rerun()
            else:
                st.warning(f"3 次未达标，已给出解析。下次复习 {next_review}")
                with st.expander("解析", expanded=True):
                    st.markdown(sol)
                if st.button("继续下一题"):
                    st.session_state.rev_hint = ""
                    st.rerun()
        else:
            with st.spinner("生成提示中..."):
                hint = agent.get_hint(pid, code, None, "direct")
            st.session_state.rev_hint = hint
            st.session_state.rev_attempts += 1
            st.warning(f"得分 {score}/4，看看提示再试一次。")
            st.rerun()


# ════════════════════════════════════════════════════════════════
# 模式 2：学新题
# ════════════════════════════════════════════════════════════════
elif mode == "学新题":

    if "new_pid" not in st.session_state:
        row = db.get_next_unstarted()
        if row is None:
            st.success("所有题目都已学过！")
            st.stop()
        st.session_state.new_pid = row["id"]
        st.session_state.new_attempts = 0
        st.session_state.new_hint = ""
        st.session_state.new_done = False

    pid = st.session_state.new_pid
    p = db.get_promble(pid)
    title = p[1] if p else f"题 {pid}"
    source = p[4] if p and len(p) > 4 else None
    attempts = st.session_state.new_attempts

    st.subheader(f"首次学习：{pid}. {title}")
    if source and str(source).startswith("http"):
        st.info(f"先去 LeetCode 做 30 分钟。卡住后看代随讲解：[点击跳转]({source})")
    else:
        st.info("先去 LeetCode 做 30 分钟，没有思路别死磕。")

    if st.session_state.new_hint:
        with st.expander("提示", expanded=True):
            st.markdown(st.session_state.new_hint)

    if st.session_state.new_done:
        st.success("本题已完成，已加入复习计划！")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("下一题", type="primary", use_container_width=True):
                del st.session_state["new_pid"]
                for k in ["new_attempts", "new_hint", "new_done"]:
                    st.session_state.pop(k, None)
                st.rerun()
        with col2:
            if st.button("去复习", use_container_width=True):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()
        st.stop()

    lc = st.radio("LeetCode 提交结果", ["ac", "wa", "放弃"], horizontal=True, key=f"new_lc_{attempts}")
    code = st.text_area("贴上你的代码", height=280, key=f"new_code_{attempts}")

    col_sub, col_skip = st.columns([3, 1])
    with col_sub:
        submitted = st.button("提交", key=f"new_sub_{attempts}", type="primary", use_container_width=True)
    with col_skip:
        if st.button("跳过", key=f"new_skip_{attempts}", use_container_width=True):
            st.info("跳过此题，未记录。")
            for k in ["new_pid", "new_attempts", "new_hint", "new_done"]:
                st.session_state.pop(k, None)
            st.rerun()

    if submitted:
        if lc == "放弃":
            for k in ["new_pid", "new_attempts", "new_hint", "new_done"]:
                st.session_state.pop(k, None)
            st.rerun()

        elif lc == "ac":
            with st.spinner("评估复杂度..."):
                score = agent.grade_attempt(pid, code, "ac")
            logic.record_practice(pid, score or 3)
            st.session_state.new_done = True
            st.rerun()

        else:  # wa
            if attempts >= 2:
                with st.spinner("获取解析..."):
                    sol = agent.reveal_solution(pid)
                logic.record_practice(pid, 1)
                st.session_state.new_hint = sol
                st.session_state.new_done = True
                st.rerun()
            else:
                if not code.strip():
                    st.warning("请贴上你的代码再提交。")
                else:
                    with st.spinner("分析代码中..."):
                        hint = agent.get_hint(pid, code, None, "direct")
                    st.session_state.new_hint = hint
                    st.session_state.new_attempts += 1
                    st.rerun()


# ════════════════════════════════════════════════════════════════
# 模式 3：自由提问
# ════════════════════════════════════════════════════════════════
elif mode == "自由提问":
    st.subheader("AI 答疑")

    col1, col2 = st.columns([1, 2])
    with col1:
        pid = st.number_input("题号", min_value=1, step=1, value=1)
    with col2:
        hint_mode = st.radio("提示模式", ["苏格拉底（引导思考）", "直接告诉我"], horizontal=True)

    stuck = st.text_input("你卡在哪？（可留空）")
    code = st.text_area("贴上你的代码", height=260)

    if st.button("获取提示", type="primary"):
        if not code.strip():
            st.warning("请先贴上代码。")
        else:
            mode_key = "socratic" if "苏格拉底" in hint_mode else "direct"
            with st.spinner("思考中..."):
                result = agent.get_hint(int(pid), code, stuck or None, mode_key)
            st.divider()
            st.markdown(result)
