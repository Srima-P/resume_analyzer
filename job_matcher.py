def calculate_skill_match(candidate_skills, required_skills):

    candidate_set = set(s.lower() for s in candidate_skills)
    required_set = set(s.lower() for s in required_skills)

    matched = candidate_set & required_set

    if not required_set:
        return 0, []

    percent = (len(matched) / len(required_set)) * 100

    return round(percent, 2), list(matched)