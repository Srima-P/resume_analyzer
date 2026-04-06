import pdfplumber
import re


def extract_text(file_path):

    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text.lower()


def extract_cgpa(text):

    match = re.search(r"\b\d\.\d{1,2}\b", text)

    return float(match.group()) if match else 0


def extract_skills(text):

    skills = [
        "python","java","c++","machine learning",
        "sql","javascript","html","css","react"
    ]

    return [s for s in skills if s in text]


def extract_certifications(text):

    words = ["certification","certificate","coursera","udemy"]

    return sum(text.count(w) for w in words)


def extract_project_weights(text):

    major = sum(1 for line in text.split("\n") if "project" in line)

    internship = 1 if "internship" in text else 0
    research = 1 if "research" in text else 0
    minor = 1 if "mini project" in text else 0

    return {
        "major": major,
        "research": research,
        "internship": internship,
        "minor": minor
    }