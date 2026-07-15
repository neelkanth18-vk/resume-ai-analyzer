# 🚀 AI Resume Analyzer

An AI-powered Resume Analyzer that evaluates resumes against a given Job Description (JD), calculates an ATS compatibility score, identifies missing skills, and provides personalized improvement suggestions. The application uses Natural Language Processing (NLP) and Explainable AI techniques to help candidates optimize their resumes for modern Applicant Tracking Systems (ATS).

---

## 🌐 Live Demo

**Frontend (Vercel):**
https://neelkanth18-vk-resume-ai-analyzer.vercel.app

**Backend API (Railway):**
https://resume-ai-analyzer-production-d578.up.railway.app

---

# 📌 Features

### User Authentication

* User Registration
* Secure Login using JWT Authentication
* Password Hashing with bcrypt

### Resume Analysis

* Upload Resume (PDF/DOCX)
* Resume Parsing
* Job Description Input
* ATS Score Calculation
* Skill Matching
* Missing Skill Detection
* Resume Improvement Suggestions

### AI & Explainability

* NLP-based Resume Parsing using spaCy
* SHAP Explainability
* LIME Explainability
* Skill Gap Analysis

### Dashboard

* Resume Analysis Report
* ATS Compatibility Score
* Missing Skills List
* Resume Recommendations

---

# 🛠 Tech Stack

## Frontend

* React.js
* Vite
* Tailwind CSS
* Axios
* React Router

## Backend

* FastAPI
* SQLAlchemy
* Alembic
* JWT Authentication
* Passlib (bcrypt)

## Database

* Aiven MySQL

## AI / Machine Learning

* spaCy
* SHAP
* LIME
* Natural Language Processing (NLP)

## Deployment

* Vercel (Frontend)
* Railway (Backend)
* Aiven Cloud MySQL (Database)

## Version Control

* Git
* GitHub

---

# 📂 Project Structure

```
resume-ai-analyzer/
│
├── backend/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── core/
│   ├── alembic/
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── App.jsx
│
└── README.md
```

---

# 📸 Application Screenshots

Add screenshots here:

* Home Page
* Register Page
* Login Page
* Dashboard
* Resume Upload
* Job Description Input
* ATS Score
* Resume Analysis Report
* Skill Gap Analysis
* Explainability (SHAP/LIME)

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/resume-ai-analyzer.git
cd resume-ai-analyzer
```

### Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

alembic upgrade head

uvicorn main:app --reload
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 🔐 Environment Variables

## Backend (.env)

```
DATABASE_URL=your_database_url

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=10080

FRONTEND_URL=http://localhost:5173
```

## Frontend (.env)

```
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

---

# 🚀 Future Enhancements

* AI Resume Rewriter using LLMs
* Interview Question Generator
* Resume Version History
* PDF Report Generation
* Admin Analytics Dashboard
* Multi-language Resume Support
* AI Career Recommendations

---

# 📖 Learning Outcomes

* Full Stack Web Development
* REST API Development
* Authentication with JWT
* Database Design using MySQL
* Cloud Deployment
* NLP-based Resume Parsing
* Explainable AI (SHAP & LIME)
* CI/CD Deployment Workflow

---

# 👨‍💻 Author

**Neelkanth Rayaji**

Final Year B.E. Student

AI | Full Stack Development | Machine Learning | NLP

---

## ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub.
