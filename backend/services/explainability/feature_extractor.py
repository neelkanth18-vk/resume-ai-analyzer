import numpy as np

# Core numerical features used by the matching engine
FEATURE_NAMES = [
    "skills_match_ratio",
    "years_experience",
    "education_level_match",
    "projects_relevance",
    "certifications_match",
    "ats_keyword_density",
    "semantic_similarity"
]

class FeatureExtractor:
    """
    Converts structured candidate metrics into a numerical NumPy array
    for our predictive model, LIME, and SHAP to process.
    """
    @staticmethod
    def extract_features(metrics: dict) -> np.ndarray:
        features = [
            float(metrics.get("skills_match_ratio", 0.0)),
            float(metrics.get("years_experience", 0.0)),
            float(metrics.get("education_level_match", 0.0)),
            float(metrics.get("projects_relevance", 0.0)),
            float(metrics.get("certifications_match", 0.0)),
            float(metrics.get("ats_keyword_density", 0.0)),
            float(metrics.get("semantic_similarity", 0.0))
        ]
        return np.array(features)

    @staticmethod
    def get_feature_names() -> list[str]:
        return FEATURE_NAMES
