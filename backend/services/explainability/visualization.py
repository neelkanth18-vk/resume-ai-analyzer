import plotly.graph_objects as go
import plotly.io as pio
import json
from schemas.explainability import LimeExplanation, ShapExplanation

class VisualizationService:
    @staticmethod
    def generate_lime_bar_chart(explanation: LimeExplanation) -> dict:
        features = []
        impacts = []
        colors = []
        
        # Combine positive and negative for plotting
        for contrib in explanation.positive_contributions + explanation.negative_contributions:
            features.append(contrib.feature)
            impacts.append(contrib.impact)
            colors.append('rgba(52, 211, 153, 0.8)' if contrib.impact > 0 else 'rgba(248, 113, 113, 0.8)')
            
        fig = go.Figure(go.Bar(
            x=impacts,
            y=features,
            orientation='h',
            marker_color=colors,
            text=[f"{i*100:+.1f}%" for i in impacts],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="LIME Feature Contributions",
            xaxis_title="Impact on Score",
            yaxis_title="Feature",
            template="plotly_white",
            margin=dict(l=20, r=20, t=40, b=20),
            yaxis={'categoryorder':'total ascending'}
        )
        
        return json.loads(pio.to_json(fig))
        
    @staticmethod
    def generate_shap_waterfall(explanation: ShapExplanation) -> dict:
        features = ["Base Value"] + [c.feature for c in explanation.local_contributions]
        
        measures = ["absolute"] + ["relative" for _ in explanation.local_contributions]
        x_values = [explanation.base_value] + [c.impact for c in explanation.local_contributions]
        
        fig = go.Figure(go.Waterfall(
            name="SHAP", orientation="v",
            measure=measures,
            x=features,
            textposition="outside",
            text=[f"{x*100:+.1f}%" if i > 0 else f"{x*100:.1f}%" for i, x in enumerate(x_values)],
            y=x_values,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "rgba(248, 113, 113, 0.8)"}},
            increasing={"marker": {"color": "rgba(52, 211, 153, 0.8)"}},
            totals={"marker": {"color": "rgba(96, 165, 250, 0.8)"}}
        ))
        
        fig.update_layout(
            title="SHAP Score Breakdown",
            showlegend=False,
            template="plotly_white",
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return json.loads(pio.to_json(fig))

visualization_service = VisualizationService()
