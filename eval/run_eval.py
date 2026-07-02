"""
grade_attempt 判分准确率评测脚本

运行方式（在 hot100_AI-Native/ 目录下）:
    python eval/run_eval.py

依赖:
    - .env 里有 DEEPSEEK_API_KEY（WA 用例不调 LLM，AC 用例会调）
    - 不要求 DB 里有这些题目；题目不存在时 title 退化为 "题 {id}"，不影响 LLM 判分

判分逻辑（来自 agent.grade_attempt）:
    lc_result="wa"  → 直接返回 1，不调 LLM（确定性）
    lc_result="ac"  → 调 DeepSeek，返回 2/3/4：
        2 = 复杂度非最优（能 O(n) 却用了 O(n²) 或 O(n log n)）
        3 = 复杂度最优但代码有瑕疵
        4 = 复杂度最优且干净

FP 警戒线: O(n²) 被打成 3 或 4（把垃圾代码放过去）
FN 警戒线: O(n) 最优解被打成 2（给正确代码扣分）
score=3 不在自动测试内——"有瑕疵"主观性高，LLM 在 temp=0 下也不稳定。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services import agent

TEST_CASES = [
    # ── WA 用例：必须是 1，不调 LLM，完全确定性 ─────────────────────────
    {
        "id": "WA_01",
        "desc": "WA → score=1（空返回，显然错）",
        "problem_id": 1,
        "code": "class Solution:\n    def twoSum(self, nums, target):\n        return []",
        "lc_result": "wa",
        "expected": 1,
    },
    {
        "id": "WA_02",
        "desc": "WA → score=1（即使代码逻辑正确，LeetCode 判 WA）",
        "problem_id": 1,
        "code": (
            "class Solution:\n"
            "    def twoSum(self, nums, target):\n"
            "        seen = {}\n"
            "        for i, n in enumerate(nums):\n"
            "            if target - n in seen:\n"
            "                return [seen[target - n], i]\n"
            "            seen[n] = i"
        ),
        "lc_result": "wa",
        "expected": 1,
    },
    # ── AC score=2：复杂度非最优 ──────────────────────────────────────────
    {
        "id": "AC_01",
        "desc": "Two Sum O(n²) 暴力 → 2（能 O(n) 却用了双重循环）",
        "problem_id": 1,
        "code": (
            "class Solution:\n"
            "    def twoSum(self, nums, target):\n"
            "        for i in range(len(nums)):\n"
            "            for j in range(i + 1, len(nums)):\n"
            "                if nums[i] + nums[j] == target:\n"
            "                    return [i, j]"
        ),
        "lc_result": "ac",
        "expected": 2,
    },
    {
        "id": "AC_02",
        "desc": "Contains Duplicate 排序法 O(n log n) → 2（最优是 O(n) hashset）",
        "problem_id": 217,
        "code": (
            "class Solution:\n"
            "    def containsDuplicate(self, nums):\n"
            "        nums.sort()\n"
            "        for i in range(1, len(nums)):\n"
            "            if nums[i] == nums[i - 1]:\n"
            "                return True\n"
            "        return False"
        ),
        "lc_result": "ac",
        "expected": 2,
    },
    # ── AC score=4：最优复杂度且干净 ─────────────────────────────────────
    {
        "id": "AC_03",
        "desc": "Two Sum O(n) hashmap 干净 → 4",
        "problem_id": 1,
        "code": (
            "class Solution:\n"
            "    def twoSum(self, nums, target):\n"
            "        seen = {}\n"
            "        for i, n in enumerate(nums):\n"
            "            if target - n in seen:\n"
            "                return [seen[target - n], i]\n"
            "            seen[n] = i"
        ),
        "lc_result": "ac",
        "expected": 4,
    },
    {
        "id": "AC_04",
        "desc": "Valid Parentheses O(n) stack 干净 → 4",
        "problem_id": 20,
        "code": (
            "class Solution:\n"
            "    def isValid(self, s):\n"
            "        stack = []\n"
            "        mapping = {')': '(', '}': '{', ']': '['}\n"
            "        for c in s:\n"
            "            if c in mapping:\n"
            "                if not stack or stack[-1] != mapping[c]:\n"
            "                    return False\n"
            "                stack.pop()\n"
            "            else:\n"
            "                stack.append(c)\n"
            "        return not stack"
        ),
        "lc_result": "ac",
        "expected": 4,
    },
    {
        "id": "AC_05",
        "desc": "Contains Duplicate O(n) set 单行 → 4",
        "problem_id": 217,
        "code": (
            "class Solution:\n"
            "    def containsDuplicate(self, nums):\n"
            "        return len(nums) != len(set(nums))"
        ),
        "lc_result": "ac",
        "expected": 4,
    },
]


def run() -> bool:
    passed = 0
    failed = 0
    failures = []

    print(f"\n{'=' * 60}")
    print(f"grade_attempt 判分评测 — {len(TEST_CASES)} 个用例")
    print(f"{'=' * 60}\n")

    for tc in TEST_CASES:
        actual = agent.grade_attempt(tc["problem_id"], tc["code"], tc["lc_result"])
        ok = actual == tc["expected"]
        if ok:
            passed += 1
        else:
            failed += 1
            failures.append((tc["id"], tc["expected"], actual, tc["desc"]))

        marker = "✓" if ok else "✗"
        print(f"  [{marker}] {tc['id']:8s}  expected={tc['expected']}  actual={actual}  {tc['desc']}")

    print(f"\n{'=' * 60}")
    print(f"结果: {passed}/{len(TEST_CASES)} 通过\n")

    if failures:
        print("失败分析：")
        for fid, exp, act, desc in failures:
            if fid.startswith("WA"):
                print(f"  {fid}: grade_attempt 逻辑 bug — WA 必须返回 1，不依赖 LLM")
            elif exp == 2 and act > 2:
                print(f"  {fid}: FP — 次优复杂度被误判为最优（{act}）。检查 BENCH_PROMPT 或 LLM 模型")
            elif exp == 4 and act < 4:
                print(f"  {fid}: FN — 最优解被误判为次优（{act}）。可能需要调整 BENCH_PROMPT")
            else:
                print(f"  {fid}: expected={exp}  actual={act}  — {desc}")
        print()

    return failed == 0


if __name__ == "__main__":
    success = run()
    sys.exit(0 if success else 1)
