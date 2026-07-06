import numpy as np
import shap
from sklearn.ensemble import RandomForestRegressor
from typing import List

from .feature_extractor import FeatureExtractor
from schemas.explainability import ShapExplanation, FeatureContribution

class ShapService:
    def __init__(self):
        # We need a trained model to initialize SHAP. Since we don't have the real ATS 
        # deep learning model here, we train a lightweight surrogate RandomForest 
        # on dummy data so SHAP can compute marginal feature contributions.
        np.random.seed(42)
        X_train = np.random.rand(100, len(FeatureExtractor.get_feature_names()))
        
        # Target variable mimicking our AI scoring weights
        weights = np.array([0.35, 0.10, 0.05, 0.10, 0.05, 0.10, 0.25])
        y_train = np.dot(X_train, weights)
        
        self.model = RandomForestRegressor(n_estimators=50, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Initialize SHAP TreeExplainer (very fast for tree models)
        self.explainer = shap.TreeExplainer(self.model)
        
        # Handle different SHAP versions of expected_value
        expected_val = self.explainer.expected_value
        self.expected_value = expected_val[0] if isinstance(expected_val, np.ndarray) else expected_val

    def explain_candidate(self, candidate_features: np.ndarray) -> ShapExplanation:
        """
        Generates local SHAP explanations for a single candidate.
        This provides the exact data needed for Waterfall and Force plots.
        """
        if candidate_features.ndim > 1:
            candidate_features = candidate_features.flatten()
            
        shap_values = self.explainer.shap_values(candidate_features)
        
        contributions = []
        for i, feature_name in enumerate(FeatureExtractor.get_feature_names()):
            impact = shap_values[i]
            clean_name = feature_name.replace("_", " ").title()
            
            contributions.append(
                FeatureContribution(
                    feature=clean_name,
                    impact=float(impact),
                    percentage_str=f"{impact * 100:+.1f}%"
                )
            )
            
        # Sort contributions by absolute impact for better UI rendering
        contributions.sort(key=lambda x: abs(x.impact), reverse=True)
            
        return ShapExplanation(
            base_value=float(self.expected_value),
            local_contributions=contributions
        )

# Instantiate as singleton
shap_service = ShapService()
