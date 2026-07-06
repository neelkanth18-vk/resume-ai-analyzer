import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';

function App() {
  const isAuthenticated = !!localStorage.getItem('token');

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route 
          path="/" 
          element={
            isAuthenticated ? 
            (
              <div className="min-h-screen bg-gray-50 p-8">
                <div className="flex justify-between items-center mb-10 max-w-6xl mx-auto">
                  <h1 className="text-3xl font-bold text-blue-600">ATS Dashboard</h1>
                  <button 
                    onClick={() => {
                      localStorage.removeItem('token'); 
                      window.location.reload();
                    }} 
                    className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold px-4 py-2 rounded-md shadow-sm transition"
                  >
                    Logout
                  </button>
                </div>
                
                <Dashboard />
              </div>
            ) : 
            <Navigate to="/login" />
          } 
        />
      </Routes>
    </Router>
  );
}

export default App;
