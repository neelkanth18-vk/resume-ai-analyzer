from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from services.scoring import calculate_ats_score
from api.deps import get_current_user
from models.user import User

router = APIRouter()

class ScoreRequest(BaseModel):
    resume_text: str
    jd_text: str
    resume_skills: List[str] = []
    jd_skills: List[str] = []

@router.post("/")
def get_ats_score(
    req: ScoreRequest,
    current_user: User = Depends(get_current_user)
):
    if not req.resume_text or not req.jd_text:
        raise HTTPException(status_code=400, detail="Missing required text data")
        
    result = calculate_ats_score(
        req.resume_text,
        req.jd_text,
        req.resume_skills,
        req.jd_skills
    )
    return result
