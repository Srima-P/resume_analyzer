from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil, os

from db_setup import create_database
from database import save_candidate, get_candidates

from parser import (
    extract_text,
    extract_cgpa,
    extract_skills,
    extract_certifications,
    extract_project_weights
)

from scoring import calculate_score
from job_matcher import calculate_skill_match

from auth import create_token, verify_token

app = FastAPI()

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "resumes")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- MODELS ----------------
class JobRequest(BaseModel):
    required_skills: list[str]

class LoginRequest(BaseModel):
    username: str
    password: str

# ---------------- AUTH ----------------
def require_interviewer(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)

    if not payload or payload.get("role") != "interviewer":
        raise HTTPException(status_code=403, detail="Access denied")

# ---------------- STARTUP ----------------
@app.on_event("startup")
def startup():
    create_database()

# ---------------- ROUTES ----------------
@app.get("/")
def home():
    return {"message": "Resume Analyzer API Running"}

# ---------------- LOGIN ----------------
@app.post("/login")
def login(user: LoginRequest):

    if user.username == "admin" and user.password == "admin":
        token = create_token({"role": "interviewer"})
        return {"token": token, "role": "interviewer"}

    else:
        token = create_token({
            "role": "candidate",
            "username": user.username
        })
        return {"token": token, "role": "candidate"}

# ---------------- UPLOAD ----------------
@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):

    path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(path)

    cgpa = extract_cgpa(text)
    skills = extract_skills(text)
    certs = extract_certifications(text)
    projects = extract_project_weights(text)

    score = calculate_score(cgpa, projects, certs, len(skills))

    candidate = {
        "name": file.filename,
        "score": score,
        "cgpa": cgpa,
        "skills": skills,
        "projects": projects,
        "certifications": certs,
        "resume": path
    }

    save_candidate(candidate)

    return {
        "message": "Uploaded",
        "score": score,
        "skills": skills,
        "projects": projects,
        "certifications": certs
    }

# ---------------- CANDIDATES ----------------
@app.get("/candidates")
def candidates(auth=Depends(require_interviewer)):
    return get_candidates()

# ---------------- LEADERBOARD ----------------
@app.get("/leaderboard")
def leaderboard(auth=Depends(require_interviewer)):

    data = get_candidates()
    data.sort(key=lambda x: x["score"], reverse=True)

    return {
        "leaderboard": [
            {"rank": i+1, "name": c["name"], "score": c["score"]}
            for i, c in enumerate(data)
        ]
    }

# ---------------- JOB MATCH ----------------
@app.post("/job_match")
def job_match(job: JobRequest, auth=Depends(require_interviewer)):

    data = get_candidates()
    results = []

    for c in data:
        percent, matched = calculate_skill_match(
            c["skills"], job.required_skills
        )

        c["match_percent"] = percent
        c["matched_skills"] = matched
        results.append(c)

    results.sort(key=lambda x: x["match_percent"], reverse=True)

    return {"results": results}

# ---------------- VIEW RESUME ----------------
@app.get("/resume/{filename}")
def view_resume(filename: str):

    if not filename.endswith(".pdf"):
        filename += ".pdf"

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Resume not found")

    return FileResponse(file_path)

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)