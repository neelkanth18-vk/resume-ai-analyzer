import React, { useState } from 'react';
import apiClient from '../api/client';
import { UploadCloud, CheckCircle, FileText, User, Mail, Star } from 'lucide-react';

export default function ResumeUpload({ onParsed }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);
  const [parsedData, setParsedData] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setStatus('');
    setParsedData(null);
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await apiClient.post('/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setStatus(response.data.message);
      const data = response.data.parsed_data;
      setParsedData(data);
      if (onParsed) onParsed({ text: data.raw_text, skills: data.skills });
      setFile(null); // Clear file after success
    } catch (err) {
      setStatus(err.response?.data?.detail || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto mt-8 grid grid-cols-1 md:grid-cols-2 gap-8">
      {/* Upload Section */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Upload Candidate Resume</h2>
        <div 
          className="border-2 border-dashed border-blue-300 rounded-lg p-10 text-center hover:bg-blue-50 transition cursor-pointer"
          onClick={() => document.getElementById('resume-upload').click()}
        >
          <UploadCloud className="mx-auto h-12 w-12 text-blue-500 mb-3" />
          {file ? (
            <p className="text-gray-700 font-medium">{file.name}</p>
          ) : (
            <p className="text-gray-500">Click to browse for a PDF or DOCX file</p>
          )}
          <input 
            id="resume-upload" 
            type="file" 
            accept=".pdf,.docx" 
            className="hidden" 
            onChange={handleFileChange} 
          />
        </div>
        
        <button 
          onClick={handleUpload}
          disabled={!file || loading}
          className={`w-full mt-4 py-2 rounded-md font-bold text-white transition shadow-sm ${!file || loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}`}
        >
          {loading ? 'Uploading & Parsing...' : 'Process Resume'}
        </button>

        {status && (
          <div className={`mt-4 p-3 rounded-md flex items-center gap-2 ${status.includes('success') ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
            {status.includes('success') && <CheckCircle className="h-5 w-5" />}
            <p className="text-sm font-medium">{status}</p>
          </div>
        )}
      </div>

      {/* Parsed Results Section */}
      {parsedData && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <FileText className="text-blue-500 h-6 w-6"/> Parsed Extraction
          </h2>
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <User className="text-gray-400 h-5 w-5" />
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wider font-semibold">Name</p>
                <p className="font-medium text-gray-800">{parsedData.name}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Mail className="text-gray-400 h-5 w-5" />
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wider font-semibold">Email</p>
                <p className="font-medium text-gray-800">{parsedData.email}</p>
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Star className="text-yellow-400 h-5 w-5" />
                <p className="text-xs text-gray-500 uppercase tracking-wider font-semibold">Extracted Skills</p>
              </div>
              <div className="flex flex-wrap gap-2">
                {parsedData.skills.map((skill, i) => (
                  <span key={i} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium uppercase">
                    {skill}
                  </span>
                ))}
                {parsedData.skills.length === 0 && <span className="text-gray-500 italic text-sm">No standard skills matched.</span>}
              </div>
            </div>
            <div className="mt-4 pt-4 border-t text-sm text-gray-500">
              Raw Text Extracted: {parsedData.raw_text_length} characters
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
