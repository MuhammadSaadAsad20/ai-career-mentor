# AI Career Mentor

[![CI](https://github.com/MuhammadSaadAsad20/ai-career-mentor/actions/workflows/ci.yml/badge.svg)](https://github.com/MuhammadSaadAsad20/ai-career-mentor/actions/workflows/ci.yml)

**Status: under construction.** The text interview loop works today. Speech and resume features
are planned and not built.

A mock-interview engine. It generates role-appropriate questions with an LLM, scores each typed
answer against a fixed rubric, and returns structured feedback.

## What works today

- Maps years of experience to a level and question difficulty.
- Generates five questions for the role and level.
- In the CLI, scores each answer and returns a validated `AnswerEvaluation`:

  | Field | Type | Meaning |
  |---|---|---|
  | `score` | 0 to 10 | Overall score |
  | `technical_correctness` | 0 to 10 | Is the content right |
  | `relevance` | 0 to 10 | Does it answer the question asked |
  | `completeness` | 0 to 10 | Did it cover what it should |
  | `strengths` | list | What the candidate did well |
  | `improvements` | list | Specific fixes |
  | `better_answer` | string | A model answer to compare against |

- Saves interviews, questions and scored answers to SQLite.

## Two entry points

- **`main.py`:** the interactive CLI, and the only path that scores answers today.
- **`app.py`:** a FastAPI service that creates interviews, generates questions and reads saved
  interviews. It does not score answers yet.

## Design notes

Question generation and evaluation both bind the model's response to a Pydantic schema, so a
malformed response fails at the boundary. Score fields are bounded with `Field(ge=0, le=10)`, and
API input is validated before any LLM call is made.

## Run it

Requires Python 3.11 or newer and an OpenAI API key.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Add your key to `.env`, then run `python main.py` or `uvicorn app:app --reload`.

## Tests

```bash
pip install pytest httpx
python -m pytest tests -q
```

The tests cover level mapping, rubric validation and API input validation, with no API key or
network calls. CI runs them on every push.

## Roadmap

1. Expose answer scoring through the API.
2. Whisper transcription for spoken answers, then delivery metrics such as pace and filler words.
3. Resume and job-description tailoring.
4. A report that tracks scores across interviews.
