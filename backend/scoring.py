def calculate_score(cgpa, project_data, cert_count, skill_count):

    cgpa_score = cgpa * 2.5

    project_score = (
        project_data["major"] * 15 +
        project_data["research"] * 20 +
        project_data["internship"] * 10 +
        project_data["minor"] * 5
    )

    cert_score = cert_count * 3
    skill_score = skill_count * 2

    total_score = cgpa_score + project_score + cert_score + skill_score

    return round(total_score, 2)