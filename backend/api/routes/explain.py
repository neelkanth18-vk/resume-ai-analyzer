from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from services.xai import generate_lime_explanation
from api.deps import get_current_user

router = APIRouter()

class ExplainRequest(BaseModel):
    resume_text: str
    jd_text: str
    resume_skills: List[str] = []
    jd_skills: List[str] = []

@router.post("/candidate")
def explain_candidate_score(req: ExplainRequest, current_user = Depends(get_current_user)):
    """
    Generates a LIME-like explanation of why the candidate received their specific score.
    """
    explanation = generate_lime_explanation(
        req.resume_text,
        req.jd_text,
        req.resume_skills,
        req.jd_skills
    )
    return explanation
