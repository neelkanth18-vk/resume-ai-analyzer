import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/client';

export default function Register() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('candidate');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await apiClient.post('/auth/register', {
        email,
        password,
        full_name: fullName,
        role
      });
      // Auto-redirect to login after successful registration
      navigate('/login');
    } catch (err) {
      // Safely handle validation array from FastAPI to prevent React from crashing
      const detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        setError(detail.map(d => `${d.loc[d.loc.length-1]}: ${d.msg}`).join(', '));
      } else {
        setError(detail || 'Failed to register account');
      }
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-gray-50">
      <div className="w-full max-w-md p-8 bg-white rounded-lg shadow-md border border-gray-100">
        <h2 className="text-3xl font-bold text-center text-blue-600 mb-6">Create Account</h2>
        {error && <p className="text-red-500 text-center mb-4 text-sm font-medium">{error}</p>}
        <form onSubmit={handleRegister} className="space-y-5">
          <div>
            <label className="block text-gray-700 font-medium mb-1">Full Name</label>
            <input 
              type="text" 
              className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50" 
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="John Doe"
              required 
            />
          </div>
          <div>
            <label className="block text-gray-700 font-medium mb-1">Email Address</label>
            <input 
              type="email" 
              className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required 
            />
          </div>
          <div>
            <label className="block text-gray-700 font-medium mb-1">Password</label>
            <input 
              type="password" 
              className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required 
            />
          </div>
          <div>
            <label className="block text-gray-700 font-medium mb-1">I am a...</label>
            <select 
              className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50"
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
              <option value="candidate">Candidate (Job Seeker)</option>
              <option value="admin">Admin (Platform Manager)</option>
            </select>
          </div>
          <button type="submit" className="w-full bg-blue-600 text-white font-bold py-2 rounded-md hover:bg-blue-700 transition shadow-sm">
            Sign Up
          </button>
        </form>
        <p className="mt-6 text-center text-gray-600 text-sm">
          Already have an account? <a href="/login" className="text-blue-600 font-semibold hover:underline">Login</a>
        </p>
      </div>
    </div>
  );
}
