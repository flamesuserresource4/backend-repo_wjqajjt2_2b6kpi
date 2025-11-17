from typing import Optional
from pydantic import BaseModel, Field, EmailStr

# Each model corresponds to a MongoDB collection with the lowercased class name

class Candidate(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    email: EmailStr
    phone: Optional[str] = None
    skills: list[str] = []
    experience_years: Optional[int] = 0
    location: Optional[str] = None
    portfolio_url: Optional[str] = None

class Job(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    company: str
    location: str
    employment_type: str  # e.g., Full-time, Contract
    description: str
    requirements: list[str]
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    tags: list[str] = []

class Application(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    candidate_email: EmailStr
    job_id: str
    cover_letter: Optional[str] = None
    status: str = "submitted"  # submitted, reviewing, interviewed, offered, rejected
