import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';

export default function ExplainabilityDash({ explanationData }) {
  if (!explanationData) return null;

  // Combine positive and negative impacts into one dataset for the waterfall/bar chart
  const data = [
    ...explanationData.feature_importance,
    ...explanationData.weakness_penalties
  ].sort((a, b) => b.impact - a.impact);

  return (
    <div className="bg-slate-800 p-8 rounded-xl mt-8 text-white shadow-2xl animate-fade-in-up">
      <h2 className="text-2xl font-bold mb-2">Explainable AI (XAI) Engine</h2>
      <p className="text-slate-400 mb-8">
        This chart reveals exactly how the AI weighted specific elements of your resume.
        Positive bars (green) show keywords that boosted your score. Negative bars (red) show penalties.
      </p>

      <div className="h-96 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ top: 20, right: 30, left: 150, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal={false} />
            <XAxis type="number" stroke="#94a3b8" />
            <YAxis dataKey="name" type="category" stroke="#94a3b8" width={200} tick={{fill: '#e2e8f0'}} />
            <Tooltip 
              cursor={{fill: '#334155'}}
              contentStyle={{backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#f8fafc'}}
              formatter={(value) => [`${value > 0 ? '+' : ''}${value} points`, 'Score Impact']}
            />
            <ReferenceLine x={0} stroke="#cbd5e1" />
            <Bar dataKey="impact" radius={[0, 4, 4, 0]}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.impact > 0 ? '#10b981' : '#ef4444'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      
      <div className="mt-6 p-4 bg-slate-700 rounded-lg text-sm text-slate-300">
        <strong>How this works:</strong> The AI iteratively removes individual skills and analyzes weaknesses to calculate the exact mathematical impact on your final {explanationData.baseline_score}/100 ATS Score.
      </div>
    </div>
  );
}
