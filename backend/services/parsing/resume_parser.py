import fitz  # PyMuPDF
import docx
import spacy
import re
from typing import Dict, Any

from services.common.skills_database import (
    TECHNICAL_SKILLS,
    SOFT_SKILLS
)

# Load spaCy model safely
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
    def extract_skills(text: str):
        """
        Extract technical and soft skills
        using the centralized skill database.
        """

        text_lower = text.lower()

        technical = []

        for category, skills in TECHNICAL_SKILLS.items():

            for skill in skills:

                if skill.lower() in text_lower:
                    technical.append(skill)

        technical = sorted(list(set(technical)))

        soft = []

        for skill in SOFT_SKILLS:

            if skill.lower() in text_lower:
                soft.append(skill)

        return technical, soft 
    
    @staticmethod
    def extract_phone(text: str) -> str:
     pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3,5}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'
     match = re.search(pattern, text)
     return match.group(0).strip() if match else "Not Found"

    @staticmethod
    def extract_linkedin(text: str) -> str:
     pattern = r'(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+'
     match = re.search(pattern, text, re.IGNORECASE)
     return match.group(0) if match else "Not Found"

    @staticmethod
    def extract_github(text: str) -> str:
     pattern = r'(https?://)?(www\.)?github\.com/[A-Za-z0-9_-]+'
     match = re.search(pattern, text, re.IGNORECASE)
     return match.group(0) if match else "Not Found"

    @staticmethod
    def extract_portfolio(text: str) -> str:
        pattern = r'https?://[^\s]+'
        matches = re.findall(pattern, text)

        for url in matches:
            lower = url.lower()

            if "github" in lower:
                continue

            if "linkedin" in lower:
                continue

            return url

        return "Not Found"

    @staticmethod
    def parse(file_path: str) -> Dict[str, Any]:

        if file_path.endswith(".pdf"):

            raw_text = ResumeParser.extract_text_from_pdf(file_path)

        elif file_path.endswith(".docx"):

            raw_text = ResumeParser.extract_text_from_docx(file_path)

        else:

            raise ValueError("Unsupported file format")

        clean_text = re.sub(r"\s+", " ", raw_text).strip()

        lines = [
            line.strip()
            for line in raw_text.split("\n")
            if line.strip()
        ]

        name = lines[0] if lines else "Unknown"

        email = "Unknown"

        if nlp:
            doc = nlp(clean_text)

        email_match = re.search(
            r'[\w\.-]+@[\w\.-]+',
            clean_text
        )

        if email_match:
            email = email_match.group(0)
        phone = ResumeParser.extract_phone(clean_text)

        linkedin = ResumeParser.extract_linkedin(clean_text)

        github = ResumeParser.extract_github(clean_text)

        portfolio = ResumeParser.extract_portfolio(clean_text)

        technical_skills, soft_skills = ResumeParser.extract_skills(
            clean_text
        )

        return {

            "name": name,

            "email": email,

            "phone": phone,

            "linkedin": linkedin,

            "github": github,

            "portfolio": portfolio,

            "skills": technical_skills,

            "technical_skills": technical_skills,

            "soft_skills": soft_skills,

            "raw_text": clean_text,

            "raw_text_length": len(clean_text)

        }