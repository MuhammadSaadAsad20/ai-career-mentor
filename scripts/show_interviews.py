import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from database import SessionLocal, Interview

db = SessionLocal()

interviews = db.query(Interview).order_by(Interview.id.asc()).all()

print("\n========== ALL SAVED INTERVIEWS ==========")

for interview in interviews:
    print("\n--------------------------------")
    print("ID:", interview.id)
    print("Candidate:", interview.candidate_name)
    print("Role:", interview.role)
    print("Score:", interview.overall_score)
    print("Questions saved:", len(interview.questions))

    for question in interview.questions:
        print(f"  Q{question.question_number}: {question.question_text}")

        if question.answer:
            print("  Answer:", question.answer.answer_text[:100])
            print("  Score:", question.answer.score)
        else:
            print("  No answer saved")

db.close()