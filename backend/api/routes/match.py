from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from services.matching.semantic import compute_semantic_similarity
from api.deps import get_current_user
from models.user import User

router = APIRouter()

class MatchRequest(BaseModel):
    resume_text: str
    jd_text: str

class MatchResponse(BaseModel):
    similarity_score: float
    percentage: str

@router.post("/semantic", response_model=MatchResponse)
def calculate_semantic_similarity(
    req: MatchRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Computes the raw semantic vector similarity between a candidate's resume and a job description.
    """
    if not req.resume_text or not req.jd_text:
        raise HTTPException(status_code=400, detail="Both resume_text and jd_text are required.")
        
    score = compute_semantic_similarity(req.resume_text, req.jd_text)
    return {
        "similarity_score": score,
        "percentage": f"{score * 100:.2f}%"
    }
