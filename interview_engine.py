def determine_level(experience):
    if experience <= 1:
        return "Beginner"
    elif experience <= 4:
        return "Intermediate"
    else:
        return "Advanced"


def determine_difficulty(level):
    if level == "Beginner":
        return "Basic"
    elif level == "Intermediate":
        return "Medium"
    else:
        return "Hard"


def get_questions():
    questions = [
        "What is Python and why is it commonly used in AI?",
        "What is an API?",
        "What is machine learning?",
        "What is FastAPI?",
        "What is the difference between AI and machine learning?"
    ]

    return questions


def get_skills():
    return [
        "Python",
        "SQL",
        "Git",
        "FastAPI",
        "Machine Learning"
    ]