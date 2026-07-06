from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True) # Optional, can upload generally or for a specific job
    
    file_path = Column(String(500), nullable=False)
    parsed_skills = Column(Text)       # Stored as JSON string or comma-separated
    parsed_experience = Column(Text)
    parsed_education = Column(Text)
    
    # AI Analysis Results
    ats_score = Column(Float, default=0.0)
    skill_gap = Column(Text)
    suggestions = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    candidate = relationship("User")
    job = relationship("Job", back_populates="resumes")
