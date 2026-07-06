from services.scoring import calculate_ats_score

def generate_lime_explanation(resume_text: str, jd_text: str, resume_skills: list, jd_requirements: list) -> dict:
    """
    Mimics LIME by systematically removing matched skills and recalculating the ATS score
    to find the exact mathematical impact of each skill on the final score.
    """
    # 1. Get baseline score
    baseline_result = calculate_ats_score(resume_text, jd_text, resume_skills, jd_requirements)
    baseline_score = int(baseline_result["overall_match_score"].replace("%", ""))
    
    impact_data = []
    
    # 2. Calculate impact of matched skills
    for skill in baseline_result["matched_skills"]:
        # Remove skill from resume text and skills list
        perturbed_skills = [s for s in resume_skills if s.lower() != skill.lower()]
        # Naive text removal for semantic perturbation
        perturbed_text = resume_text.replace(skill, "").replace(skill.lower(), "").replace(skill.title(), "")
        
        # Recalculate
        new_result = calculate_ats_score(perturbed_text, jd_text, perturbed_skills, jd_requirements)
        new_score = int(new_result["overall_match_score"].replace("%", ""))
        
        # Impact is how much the score DROPS when we remove the skill
        impact = baseline_score - new_score
        
        # Sometimes semantic similarity makes it weird, ensure we capture positive impact
        if impact > 0:
            impact_data.append({
                "name": skill,
                "impact": impact,
                "type": "positive"
            })
            
    # Sort by highest impact
    impact_data = sorted(impact_data, key=lambda x: x["impact"], reverse=True)
    
    # Calculate negative impacts from weaknesses
    weakness_impact = []
    for weakness in baseline_result["weaknesses"]:
        # We know from scoring.py that each weakness deducts 3 points
        weakness_impact.append({
            "name": weakness,
            "impact": -3,
            "type": "negative"
        })
        
    return {
        "baseline_score": baseline_score,
        "feature_importance": impact_data,
        "weakness_penalties": weakness_impact
    }
