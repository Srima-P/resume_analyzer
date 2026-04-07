from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./candidates.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    score = Column(Integer)
    cgpa = Column(String)
    skills = Column(String)
    projects = Column(String)
    certifications = Column(Integer)
    resume_path = Column(String)


def create_database():
    Base.metadata.create_all(bind=engine)