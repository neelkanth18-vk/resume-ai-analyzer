from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.job import Job
from schemas.job import JobCreate, JobResponse
from api.deps import get_current_user
from models.user import User
import json

router = APIRouter()

def extract_skills_from_jd(text: str) -> list:
    common_skills = [
        "python", "java", "c++", "c#", "react", "node.js", "aws", "docker", 
        "kubernetes", "fastapi", "machine learning", "sql", "git", "javascript",
        "typescript", "go", "ruby", "django", "flask", "pytorch", "tensorflow"
    ]
    text_lower = text.lower()
    return [skill for skill in common_skills if skill in text_lower]

@router.post("/", response_model=JobResponse)
def create_job(
    job_in: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Candidates can post jobs for ephemeral analysis
    extracted_skills = extract_skills_from_jd(job_in.description)
    requirements_json = json.dumps(extracted_skills)
    
    new_job = Job(
        title=job_in.title,
        description=job_in.description,
        requirements=requirements_json,
        recruiter_id=current_user.id
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/", response_model=list[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()
