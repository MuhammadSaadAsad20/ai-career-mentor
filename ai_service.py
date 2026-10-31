import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


# =========================
# STRUCTURED OUTPUT MODELS
# =========================

class InterviewQuestions(BaseModel):
    questions: list[str]


class AnswerEvaluation(BaseModel):
    score: int = Field(ge=0, le=10)
    technical_correctness: int = Field(ge=0, le=10)
    relevance: int = Field(ge=0, le=10)
    completeness: int = Field(ge=0, le=10)
    strengths: list[str]
    improvements: list[str]
    better_answer: str


# =========================
# QUESTION GENERATION
# =========================

def generate_interview_questions(role, experience):

    prompt = f"""
You are an expert technical interviewer.

Generate exactly 5 interview questions for a candidate applying for:

Role: {role}
Experience Level: {experience}

Rules:
- Questions must match the candidate's experience level.
- Questions should be relevant to the target role.
- Do not include answers.
- Generate exactly 5 questions.
"""

    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=prompt,
        text_format=InterviewQuestions
    )

    return response.output_parsed


# =========================
# ANSWER EVALUATION
# =========================

def evaluate_answer(question, answer, role):

    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer.

Target Role:
{role}

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate using these criteria:

1. Technical correctness
2. Relevance to the question
3. Completeness

Scoring:
- Each criterion must be from 0 to 10.
- Overall score must be from 0 to 10.
- Do not give credit for incorrect technical claims.
- Keep feedback useful for interview preparation.

Provide:
- Overall score
- Technical correctness score
- Relevance score
- Completeness score
- Strengths
- Areas for improvement
- A better example answer
"""

    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=prompt,
        text_format=AnswerEvaluation
    )

    return response.output_parsed



if __name__ == "__main__":

    question = "What is the difference between a list and a tuple in Python?"

    answer = """
    A list can be modified after creation,
    while a tuple cannot be modified.
    """

    result = evaluate_answer(
        question,
        answer,
        "Python Developer"
    )

    print("========== AI EVALUATION ==========")
    print("Overall Score:", result.score)
    print("Technical Correctness:", result.technical_correctness)
    print("Relevance:", result.relevance)
    print("Completeness:", result.completeness)

    print("\nStrengths:")
    for strength in result.strengths:
        print("-", strength)

    print("\nImprovements:")
    for improvement in result.improvements:
        print("-", improvement)

    print("\nBetter Answer:")
    print(result.better_answer)