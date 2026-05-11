from flask import Blueprint, jsonify, request

from services.matching import calculate_match_score


match_score_bp = Blueprint("match_score", __name__, url_prefix="/api")


@match_score_bp.post("/match-score")
def match_score():
    payload = request.get_json(silent=True) or {}
    score, matched_skills = calculate_match_score(
        payload.get("student_skills") or "",
        payload.get("job_description") or "",
    )
    return jsonify({"match_score": score, "matched_skills": matched_skills})
