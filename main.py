from interview_engine import (
    determine_level,
    determine_difficulty,
    get_skills
)

from ai_service import (
    generate_interview_questions,
    evaluate_answer
)

from database import (
    SessionLocal,
    Interview,
    Question,
    Answer
)


# =========================
# DATABASE SESSION
# =========================

db = SessionLocal()


# =========================
# START PROGRAM
# =========================

print("================================")
print("       AI CAREER MENTOR")
print("================================")

name = input("What is your name? ")
role = input("What job are you preparing for? ")
experience = int(input("How many years of experience do you have? "))

level = determine_level(experience)
difficulty = determine_difficulty(level)


# =========================
# CANDIDATE INFORMATION
# =========================

print()
print("========== CANDIDATE ==========")
print("Name:", name)
print("Target Role:", role)
print("Experience:", experience, "years")
print("Candidate Level:", level)
print("Interview Difficulty:", difficulty)


# =========================
# REQUIRED SKILLS
# =========================

skills = get_skills()

print()
print("========== REQUIRED SKILLS ==========")

for skill in skills:
    print(f"- {skill}")


# =========================
# GENERATE INTERVIEW
# =========================

print()
print("========== GENERATING INTERVIEW ==========")

questions = generate_interview_questions(
    role,
    level
)


# =========================
# CONDUCT INTERVIEW
# =========================

print()
print("========== INTERVIEW ==========")

answers = []
evaluations = []

for number, question in enumerate(
    questions.questions,
    start=1
):

    print(f"\nQuestion {number}: {question}")

    answer = input("Your answer: ")

    answers.append(answer)

    feedback = evaluate_answer(
        question,
        answer,
        role
    )

    evaluations.append(feedback)

    print("\n========== AI FEEDBACK ==========")

    print("Overall Score:", feedback.score)
    print(
        "Technical Correctness:",
        feedback.technical_correctness
    )
    print("Relevance:", feedback.relevance)
    print("Completeness:", feedback.completeness)

    print("\nStrengths:")

    for strength in feedback.strengths:
        print("-", strength)

    print("\nImprovements:")

    for improvement in feedback.improvements:
        print("-", improvement)

    print("\nBetter Answer:")
    print(feedback.better_answer)


# =========================
# FINAL INTERVIEW RESULT
# =========================

if evaluations:

    overall_score = sum(
        evaluation.score
        for evaluation in evaluations
    ) / len(evaluations)

    technical_score = sum(
        evaluation.technical_correctness
        for evaluation in evaluations
    ) / len(evaluations)

    relevance_score = sum(
        evaluation.relevance
        for evaluation in evaluations
    ) / len(evaluations)

    completeness_score = sum(
        evaluation.completeness
        for evaluation in evaluations
    ) / len(evaluations)


    print()
    print("================================")
    print("       FINAL INTERVIEW RESULT")
    print("================================")

    print(f"Candidate: {name}")
    print(f"Role: {role}")
    print(f"Level: {level}")

    print()
    print(f"Overall Score: {overall_score:.1f}/10")
    print(
        f"Technical Correctness: "
        f"{technical_score:.1f}/10"
    )
    print(
        f"Relevance: "
        f"{relevance_score:.1f}/10"
    )
    print(
        f"Completeness: "
        f"{completeness_score:.1f}/10"
    )


    # =========================
    # SAVE INTERVIEW
    # =========================

    interview_record = Interview(
        candidate_name=name,
        role=role,
        experience=experience,
        level=level,
        difficulty=difficulty,
        overall_score=overall_score
    )

    db.add(interview_record)

    db.commit()

    db.refresh(interview_record)


    # =========================
    # SAVE QUESTIONS + ANSWERS
    # =========================

    for number, (question_text, answer_text, evaluation) in enumerate(
        zip(
            questions.questions,
            answers,
            evaluations
        ),
        start=1
    ):

        question_record = Question(
            interview_id=interview_record.id,
            question_number=number,
            question_text=question_text
        )

        db.add(question_record)

        db.flush()


        answer_record = Answer(
            question_id=question_record.id,
            answer_text=answer_text,
            score=evaluation.score,
            technical_correctness=evaluation.technical_correctness,
            relevance=evaluation.relevance,
            completeness=evaluation.completeness,
            strengths="\n".join(evaluation.strengths),
            improvements="\n".join(evaluation.improvements),
            better_answer=evaluation.better_answer
        )

        db.add(answer_record)


    db.commit()

interview_id = interview_record.id

db.close()


print()
print("================================")
print("       INTERVIEW SAVED")
print("================================")

print("Interview ID:", interview_id)

print()
print("================================")
print("       INTERVIEW COMPLETE")
print("================================")