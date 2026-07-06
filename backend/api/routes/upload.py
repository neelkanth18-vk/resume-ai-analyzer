from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from services.parsing.resume_parser import ResumeParser

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_resume(file: UploadFile = File(...)):
    """
    Accepts a PDF or DOCX resume file and parses it using NLP.
    """
    if not file.filename.endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")
        
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Parse the uploaded file
        parsed_data = ResumeParser.parse(file_path)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
        
    return {
        "filename": file.filename,
        "message": "Resume uploaded and parsed successfully!",
        "parsed_data": parsed_data
    }
