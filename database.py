from db_setup import SessionLocal, Candidate


def save_candidate(candidate):

    db = SessionLocal()

    db_candidate = Candidate(
        name=candidate["name"],
        score=candidate["score"],
        cgpa=str(candidate["cgpa"]),
        skills=",".join(candidate["skills"]),
        projects=str(candidate["projects"]),
        certifications=candidate["certifications"],
        resume_path=candidate["resume"]
    )

    db.add(db_candidate)
    db.commit()
    db.close()


def get_candidates():

    db = SessionLocal()

    data = db.query(Candidate).all()

    result = []

    for c in data:
        result.append({
            "name": c.name,
            "score": c.score,
            "cgpa": c.cgpa,
            "skills": c.skills.split(",") if c.skills else [],
            "projects": c.projects,
            "certifications": c.certifications,
            "resume": c.resume_path
        })

    db.close()

    return result