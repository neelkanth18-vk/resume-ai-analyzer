import React, { useState } from 'react';
import apiClient from '../api/client';
import { Briefcase, CheckCircle } from 'lucide-react';

export default function JobDescriptionForm({ onParsed }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);
  const [parsedSkills, setParsedSkills] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus('');
    setParsedSkills([]);
    
    try {
      const response = await apiClient.post('/jobs/', {
        title,
        description
      });
      setStatus('Job successfully created and parsed!');
      const reqs = JSON.parse(response.data.requirements || '[]');
      setParsedSkills(reqs);
      if (onParsed) onParsed({ text: description, skills: reqs });
      setTitle('');
      setDescription('');
    } catch (err) {
      setStatus(err.response?.data?.detail || 'Failed to create job');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto mt-8 grid grid-cols-1 md:grid-cols-2 gap-8">
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <Briefcase className="text-indigo-500 h-6 w-6"/> Post a Job Description
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-gray-700 font-medium mb-1">Job Title</label>
            <input 
              type="text" 
              className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-gray-50" 
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Senior Frontend Engineer"
              required 
            />
          </div>
          <div>
            <label className="block text-gray-700 font-medium mb-1">Job Description</label>
            <textarea 
              className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-gray-50 h-32" 
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Paste the full job requirements and responsibilities here..."
              required 
            ></textarea>
          </div>
          <button 
            type="submit"
            disabled={loading}
            className={`w-full py-2 rounded-md font-bold text-white transition shadow-sm ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'}`}
          >
            {loading ? 'Processing...' : 'Parse & Save Job'}
          </button>
        </form>

        {status && (
          <div className={`mt-4 p-3 rounded-md flex items-center gap-2 ${status.includes('success') ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
            {status.includes('success') && <CheckCircle className="h-5 w-5" />}
            <p className="text-sm font-medium">{status}</p>
          </div>
        )}
      </div>

      {parsedSkills.length > 0 && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Required Skills Extracted</h2>
          <p className="text-sm text-gray-500 mb-4">The AI has automatically analyzed the job description and extracted the following core requirements:</p>
          <div className="flex flex-wrap gap-2">
            {parsedSkills.map((skill, i) => (
              <span key={i} className="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm font-medium uppercase">
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
