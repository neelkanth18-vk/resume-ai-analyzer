from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from models.job import Job
from api.deps import get_current_user

router = APIRouter()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_count = db.query(User).count()
    job_count = db.query(Job).count()
    return {"users": user_count, "jobs": job_count}
