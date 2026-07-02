from . import db
from datetime import date, timedelta
def calculate_sm2(reps, ease, interval_days, score):
    """SM-2 算法：输入当前状态和本次分数，返回新状态。score 为 1-5。"""
    if score >= 3:
        if reps == 0:
            interval_days = 1
        elif reps == 1:
            interval_days = 6
        else:
            interval_days = round(interval_days * ease)
        reps += 1
    else:
        reps = 0
        interval_days = 1

    ease = ease + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02))
    ease = max(1.3, round(ease, 2))

    return reps, ease, interval_days

def record_practice(problem_id, score, practiced_at=None):
    practiced_at = practiced_at or str(date.today())

    # 1. 记一条流水；今天已经记过就跳过（ADR-003：只有第一次计分）
    if not db.add_practice_log(problem_id, practiced_at, score):
        return

    # 2. 读出这道题当前的 SM-2 状态（没有就用初始值）
    state = db.get_review_state(problem_id)          # ← 要新加的函数
    reps, ease, interval = (0, 2.5, 0) if state is None else (state[1], state[2], state[3])

    # 3. 算新状态（到这一步才用 calculate_sm2，三个数是“算出来的”）
    reps, ease, interval = calculate_sm2(reps, ease, interval, score)
    next_review = str(date.fromisoformat(practiced_at) + timedelta(days=interval))      # 日期运算你来写

    # 4. 写回：第一次 add，之后 update
    if state is None:
        db.add_review_state(problem_id, reps, ease, interval, practiced_at, next_review)
    else:
        db.update_review_state(reps, ease, interval, practiced_at, next_review, problem_id)

            