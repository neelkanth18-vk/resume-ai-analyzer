from typing import List
from services.matching.semantic import compute_semantic_similarity
import re

def calculate_ats_score(
    resume_text: str, 
    jd_text: str, 
    resume_skills: List[str], 
    jd_requirements: List[str]
) -> dict:
    
    semantic_score = compute_semantic_similarity(resume_text, jd_text)
    
    r_skills_lower = [s.lower() for s in resume_skills]
    jd_req_lower = [r.lower() for r in jd_requirements]
    
    if not jd_requirements:
        keyword_score = 1.0
        matched_skills = r_skills_lower
        missing_skills = []
    else:
        matched_skills = [req for req in jd_req_lower if req in r_skills_lower or req in resume_text.lower()]
        missing_skills = [req for req in jd_req_lower if req not in matched_skills]
        keyword_score = len(matched_skills) / len(jd_req_lower)
        
    final_score = (semantic_score * 0.4) + (keyword_score * 0.6)
    
    # NLP Heuristics for Weaknesses
    weaknesses = []
    suggestions = []
    
    text_lower = resume_text.lower()
    
    # 1. Quantifiable achievements
    has_metrics = bool(re.search(r'\d+%|\$\d+|\d+x', text_lower))
    if not has_metrics:
        weaknesses.append("No measurable achievements detected")
        suggestions.append("Rewrite project/experience descriptions to include metrics (e.g., 'improved performance by 20%')")
        
    # 2. GitHub profile
    if 'github.com' not in text_lower:
        weaknesses.append("Missing GitHub profile link")
        suggestions.append("Add a link to your GitHub profile to showcase your code")
        
    # 3. Overall length (proxy for detail)
    if len(resume_text) < 500:
        weaknesses.append("Resume content is too brief")
        suggestions.append("Expand on your project descriptions and responsibilities to provide more context")
        
    # 4. LinkedIn profile
    if 'linkedin.com' not in text_lower:
        weaknesses.append("Missing LinkedIn profile link")
        suggestions.append("Add a link to your professional LinkedIn network")
        
    # Deduplicate and capitalize
    matched_skills = [s.title() for s in list(set(matched_skills))]
    missing_skills = [s.title() for s in list(set(missing_skills))]
    
    # Base ATS Score
    ats_score_val = int(final_score * 100)
    
    # Overall Match Score (Pure match percentage)
    overall_match = ats_score_val
    
    # Final ATS score deducts points for weaknesses to simulate strict ATS screening
    deduction = len(weaknesses) * 3
    ats_score_val = max(0, ats_score_val - deduction)
    
    return {
        "overall_match_score": f"{overall_match}%",
        "ats_score": f"{ats_score_val}/100",
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        # Legacy fields
        "semantic_score": float(semantic_score),
        "keyword_score": float(keyword_score),
        "percentage": f"{overall_match}%"
    }
