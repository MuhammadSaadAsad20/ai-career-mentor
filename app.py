from fastapi import HTTPException
from interview_engine import determine_level, determine_difficulty
from ai_service import generate_interview_questions
from database import Question
from pydantic import BaseModel, Field
from database import SessionLocal, Interview
from fastapi import FastAPI

app = FastAPI(
    title="AI Career Mentor",
    description="AI-powered interview and career coaching API",
    version="1.0.0"
)

class InterviewRequest(BaseModel):
    candidate_name: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=100)
    experience: int = Field(ge=0, le=50)


@app.get("/")
def home():
    return {
        "message": "AI Career Mentor API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/interviews")
def get_interviews():
    db = SessionLocal()

    try:
        interviews = (
            db.query(Interview)
            .order_by(Interview.id.desc())
            .all()
        )

        return [
            {
                "id": interview.id,
                "candidate_name": interview.candidate_name,
                "role": interview.role,
                "experience": interview.experience,
                "level": interview.level,
                "difficulty": interview.difficulty,
                "overall_score": interview.overall_score,
                "created_at": interview.created_at,
            }
            for interview in interviews
        ]

    finally:
        db.close()


@app.get("/interviews/{interview_id}")
def get_interview_details(interview_id: int):
    db = SessionLocal()

    try:
        interview = db.get(Interview, interview_id)

        if interview is None:
            from fastapi import HTTPException

            raise HTTPException(
                status_code=404,
                detail="Interview not found"
            )

        return {
            "id": interview.id,
            "candidate_name": interview.candidate_name,
            "role": interview.role,
            "experience": interview.experience,
            "level": interview.level,
            "difficulty": interview.difficulty,
            "overall_score": interview.overall_score,
            "created_at": interview.created_at,
            "questions": [
                {
                    "question_number": question.question_number,
                    "question_text": question.question_text,
                    "answer": (
                        {
                            "answer_text": question.answer.answer_text,
                            "score": question.answer.score,
                            "technical_correctness": question.answer.technical_correctness,
                            "relevance": question.answer.relevance,
                            "completeness": question.answer.completeness,
                            "strengths": question.answer.strengths,
                            "improvements": question.answer.improvements,
                            "better_answer": question.answer.better_answer,
                        }
                        if question.answer else None
                    ),
                }
                for question in interview.questions
            ],
        }

    finally:
        db.close()



@app.post("/interviews")
def create_interview(request: InterviewRequest):
    db = SessionLocal()

    try:
        # Determine the candidate's level
        level = determine_level(request.experience)
        difficulty = determine_difficulty(level)

        # Generate questions using your existing AI service
        try:
            result = generate_interview_questions(
                request.role,
                level
            )
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="Unable to generate interview questions."
            ) from exc

        # Save the interview record
        interview = Interview(
            candidate_name=request.candidate_name.strip(),
            role=request.role.strip(),
            experience=request.experience,
            level=level,
            difficulty=difficulty,
            overall_score=0.0
        )

        db.add(interview)
        db.flush()

        # Save the generated questions
        saved_questions = []

        for number, question_text in enumerate(
            result.questions, start=1
        ):
            question = Question(
                interview_id=interview.id,
                question_number=number,
                question_text=question_text
            )

            db.add(question)

            saved_questions.append({
                "question_number": number,
                "question_text": question_text
            })

        db.commit()
        db.refresh(interview)

        return {
            "message": "Interview created successfully.",
            "interview_id": interview.id,
            "candidate_name": interview.candidate_name,
            "role": interview.role,
            "level": interview.level,
            "difficulty": interview.difficulty,
            "overall_score": interview.overall_score,
            "questions": saved_questions
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to save the interview."
        ) from exc

    finally:
        db.close()

