PRAGMA foreign_keys = ON;

CREATE TABLE problems (
    id          INTEGER PRIMARY KEY,                 -- LeetCode 题号 (704 表示 LC704)
    title       TEXT NOT NULL,
    difficulty  TEXT CHECK (difficulty IN ('easy','medium','hard')),
    tags        TEXT NOT NULL DEFAULT '[]',          -- JSON array: ["hash","array"]
    source      TEXT,                                -- "hot100" / "carl-array" / ...
    carl_url    TEXT
    study_order INTEGER  
);

-- 不可变事件流：每次练习只追加，永不 UPDATE/DELETE。这是你的"历史真相"。
CREATE TABLE practice_log (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_id   INTEGER NOT NULL REFERENCES problems(id),
    practiced_at TEXT    NOT NULL DEFAULT (datetime('now')),
    self_score   INTEGER CHECK (self_score BETWEEN 1 AND 5)
);

-- 当前复习状态：每题一行，每次练习后被覆盖更新。这是"现在该干嘛"。
CREATE TABLE review_state (
    problem_id     INTEGER PRIMARY KEY REFERENCES problems(id),
    reps           INTEGER NOT NULL DEFAULT 0,       -- 连续通过次数
    ease           REAL    NOT NULL DEFAULT 2.5,     -- 难度系数 (SM-2 风格)
    interval_days  INTEGER NOT NULL DEFAULT 0,
    last_practiced TEXT,
    next_review_at TEXT
);

CREATE INDEX idx_log_problem ON practice_log(problem_id);
CREATE INDEX idx_review_due  ON review_state(next_review_at);