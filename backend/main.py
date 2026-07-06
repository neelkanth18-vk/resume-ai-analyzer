from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS so the React frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.FRONTEND_URL.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.routes import auth, explain, upload, job, match, score, admin

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(explain.router, prefix=f"{settings.API_V1_STR}/explain", tags=["explainability"])
app.include_router(upload.router, prefix=f"{settings.API_V1_STR}/upload", tags=["upload"])
app.include_router(job.router, prefix=f"{settings.API_V1_STR}/jobs", tags=["jobs"])
app.include_router(match.router, prefix=f"{settings.API_V1_STR}/match", tags=["matching"])
app.include_router(score.router, prefix=f"{settings.API_V1_STR}/score", tags=["scoring"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Resume Screening & Recruitment API!"}

@app.get(f"{settings.API_V1_STR}/health")
def health_check():
    return {"status": "healthy"}
