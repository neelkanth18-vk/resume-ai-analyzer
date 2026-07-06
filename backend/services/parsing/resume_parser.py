import fitz  # PyMuPDF
import docx
import spacy
import re
from typing import Dict, Any

# Load spaCy NLP model safely
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

class ResumeParser:
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        text = ""
        try:
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return text

    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        text = ""
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX: {e}")
        return text

    @staticmethod
    def parse(file_path: str) -> Dict[str, Any]:
        """
        Extracts raw text and structures it into entities (Name, Email, Skills).
        """
        if file_path.endswith('.pdf'):
            raw_text = ResumeParser.extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            raw_text = ResumeParser.extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format")

        clean_text = re.sub(r'\s+', ' ', raw_text).strip()
        
        # Heuristic: The first non-empty line of a resume is almost always the candidate's name.
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
        name = lines[0] if lines else "Unknown"
        
        email = "Unknown"
        
        if nlp:
            doc = nlp(clean_text)
            # We can skip spaCy name extraction since the first line heuristic is usually better for resumes
                
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', clean_text)
        if email_match:
            email = email_match.group(0)
            
        common_skills = [
            "python", "java", "c++", "c#", "react", "node.js", "aws", "docker", 
            "kubernetes", "fastapi", "machine learning", "sql", "git", "javascript",
            "typescript", "go", "ruby", "django", "flask", "pytorch", "tensorflow"
        ]
        
        text_lower = clean_text.lower()
        found_skills = [skill for skill in common_skills if skill in text_lower]

        return {
            "name": name,
            "email": email,
            "skills": found_skills,
            "raw_text": clean_text,
            "raw_text_length": len(clean_text)
        }
