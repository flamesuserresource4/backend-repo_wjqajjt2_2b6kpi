from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents
from schemas import Candidate, Job, Application

app = FastAPI(title="IT Recruitment API")

# CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    employment_type: str
    description: str
    requirements: List[str]
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    tags: List[str] = []

class CandidateCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    skills: List[str] = []
    experience_years: Optional[int] = 0
    location: Optional[str] = None
    portfolio_url: Optional[str] = None

class ApplicationCreate(BaseModel):
    candidate_email: str
    job_id: str
    cover_letter: Optional[str] = None

@app.get("/", tags=["health"]) 
async def root():
    return {"message": "IT Recruitment API is running"}

@app.get("/test", tags=["health"]) 
async def test_db():
    items = await get_documents("job", limit=1)
    return {"ok": True, "sample": items}

# Jobs
@app.post("/jobs", response_model=Job, tags=["jobs"]) 
async def create_job(job: JobCreate):
    created = await create_document("job", job.model_dump())
    return Job(**created)  # type: ignore

@app.get("/jobs", response_model=List[Job], tags=["jobs"]) 
async def list_jobs(tag: Optional[str] = None):
    filter_dict = {"tags": {"$in": [tag]}} if tag else {}
    items = await get_documents("job", filter_dict=filter_dict, limit=50)
    return [Job(**i) for i in items]  # type: ignore

# Candidates
@app.post("/candidates", response_model=Candidate, tags=["candidates"]) 
async def create_candidate(candidate: CandidateCreate):
    created = await create_document("candidate", candidate.model_dump())
    return Candidate(**created)  # type: ignore

@app.get("/candidates", response_model=List[Candidate], tags=["candidates"]) 
async def list_candidates(skill: Optional[str] = None):
    filter_dict = {"skills": {"$in": [skill]}} if skill else {}
    items = await get_documents("candidate", filter_dict=filter_dict, limit=50)
    return [Candidate(**i) for i in items]  # type: ignore

# Applications
@app.post("/applications", response_model=Application, tags=["applications"]) 
async def create_application(apply: ApplicationCreate):
    created = await create_document("application", apply.model_dump())
    return Application(**created)  # type: ignore

@app.get("/applications", response_model=List[Application], tags=["applications"]) 
async def list_applications(candidate_email: Optional[str] = None):
    filter_dict = {"candidate_email": candidate_email} if candidate_email else {}
    items = await get_documents("application", filter_dict=filter_dict, limit=50)
    return [Application(**i) for i in items]  # type: ignore
