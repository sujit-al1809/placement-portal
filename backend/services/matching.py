import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").lower()).strip()


def parse_skills(skills_text: str):
    pieces = re.split(r"[,;/|\n]", skills_text or "")
    cleaned = []
    seen = set()
    for piece in pieces:
        skill = _normalize_text(piece)
        if skill and skill not in seen:
            cleaned.append(skill)
            seen.add(skill)
    return cleaned


def calculate_match_score(student_skills: str, job_description: str):
    skills = parse_skills(student_skills)
    skills_text = " ".join(skills)
    job_text = _normalize_text(job_description)

    if not skills_text or not job_text:
        return 0.0, []

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform([skills_text, job_text])
    score = float(cosine_similarity(matrix[0], matrix[1])[0][0] * 100)

    matched_skills = [skill for skill in skills if skill in job_text]
    if not matched_skills:
        matched_skills = [skill for skill in skills if any(token in job_text for token in skill.split())]

    return round(score, 1), matched_skills
