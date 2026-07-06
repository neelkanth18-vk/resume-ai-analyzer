import React, { useState, useEffect } from 'react';
import ResumeUpload from '../components/ResumeUpload';
import JobDescriptionForm from '../components/JobDescriptionForm';
import CandidateReport from '../components/CandidateReport';
import apiClient from '../api/client';
import { Target, UserCircle, Users, FileText, Activity } from 'lucide-react';

export default function Dashboard() {
  const [jobData, setJobData] = useState(null);
  const [resumeData, setResumeData] = useState(null);
  const [scoreResult, setScoreResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState(null);
  
  // Admin stats
  const [stats, setStats] = useState({ users: 0, jobs: 0 });

  useEffect(() => {
    apiClient.get('/auth/me')
      .then(res => {
        setUser(res.data);
        if (res.data.role === 'admin') {
          fetchAdminStats();
        }
      })
      .catch(err => console.error(err));
  }, []);
  
  const fetchAdminStats = async () => {
    try {
      const res = await apiClient.get('/admin/stats');
      setStats(res.data);
    } catch (e) {
      console.error("Failed to load admin stats");
    }
  };

  const handleGenerateScore = async () => {
    if (!jobData || !resumeData) return;
    setLoading(true);
    setScoreResult(null);
    try {
      const response = await apiClient.post('/score/', {
        resume_text: resumeData.text,
        jd_text: jobData.text,
        resume_skills: resumeData.skills,
        jd_skills: jobData.skills
      });
      setScoreResult(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!user) return <div className="text-center mt-20 text-gray-500 font-medium">Loading profile...</div>;

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="bg-blue-50 border border-blue-100 rounded-lg p-4 flex justify-between items-center text-blue-800 shadow-sm">
        <div className="flex items-center gap-3">
          <UserCircle className="h-8 w-8 text-blue-600" />
          <div>
            <p className="font-bold text-lg">{user.full_name}</p>
            <p className="text-sm uppercase tracking-wider font-semibold opacity-80">{user.role}</p>
          </div>
        </div>
      </div>

      {user.role === 'admin' ? (
        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            <Activity className="text-blue-500" /> Platform Overview
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gray-50 p-6 rounded-lg border border-gray-200 flex flex-col items-center">
              <Users className="h-8 w-8 text-blue-500 mb-3" />
              <p className="text-gray-500 font-medium mb-1">Total Users</p>
              <p className="text-4xl font-black text-gray-800">{stats.users}</p>
            </div>
            <div className="bg-gray-50 p-6 rounded-lg border border-gray-200 flex flex-col items-center">
              <FileText className="h-8 w-8 text-green-500 mb-3" />
              <p className="text-gray-500 font-medium mb-1">Uploaded Jobs</p>
              <p className="text-4xl font-black text-gray-800">{stats.jobs}</p>
            </div>
            <div className="bg-gray-50 p-6 rounded-lg border border-gray-200 flex flex-col items-center">
              <Target className="h-8 w-8 text-purple-500 mb-3" />
              <p className="text-gray-500 font-medium mb-1">Status</p>
              <p className="text-2xl font-black text-green-600 mt-2">Operational</p>
            </div>
          </div>
        </div>
      ) : (
        <>
          <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-200">
            <h2 className="text-xl font-bold mb-4 text-gray-800">1. Paste Job Description</h2>
            <JobDescriptionForm onParsed={(data) => setJobData(data)} />
          </div>
          
          <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-200 mt-8">
            <h2 className="text-xl font-bold mb-4 text-gray-800">2. Upload Your Resume</h2>
            <ResumeUpload onParsed={(data) => setResumeData(data)} />
          </div>
          
          {jobData && resumeData && (
            <div className="text-center mt-12 mb-8">
              <button
                onClick={handleGenerateScore}
                disabled={loading}
                className={`px-12 py-4 rounded-full font-bold text-xl text-white transition shadow-lg ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700 hover:scale-105 transform'}`}
              >
                {loading ? 'Analyzing Gap...' : 'Analyze Resume'}
              </button>
            </div>
          )}
          
          {scoreResult && <CandidateReport data={scoreResult} jobData={jobData} resumeData={resumeData} />}
        </>
      )}
    </div>
  );
}
