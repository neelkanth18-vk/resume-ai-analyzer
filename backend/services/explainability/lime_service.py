import numpy as np
import lime
import lime.lime_tabular
from typing import List

from .feature_extractor import FeatureExtractor
from schemas.explainability import LimeExplanation, FeatureContribution

class LimeService:
    def __init__(self):
        # LIME requires a background dataset to calculate feature statistics (mean, variance).
        # In production, this would be your historical candidate features matrix.
        np.random.seed(42)
        self.background_data = np.random.rand(100, len(FeatureExtractor.get_feature_names()))
        
        self.explainer = lime.lime_tabular.LimeTabularExplainer(
            self.background_data,
            feature_names=FeatureExtractor.get_feature_names(),
            class_names=['Match Score'],
            mode='regression',
            random_state=42
        )
        
    def _predict_fn(self, X: np.ndarray) -> np.ndarray:
        """
        A dummy scoring function simulating an AI model.
        It heavily weights skills and semantic similarity.
        """
        # Weights corresponding to FEATURE_NAMES
        weights = np.array([0.35, 0.10, 0.05, 0.10, 0.05, 0.10, 0.25])
        return np.dot(X, weights)

    def explain_candidate(self, candidate_features: np.ndarray, missing_skills: List[str] = None) -> LimeExplanation:
        """
        Generates a LIME explanation for a single candidate.
        """
        # Ensure 1D array for single instance
        if candidate_features.ndim > 1:
            candidate_features = candidate_features.flatten()

        exp = self.explainer.explain_instance(
            candidate_features, 
            self._predict_fn, 
            num_features=len(FeatureExtractor.get_feature_names())
        )
        
        positive = []
        negative = []
        
        for feature_desc, impact in exp.as_list():
            # Clean up feature name from LIME's condition (e.g. "skills_match_ratio > 0.8")
            clean_name = feature_desc
            for fn in FeatureExtractor.get_feature_names():
                if fn in feature_desc:
                    clean_name = fn.replace("_", " ").title()
                    break
                    
            contribution = FeatureContribution(
                feature=clean_name,
                impact=float(impact),
                percentage_str=f"{impact * 100:+.1f}%"
            )
            
            if impact > 0:
                positive.append(contribution)
            else:
                negative.append(contribution)
                
        # Sort by absolute impact
        positive.sort(key=lambda x: abs(x.impact), reverse=True)
        negative.sort(key=lambda x: abs(x.impact), reverse=True)

        # Handle missing skills penalty visualization
        missing_impacts = []
        if missing_skills:
            for skill in missing_skills:
                missing_impacts.append(
                    FeatureContribution(
                        feature=skill,
                        impact=-0.03, # Simulated 3% penalty
                        percentage_str="-3.0%"
                    )
                )

        predicted_score = self._predict_fn(candidate_features.reshape(1, -1))[0]

        return LimeExplanation(
            predicted_score_percentage=f"{predicted_score * 100:.1f}%",
            positive_contributions=positive,
            negative_contributions=negative,
            missing_skills_impact=missing_impacts
        )

# Instantiate as a singleton to avoid recreating the explainer (which is slow)
lime_service = LimeService()
