from pydantic import BaseModel

class NewProblemIn(BaseModel):
    problem_id: int

class ProblemOut(BaseModel):
    problem_id: int
    title: str
    source: str | None

class SessionOut(BaseModel):
    session_id: str
    problem_id: int
    title: str
    total: int           # 今天共几道题
    source: str | None = None

class SubmitIn(BaseModel):
    lc_result: str       # "ac" | "wa"
    code: str

class SubmitOut(BaseModel):
    score: int | None = None
    next_action: str     # "hint" | "reveal" | "next_problem" | "done"
    message: str | None = None        # hint 文本 / reveal / AC 优化提示
    next_problem_id: int | None = None
    next_title: str | None = None
    next_source: str | None = None

class GradeIn(BaseModel):
    problem_id: str
    code: str
    lc_result: str

class HintIn(BaseModel):
    problem_id: str
    code: str
    status: str        # "AC" | "WA"
    mode: str = "direct"  # "direct" | "socratic"，仅对 WA 生效