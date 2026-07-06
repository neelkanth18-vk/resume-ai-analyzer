import React, { useState } from 'react';
import { Check, X, AlertTriangle, Lightbulb, TrendingUp } from 'lucide-react';
import ExplainabilityDash from './ExplainabilityDash';
import apiClient from '../api/client';

export default function CandidateReport({ data, jobData, resumeData }) {
  const [xaiData, setXaiData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleExplain = async () => {
    if (xaiData) return; // already loaded
    setLoading(true);
    try {
      const response = await apiClient.post('/explain/candidate', {
        resume_text: resumeData.text,
        jd_text: jobData.text,
        resume_skills: resumeData.skills,
        jd_skills: jobData.skills
      });
      setXaiData(response.data);
    } catch (err) {
      console.error("XAI error", err);
    } finally {
      setLoading(false);
    }
  };

  if (!data) return null;

  return (
    <div className="bg-white p-8 rounded-xl shadow-lg border border-gray-200 mt-8 animate-fade-in-up">
      <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">Detailed Resume Gap Analysis</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
        <div className="bg-indigo-50 p-6 rounded-xl border border-indigo-100 flex flex-col items-center justify-center shadow-sm">
          <p className="text-indigo-600 font-semibold uppercase tracking-wider mb-2 text-sm">Overall Match Score</p>
          <p className="text-7xl font-black text-indigo-700">{data.overall_match_score}</p>
        </div>
        <div className="bg-blue-50 p-6 rounded-xl border border-blue-100 flex flex-col items-center justify-center shadow-sm">
          <p className="text-blue-600 font-semibold uppercase tracking-wider mb-2 text-sm">ATS Score</p>
          <p className="text-7xl font-black text-blue-700">{data.ats_score}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
        <div className="bg-gray-50 p-6 rounded-xl border border-gray-100">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            Matched Skills
          </h3>
          <ul className="space-y-3">
            {data.matched_skills.map((skill, i) => (
              <li key={i} className="flex items-center gap-3 text-gray-700 font-medium">
                <Check className="h-6 w-6 text-green-500 bg-green-100 rounded-full p-1" /> {skill}
              </li>
            ))}
            {data.matched_skills.length === 0 && <p className="text-gray-500 italic">No exact skill matches found.</p>}
          </ul>
        </div>
        
        <div className="bg-gray-50 p-6 rounded-xl border border-gray-100">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            Missing Skills
          </h3>
          <ul className="space-y-3">
            {data.missing_skills.map((skill, i) => (
              <li key={i} className="flex items-center gap-3 text-gray-700 font-medium">
                <X className="h-6 w-6 text-red-500 bg-red-100 rounded-full p-1" /> {skill}
              </li>
            ))}
            {data.missing_skills.length === 0 && <p className="text-gray-500 italic">No missing skills! You meet all requirements.</p>}
          </ul>
        </div>
      </div>

      <div className="border-t border-gray-200 pt-8 mb-8">
        <h3 className="text-xl font-bold text-gray-800 mb-5 flex items-center gap-2">
          <AlertTriangle className="text-orange-500 h-6 w-6" /> Resume Weaknesses
        </h3>
        <ul className="space-y-4">
          {data.weaknesses.map((weakness, i) => (
            <li key={i} className="flex items-start gap-4 text-gray-700 bg-orange-50 p-4 rounded-lg border border-orange-100">
              <span className="text-orange-500 font-black text-xl leading-none mt-1">•</span>
              <span className="font-medium">{weakness}</span>
            </li>
          ))}
          {data.weaknesses.length === 0 && <p className="text-green-600 font-medium bg-green-50 p-4 rounded-lg">No major structural weaknesses detected!</p>}
        </ul>
      </div>

      <div className="bg-yellow-50 p-6 rounded-xl border border-yellow-100 shadow-sm mb-10">
        <h3 className="text-xl font-bold text-gray-800 mb-5 flex items-center gap-2">
          <Lightbulb className="text-yellow-600 h-6 w-6" /> Suggestions for Improvement
        </h3>
        <ul className="space-y-4">
          {data.suggestions.map((suggestion, i) => (
            <li key={i} className="flex items-start gap-4 text-gray-800 bg-white p-4 rounded-lg border border-yellow-200 shadow-sm">
              <span className="text-yellow-500 font-black text-xl leading-none mt-1">•</span>
              <span className="font-medium">{suggestion}</span>
            </li>
          ))}
          {data.suggestions.length === 0 && <p className="text-gray-600">Your resume structure is fully optimized for ATS.</p>}
        </ul>
      </div>

      <div className="border-t border-gray-200 pt-8 text-center">
        <button 
          onClick={handleExplain}
          disabled={loading}
          className={`flex items-center gap-2 mx-auto px-8 py-3 rounded-full font-bold text-white transition shadow-md ${loading ? 'bg-slate-400 cursor-not-allowed' : 'bg-slate-800 hover:bg-slate-900 hover:scale-105 transform'}`}
        >
          <TrendingUp className="h-5 w-5" />
          {loading ? 'Analyzing Neural Weights...' : 'Why did I get this score?'}
        </button>
      </div>

      {xaiData && <ExplainabilityDash explanationData={xaiData} />}
    </div>
  );
}
