from pydantic import BaseModel
from typing import List, Dict, Any

class CandidateMetrics(BaseModel):
    skills_match_ratio: float = 0.0
    years_experience: float = 0.0
    education_level_match: float = 0.0
    projects_relevance: float = 0.0
    certifications_match: float = 0.0
    ats_keyword_density: float = 0.0
    semantic_similarity: float = 0.0

class ExplainabilityRequest(BaseModel):
    candidate_metrics: CandidateMetrics

class FeatureContribution(BaseModel):
    feature: str
    impact: float
    percentage_str: str

class LimeExplanation(BaseModel):
    predicted_score_percentage: str
    positive_contributions: List[FeatureContribution]
    negative_contributions: List[FeatureContribution]
    missing_skills_impact: List[FeatureContribution] = []
    visualization_json: Dict[str, Any] = {}

class ShapExplanation(BaseModel):
    base_value: float
    local_contributions: List[FeatureContribution]
    visualization_json: Dict[str, Any] = {}
