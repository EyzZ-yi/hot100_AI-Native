import sqlite3
import re
import os
from . import logic
from datetime import date, datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.getenv("DB_PATH", os.path.join(BASE_DIR, "practice.db"))

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY,
            title TEXT,
            difficulty TEXT,
            tags TEXT,
            source TEXT,
            study_order INTEGER
        );
        CREATE TABLE IF NOT EXISTS practice_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id INTEGER,
            practiced_at TEXT,
            self_score INTEGER,
            UNIQUE(problem_id, practiced_at)
        );
        CREATE TABLE IF NOT EXISTS review_state (
            problem_id INTEGER PRIMARY KEY,
            reps INTEGER,
            ease REAL,
            interval_days INTEGER,
            last_practiced TEXT,
            next_review_at TEXT
        );
    """)
    # 旧库迁移：补上后来新增的列
    existing_cols = {row[1] for row in cur.execute("PRAGMA table_info(problems)")}
    if "study_order" not in existing_cols:
        cur.execute("ALTER TABLE problems ADD COLUMN study_order INTEGER")
    conn.commit()
    conn.close()


# def add_promble(id, title, difficulty, tags, source, study_order=None):
#     conn = sqlite3.connect(DB_PATH)
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT OR IGNORE INTO problems (id, title, difficulty, tags, source, study_order) VALUES (?,?,?,?,?,?)",
#         (id, title, difficulty, tags, source, study_order)
#     )
#     conn.commit(); conn.close()

def add_problem(id, title, difficulty="", tags="", source=None, study_order=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO problems (id, title, difficulty, tags, source, study_order) "
        "VALUES (?,?,?,?,?,?)",
        (id, title, difficulty, tags, source, study_order)
    )
    conn.commit()
    added = cur.rowcount
    conn.close()
    print(f"题 {id}. {title} {'已添加' if added else '已存在,跳过'}")
    return bool(added)

def get_promble(id) :
    conn=sqlite3.connect(DB_PATH)
    cur=conn.cursor()
    cur.execute("SELECT * FROM problems WHERE id = ?",(id,))
    row=cur.fetchone()
    conn.close()
    return row
 


def add_practice_log(problem_id, practiced_at, self_score) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO practice_log (problem_id, practiced_at, self_score) VALUES (?, ?, ?)",
        (problem_id, practiced_at, self_score),
    )
    conn.commit()
    inserted = bool(cur.rowcount)
    conn.close()
    return inserted



def get_practice_log_date(practiced_at) :
    conn=sqlite3.connect(DB_PATH)
    cur=conn.cursor()
    cur.execute("SELECT * FROM practice_log WHERE practiced_at = ?",(practiced_at,))
    row=cur.fetchall()
    conn.close()
    return row

def get_practice_log_promble_id(problem_id) :
    conn=sqlite3.connect(DB_PATH)
    cur=conn.cursor()
    cur.execute("SELECT * FROM practice_log WHERE problem_id = ?",(problem_id,))
    row=cur.fetchall()
    conn.close()
    return row


def add_review_state(problem_id, reps, ease, interval_days, last_practiced, next_review_at) :
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO  review_state  (problem_id, reps, ease, interval_days, last_practiced, next_review_at) VALUES(?, ?, ?, ?, ?, ?)",
        (problem_id, reps, ease, interval_days, last_practiced, next_review_at),
    )
    conn.commit()
    conn.close()

def update_review_state(reps, ease, interval_days, last_practiced, next_review_at, problem_id) :
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "UPDATE  review_state SET reps= ?, ease= ?, interval_days= ?, last_practiced= ?, next_review_at= ? WHERE problem_id= ?",
        (reps, ease, interval_days, last_practiced, next_review_at, problem_id),
    )
    conn.commit()
    conn.close()

def get_due_review() :
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM review_state WHERE next_review_at<= date('now')")
    row=cur.fetchall()
    conn.close()
    return row

def get_review_state(problem_id) :
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM review_state WHERE problem_id= ?",(problem_id,))
    row=cur.fetchone()
    conn.close()
    return row

#帮你自动找出下一道该学的新题目
def get_next_unstarted():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute("""
        SELECT p.id, p.title FROM problems p
        LEFT JOIN review_state r ON p.id = r.problem_id
        WHERE r.problem_id IS NULL AND p.study_order IS NOT NULL
        ORDER BY p.study_order LIMIT 1
    """).fetchone()
    conn.close()
    return row

def count_reviews_today():
    """今天已完成的【复习】数(= 今天练的题里,今天之前就练过的)。首次不计入。"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    today = str(date.today())
    cur.execute("""
        SELECT COUNT(DISTINCT pl.problem_id) FROM practice_log pl
        WHERE pl.practiced_at = ?
        AND EXISTS (SELECT 1 FROM practice_log p2
                    WHERE p2.problem_id = pl.problem_id AND p2.practiced_at < ?)
    """, (today, today))
    n = cur.fetchone()[0]
    conn.close()
    return n

def already_practiced_today(problem_id):
    """这道题今天是否已经练过(查 practice_log)。"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM practice_log WHERE problem_id = ? AND practiced_at = ?",
        (problem_id, str(date.today()))
    )
    hit = cur.fetchone()
    conn.close()
    return hit is not None

def parse_and_import_md():
    with open(os.path.join(BASE_DIR, "data/practice_log.md"), "r", encoding="utf-8") as f:
        md_text = f.read()

    # 按题目分块，每块以 "## LC 数字" 开头
    sections = re.split(r'(?=##\s+LC\s+\d+)', md_text)
    table_line_pattern = re.compile(
        r'\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(\d)(?:/5)?\s*\|'
    )

    total = 0
    for section in sections:
        title_match = re.search(r'##\s+LC\s+(\d+)', section)
        if not title_match:
            continue
        problem_id = int(title_match.group(1))

        for line in section.split('\n'):
            match = table_line_pattern.search(line)
            if match:
                practiced_at = match.group(1)
                self_score = int(match.group(2))
                try:
                    add_practice_log(problem_id, practiced_at, self_score)
                    print(f"成功导入: 题目 {problem_id} | 日期 {practiced_at} | 分数 {self_score}")
                    total += 1
                except sqlite3.Error as e:
                    print(f"导入失败 (题目 {problem_id} | {practiced_at}): {e}")

    print(f"--- 导入完成，共成功导入 {total} 条记录 ---")

def init_review_state_from_log():
    """遍历每道题的练习历史，用 SM-2 算出当前复习状态，写入 review_state。"""
    from datetime import date, timedelta

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT problem_id FROM practice_log")
    problem_ids = [row[0] for row in cur.fetchall()]

    for problem_id in problem_ids:
        cur.execute(
            "SELECT practiced_at, self_score FROM practice_log WHERE problem_id = ? ORDER BY practiced_at ASC",
            (problem_id,)
        )
        records = cur.fetchall()

        reps, ease, interval_days = 0, 2.5, 1
        last_practiced = None
        for practiced_at, self_score in records:
            reps, ease, interval_days = logic.calculate_sm2(reps, ease, interval_days, self_score)
            last_practiced = practiced_at

        next_review_at = str(date.fromisoformat(last_practiced) + timedelta(days=interval_days))

        cur.execute("SELECT 1 FROM review_state WHERE problem_id = ?", (problem_id,))
        if cur.fetchone():
            cur.execute(
                "UPDATE review_state SET reps=?, ease=?, interval_days=?, last_practiced=?, next_review_at=? WHERE problem_id=?",
                (reps, ease, interval_days, last_practiced, next_review_at, problem_id)
            )
        else:
            cur.execute(
                "INSERT INTO review_state (problem_id, reps, ease, interval_days, last_practiced, next_review_at) VALUES (?,?,?,?,?,?)",
                (problem_id, reps, ease, interval_days, last_practiced, next_review_at)
            )
        print(f"题目 {problem_id} | reps={reps} ease={ease} interval={interval_days}天 | 下次复习: {next_review_at}")

    conn.commit()
    conn.close()

def import_problems_json():
    import json
    with open(os.path.join(BASE_DIR, "data/problem.json"), "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    count = 0
    for problem_id, info in data.items():
        tags = ",".join(info.get("tags", []))
        study_order = info.get("study_order")
        cur.execute(
            "INSERT OR IGNORE INTO problems (id, title, difficulty, tags, study_order) VALUES (?, ?, ?, ?, ?)",
            (int(problem_id), info["title"], info.get("difficulty", ""), tags, study_order)
        )
        if cur.rowcount:
            count += 1
    conn.commit()
    conn.close()
    print(f"--- 题目导入完成，共导入 {count} 条 ---")

if __name__ == "__main__":
    init_db()
    parse_and_import_md()
    init_review_state_from_log()
    import_problems_json()

    
