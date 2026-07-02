from fastapi import APIRouter, HTTPException
from app.schemas import NewProblemIn, ProblemOut, GradeIn, HintIn, SessionOut, SubmitIn, SubmitOut
from app.services import agent

router = APIRouter()

@router.post("/problems/new", response_model=ProblemOut)
async def new_problem(req: NewProblemIn):
    result = agent.start_new_problem(req.problem_id)
    if result is None:
        raise HTTPException(404, "problem not found")
    return result

@router.post("/attempts/grade")
async def grade(req: GradeIn):
    return agent.grade_attempt(req.problem_id, req.code, req.lc_result)

@router.post("/hints")
async def hint(req: HintIn):
    return agent.get_hint(req.problem_id, req.code, status=req.status, mode=req.mode)

@router.post("/new-sessions", response_model=SessionOut)
async def create_new_session():
    result = agent.create_new_session()
    if result is None:
        raise HTTPException(404, "no unstarted problems left")
    return result

@router.post("/sessions", response_model=SessionOut)
async def create_session():
    result = agent.create_review_session()
    if result is None:
        raise HTTPException(404, "no problems due today")
    return result

@router.post("/sessions/{session_id}/submit", response_model=SubmitOut)
async def submit(session_id: str, req: SubmitIn):
    result = agent.submit_attempt(session_id, req.lc_result, req.code)
    if result is None:
        raise HTTPException(404, "session not found")
    return result