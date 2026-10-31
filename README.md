# AI Career Mentor

A mock-interview engine that generates role-appropriate questions with an LLM,
then scores each spoken-or-typed answer against a fixed rubric and returns
structured, specific feedback — not a paragraph of encouragement.

The scoring is the point. Every evaluation comes back as a validated Pydantic
model with four numeric sub-scores, a list of strengths, a list of concrete
improvements, and a rewritten model answer. Nothing is parsed out of prose.

## What it does

1. Takes a candidate's name, target role, and years of experience.
2. Maps experience to a level (Beginner / Intermediate / Advanced) and a question
   difficulty (Basic / Medium / Hard).
3. Asks the LLM for five interview questions calibrated to that role and level.
4. For each answer, returns a structured evaluation:

   | Field | Type | Meaning |
   |---|---|---|
   | `score` | 0–10 | Overall |
   | `technical_correctness` | 0–10 | Is the content right |
   | `relevance` | 0–10 | Does it answer the question asked |
   | `completeness` | 0–10 | Did it cover what it should |
   | `strengths` | list | What the candidate did well |
   | `improvements` | list | Specific, actionable fixes |
   | `better_answer` | string | A model answer to compare against |

5. Persists the interview, its questions, and every answer with its scores to
   SQLite, so sessions can be reviewed later.

## Two front ends

- **`main.py`** — an interactive CLI. Runs a full interview in the terminal.
- **`app.py`** — a FastAPI service over the same engine.

  | Method | Route | Purpose |
  |---|---|---|
  | `GET` | `/health` | Liveness check |
  | `GET` | `/interviews` | List past interviews, newest first |
  | `GET` | `/interviews/{id}` | One interview with its questions |
  | `POST` | `/interviews` | Start an interview and generate questions |

## Design notes

**Structured output over prose parsing.** `generate_interview_questions` and
`evaluate_answer` both bind the LLM response to a Pydantic schema. A malformed
or hallucinated shape fails validation at the boundary instead of silently
producing a half-parsed score downstream.

**Bounded fields.** `score` and the three sub-scores are `Field(ge=0, le=10)`;
request input is bounded too (`experience` is `ge=0, le=50`). The model cannot
hand back an 11 or a negative year count.

**The rubric lives in the schema, not the prompt.** Adding a scoring dimension
means adding a field, which forces the model to produce it.

## Running it

Requires Python 3.11+ and an OpenAI API key.

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install fastapi uvicorn openai sqlalchemy pydantic python-dotenv
```

Put your key in `.env`:

```
OPENAI_API_KEY=sk-your-key-here
```

CLI:

```bash
python main.py
```

API:

```bash
uvicorn app:app --reload
```

Then open <http://127.0.0.1:8000/docs>.

## Current limits

Stated plainly, because they are the roadmap:

- **Text answers only.** There is no speech input, no transcription, and no
  delivery analysis (pace, pauses, filler words) yet.
- **Questions key off role and experience only.** Resume and job-description
  tailoring is not implemented.
- **No scoring endpoint on the API.** Answer evaluation currently runs through
  the CLI path; `POST /interviews` generates questions but does not yet accept
  and score answers.
- **Single user, single machine.** SQLite, no accounts, no auth.

## Where it goes next

In order of value:

1. Expose answer scoring over the API so the CLI and service are at parity.
2. Whisper transcription for spoken answers, then delivery metrics derived from
   the transcript and its timings — speaking pace, pause length, filler-word rate.
3. Resume and job-description parsing, so questions target the actual gap
   between a candidate and a specific posting.
4. A session report that trends scores across repeated interviews.
