import os

os.environ.setdefault("OPENAI_API_KEY", "not-used-by-these-tests")

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from ai_service import AnswerEvaluation
from app import app
from interview_engine import determine_difficulty, determine_level

client = TestClient(app)


@pytest.mark.parametrize("years,level,difficulty", [
    (0, "Beginner", "Basic"),
    (1, "Beginner", "Basic"),
    (2, "Intermediate", "Medium"),
    (4, "Intermediate", "Medium"),
    (5, "Advanced", "Hard"),
])
def test_experience_maps_to_level_and_difficulty(years, level, difficulty):
    assert determine_level(years) == level
    assert determine_difficulty(level) == difficulty


def evaluation(**overrides):
    fields = dict(
        score=7, technical_correctness=8, relevance=7, completeness=6,
        strengths=["clear"], improvements=["add an example"], better_answer="...",
    )
    return AnswerEvaluation(**(fields | overrides))


def test_rubric_accepts_scores_in_range():
    assert evaluation().score == 7


@pytest.mark.parametrize("field,value", [("score", 11), ("relevance", -1)])
def test_rubric_rejects_scores_out_of_range(field, value):
    with pytest.raises(ValidationError):
        evaluation(**{field: value})


def test_health_endpoint():
    assert client.get("/health").json() == {"status": "healthy"}


@pytest.mark.parametrize("payload", [
    {"candidate_name": "", "role": "Engineer", "experience": 1},
    {"candidate_name": "A", "role": "Engineer", "experience": 51},
])
def test_invalid_interview_requests_are_rejected_before_any_llm_call(payload):
    assert client.post("/interviews", json=payload).status_code == 422
