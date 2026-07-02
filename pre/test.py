
    # test_grader.py —— 验证评分器会不会给坏代码放水
import agent

# BUGGY_203 = """public ListNode removeElements(ListNode head, int val) {
#     ListNode hypHead=new ListNode();
#     hypHead.next=head;
#     ListNode cur=hypHead;
#     ListNode pre=null;
#     while (cur!=null){
#         if(cur.val==val){ pre.next=cur.next; }   // pre 为 null 时 NPE,逻辑也错
#         else{ pre=cur; }
#         cur=cur.next;
#     }
#     return hypHead.next;
# }"""

# CLEAN_501 = """public ListNode removeElements(ListNode head, int val) {
#     int cur=0,max=Integer.MIN_VALUE;
#     TreeNode pre=null;
#     ArrayList<Integer> res1=new ArrayList<>();
#     public int[] findMode(TreeNode root) {
#         help(root);
#         int[] res=new int[res1.size()];
#         for(int i=0;i<res1.size();i++){
#             res[i]=res1.get(i);
#         }
#         return res;
#     }
#     public void help(TreeNode root){
#         if(root==null) return;
#         help(root.left);
#         cur=1;
#         if(cur>max) {
#             res1.clear();
#             res1.add(root.val);
#         }else if(cur==max) {
#             res1.add(root.val);
#         }
#          if(pre!=null && pre.val==root.val){
#              cur++;
#              if(cur>max) {
#                  res1.clear();
#                  res1.add(root.val);
#              }
#              else if(cur==max) {
#                  res1.add(root.val);
#              }
#          }
#          pre=root;
#         help(root.right);
#     }
# }"""

# # (题号, 期望, 代码, 说明)  期望 pass=该>=3(SM-2 推进), fail=该<3(重置)
# FIXTURES = [
#     (203, "fail", BUGGY_203, "有 bug 跑不对——给>=3 就是放水"),
#     (501, "fail", CLEAN_501, "思路错误"),
#     # TODO: 你再加几个,重点放"看着对、藏着 bug"的
# ]

# RUNS = 3   # LLM 不确定,每个跑几次看稳不稳

# print(f"{'结果':<8}{'题':<5}{'期望':<6}{'分数x3':<14}说明")
# for pid, expect, code, note in FIXTURES:
#     scores = [agent.grade_attempt(pid, code) for _ in range(RUNS)]
#     passed = [(s is not None and s >= 3) for s in scores]
#     want = (expect == "pass")
#     leaked = (expect == "fail") and any(passed)      # 坏代码被判通过
#     mark = "❌放水" if leaked else ("✅" if all(p == want for p in passed) else "⚠️不稳")
#     print(f"{mark:<8}{pid:<5}{expect:<6}{str(scores):<14}{note}")

import db, logic, sqlite3, os
from datetime import date

# ===== 1. 到期体检(只读)=====
# conn = sqlite3.connect(os.path.join(db.BASE_DIR, "practice.db"))
# conn.row_factory = sqlite3.Row
# total = conn.execute("SELECT COUNT(*) FROM review_state").fetchone()[0]
# rows = conn.execute("""SELECT date(next_review_at) due, COUNT(*) n
#                        FROM review_state GROUP BY due ORDER BY due""").fetchall()
# conn.close()
# today = date.today().isoformat()
# due_now = sum(r["n"] for r in rows if r["due"] is None or r["due"] <= today)
# print(f"== 到期体检 == 总{total}题,今天到期 {due_now} ({due_now/total:.0%})")
# for r in rows:
#     flag = " ←今天/过期" if (r["due"] is None or r["due"] <= today) else ""
#     print(f"  {r['due'] or 'NULL'}: {r['n']}{flag}")

# # ===== 2. 状态流转(假题,测完删,不碰真实数据)=====
# PID = 999999
# print("\n== 流转测试 ==")
# db.add_review_state(PID, 2, 2.5, 6, "2025-01-01", "2025-01-01")   # 种一道到期的假题

# logic.record_practice(PID, 4, practiced_at="2025-06-01")          # 通过
# s = db.get_review_state(PID)
# print(f"打4分后: reps={s[1]} interval={s[3]} 下次={s[5]}")
# assert s[3] > 6 and s[5] > "2025-06-01", "通过后间隔没涨/没推后!"

# logic.record_practice(PID, 1, practiced_at="2025-06-02")          # 失败
# s = db.get_review_state(PID)
# print(f"打1分后: reps={s[1]} interval={s[3]} 下次={s[5]}")
# assert s[1] == 0 and s[3] == 1, "失败后没重置!"
# print("✅ 流转正确:通过→间隔变长推后,失败→重置")

# conn = sqlite3.connect(os.path.join(db.BASE_DIR, "practice.db"))   # 清理假题
# conn.execute("DELETE FROM review_state WHERE problem_id=?", (PID,))
# conn.execute("DELETE FROM practice_log WHERE problem_id=?", (PID,))
# conn.commit(); conn.close()
# print("(假题已清理)")


def setup():
    db.init_db()
    db.import_problems_json()      # 读仓库自带的 problem.json
    print("初始化完成,运行 onboarding_fresh() 开始学习。")

setup()
agent.onboarding_fresh()