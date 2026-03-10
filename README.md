# food-image-analyzer

AI-powered food image analyzer that extracts ingredients and nutritional information from food images using **LangGraph** (orchestration), **LangChain** / OpenAI Vision, and **LangSmith** (evaluation and tracing).

## Overview

This application provides:

- 🍽️ **Ingredient Detection**: Analyze food images to identify ingredients and their quantities
- 📊 **Nutritional Analysis**: Calculate detailed nutritional information (calories, fat, protein)
- 🔀 **LangGraph Workflow**: A stateful pipeline that runs ingredient analysis → nutrient analysis in sequence
- 🚀 **FastAPI REST API**: Modern, fast API with a single `/food-analysis` endpoint
- 🔄 **Redis Caching**: Cache analysis results for improved performance
- 🗄️ **MongoDB Storage**: Persist analysis results and user data
- 📡 **LangSmith**: Optional tracing and evaluation with LangSmith datasets
- 🔍 **Smart Environment Loading**: Automatic `.env` file discovery with parent directory traversal

### How It Works

1. **Provide a food image URL** via the API.
2. **LangGraph pipeline** runs two nodes in order:
   - **analyze_ingredients**: Encodes the image, (optionally) checks Redis cache, then uses a LangChain/OpenAI vision model with structured output to detect ingredients.
   - **analyze_nutrients**: Uses the same LLM with structured output to compute nutrients from those ingredients (with optional caching).
3. **Structured response**: Returns JSON with ingredients, quantities, and nutrients. Results can be traced in **LangSmith** when configured.

## Prerequisites

- Python 3.12 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- LangSmith API key ([Get one here](https://smith.langchain.com/)) — optional; used for tracing and running evaluations
- Redis server (optional, for caching)
- MongoDB server (optional, for persistence)
- `uv` package manager (recommended)

## Getting Started

### 1. Install `uv` Package Manager

```bash
# macOS/Linux
brew install uv
```

After installation, restart your terminal.

### 2. Install Python Version 3.12.0

```bash
# Installing python and creating virtual environment at: `.venv/`
uv venv --python 3.12.0
```

### 3. Initialize project and install dependencies and dev dependencies

```bash
uv init
```

Install all project dependencies (includes both runtime and dev dependencies):

```bash
# This installs packages from `pyproject.toml`
uv sync
```

**Note:** If you need to add new dependencies later:

```bash
# Add runtime dependency
uv add package-name

# Add dev dependency
uv add --dev package-name
```

When using Docker Compose, set `REDIS_HOST=redis` and `MONGODB_HOST=mongodb` in `.env` (service names). When running on the host, keep `REDIS_HOST=localhost` and `MONGODB_HOST=localhost`.

### 4. Run Redis (Optional)

If you want to enable caching, start a Redis server:

```bash
# Using Docker
docker run --rm -d -p 6379:6379 redis:latest

# Or using Homebrew (macOS)
brew services start redis
```

### 5. Run the Application

#### FastAPI Server

Start the FastAPI development server:

```bash
cd src
PYTHONPATH=. uv run fastapi dev api/app.py
```

The API will be available at `http://localhost:8000`

#### Docker

**Build the image:**

```bash
docker build -t food-image-analyzer .
```

**Run the container:**

```bash
docker run --rm -p 8000:8000 --env-file .env food-image-analyzer
```

#### Docker Compose

The compose file runs the API, Redis, and MongoDB together. Make sure your `.env` is present
before starting the stack.

```bash
# Build and start the stack
docker compose up --build -d

# Stop and remove containers
docker compose down

# Follow logs (service names: food-image-analyzer, redis, mongodb)
docker compose logs -f food-image-analyzer
```

## API Endpoints

| Method | Endpoint         | Description                                                            |
| ------ | ---------------- | ---------------------------------------------------------------------- |
| `GET`  | `/`              | Welcome message                                                        |
| `GET`  | `/health`        | Health check endpoint                                                  |
| `POST` | `/food-analysis` | Full pipeline: analyze image → extract ingredients → compute nutrients |

### POST `/food-analysis`

Runs the full **LangGraph** pipeline: ingredient detection from the image, then nutrient calculation from those ingredients. Returns both in one response.

**Request Body:**

```json
{
  "image_url": "https://example.com/food-image.jpg"
}
```

**Response:**

```json
{
  "status": "successful",
  "processed_at": "2026-01-12T10:30:00Z",
  "request": {
    "image_url": "https://example.com/food-image.jpg"
  },
  "ingredients_response": {
    "name": "Caesar Salad",
    "ingredients": [
      { "ingredient_name": "Romaine lettuce", "portion": "2 cups" },
      { "ingredient_name": "Parmesan cheese", "portion": "30g" },
      { "ingredient_name": "Croutons", "portion": "1/2 cup" }
    ]
  },
  "nutrients_response": {
    "total_calories": 250,
    "total_protein_g": 12.5,
    "total_carbohydrates_g": 15.0,
    "total_fats_g": 18.0,
    "total_fiber_g": 3.5
  },
  "error": null
}
```

**Interactive API Documentation:**

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### Command Line Application

```bash
uv run python main.py
```

Alternatively, activate the virtual environment first:

```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Then run
python main.py
```

**Note:** To exit the application, type `exit` or `quit`.

### Setting PYTHONPATH

If you need to run Python modules directly or have import issues, you may need to set the `PYTHONPATH` to include the project root.

**macOS/Linux (bash/zsh):**

```bash
# run with PYTHONPATH inline
PYTHONPATH=. python main.py
```

To make it permanent, add to your `~/.zshrc` or `~/.bashrc`:

```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/food-image-analyzer"
```

**Windows (PowerShell):**

```powershell
# run with PYTHONPATH inline
$env:PYTHONPATH = "."; python main.py
```

## Project Structure

```
food-image-analyzer-langgraph/
├── .env                    # Environment variables (create from .env.example)
├── .env.example            # Example: OpenAI, LangSmith, Redis, MongoDB
├── .github/
│   └── workflows/
│       └── tests.yml       # CI/CD test workflow
├── .gitignore
├── .python-version
├── Dockerfile
├── docker-compose.yml      # API + Redis + MongoDB
├── LICENSE
├── Makefile                # Ruff lint/format, clean
├── pyproject.toml
├── README.md
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── app.py          # FastAPI app, /food-analysis endpoint
│   │   └── schemas.py      # Request/response Pydantic models
│   ├── evaluation/         # LangSmith-based evaluation
│   │   ├── eval_dataset.py # Run model on LangSmith dataset, score results
│   │   ├── llm_judging.py  # LLM-as-judge for ingredient quality
│   │   ├── run_evaluation.py  # Entry: load dataset, run eval
│   │   ├── schema.py       # Evaluation data shapes
│   │   └── scoring.py      # Nutrient scoring (e.g. MAE)
│   ├── services/
│   │   ├── cache/          # Redis caching
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   └── config.py
│   │   ├── database/       # MongoDB persistence
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   └── config.py
│   │   ├── image_processing.py  # Base64 image encoding
│   │   ├── llm/            # LangGraph + LangChain food pipeline
│   │   │   ├── config.py   # Model name, temperature
│   │   │   ├── food_llm.py # StateGraph: analyze_ingredients → analyze_nutrients
│   │   │   └── schemas.py  # IngredientsResponse, NutrientsResponse
│   │   └── prompts.py      # System/user prompts for ingredients & nutrients
│   └── tests/              # Pytest suite (conftest, api, services)
│       ├── conftest.py
│       ├── api/
│       │   └── test_app.py
│       └── services/
│           └── llm/
│               └── test_food_llm.py
└── uv.lock
```

### Key Components

| Component                | Path                               | Description                                                                                |
| ------------------------ | ---------------------------------- | ------------------------------------------------------------------------------------------ |
| **API Layer**            | `src/api/`                         | FastAPI app; `/food-analysis` runs the full LangGraph pipeline                             |
| **LangGraph Pipeline**   | `src/services/llm/food_llm.py`     | StateGraph: ingredients → nutrients; LangChain + OpenAI structured output                  |
| **LLM Config & Schemas** | `src/services/llm/`                | Model config and Pydantic schemas for structured LLM output                                |
| **LangSmith Evaluation** | `src/evaluation/`                  | Load datasets from LangSmith, run FoodLLM, score with LLM judge & metrics                  |
| **Redis Cache**          | `src/services/cache/`              | Cache ingredient and nutrient results                                                      |
| **MongoDB**              | `src/services/database/`           | Persist analysis results                                                                   |
| **Image Processing**     | `src/services/image_processing.py` | Base64 encoding for image URLs                                                             |
| **Prompts**              | `src/services/prompts.py`          | Prompts for ingredient and nutrient analysis                                               |
| **Tests**                | `src/tests/`                       | Pytest suite: API (`api/`), LangGraph pipeline (`services/llm/`), fixtures (`conftest.py`) |

## Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for fast Python linting and formatting.

### Running Ruff

**Check for linting issues:**

```bash
uv run ruff check ./src/
```

**Auto-fix linting issues:**

```bash
uv run ruff check --fix ./src/
```

**Format code:**

```bash
uv run ruff format ./src/
```

**Check formatting (without making changes):**

```bash
uv run ruff format --check ./src/
```

### Recommended Workflow

Before committing code, run (or use `make ruff_lint` and `make ruff_format`):

```bash
uv run ruff check --fix ./src/      # Fix linting violations
uv run ruff format ./src/          # Format code
uv run ruff check --select I --fix ./src/  # Sort imports
```

## Running Tests

This project uses [pytest](https://docs.pytest.org/) for testing. The suite lives under `src/tests/` and mirrors the source layout; `pyproject.toml` sets `pythonpath = ["src"]` and `testpaths = ["tests"]`, so from the project root you can run:

| Directory / file          | What it tests                        |
| ------------------------- | ------------------------------------ |
| `src/tests/conftest.py`   | Shared fixtures (e.g. for API / LLM) |
| `src/tests/api/`          | FastAPI app and `/food-analysis`     |
| `src/tests/services/llm/` | LangGraph pipeline (food_llm)        |

### Run all tests

```bash
uv run pytest src/tests
```

### Verbose output

```bash
uv run pytest src/tests -v
```

### Single file or path

```bash
uv run pytest src/tests/api/test_app.py
uv run pytest src/tests/services/llm/
```

### With coverage

```bash
uv run pytest src/tests --cov=src
```

## CI/CD

This project uses GitHub Actions for continuous integration. Tests are automatically run on:

- Push to `main` branch
- Pull requests to `main` branch

See `.github/workflows/tests.yml` for the workflow configuration.

## LangGraph and LangSmith

- **LangGraph** ([docs](https://langchain-ai.github.io/langgraph/)): The analysis pipeline is implemented as a compiled `StateGraph` in `src/services/llm/food_llm.py`. The graph has two nodes—`analyze_ingredients` and `analyze_nutrients`—that run in sequence. State (image URL, ingredient result, nutrient result) is passed between nodes; the chain is invoked with an image URL and returns both responses.
- **LangSmith** ([docs](https://docs.smith.langchain.com/)): Used for:
  - **Tracing**: Set `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY` (and optionally `LANGSMITH_PROJECT`) in `.env` to trace runs in the LangSmith UI.
  - **Evaluation**: The `src/evaluation/` module uses the LangSmith client to load a dataset (e.g. `food-image-analyzer`), run the `FoodLLM` pipeline on each example, and score outputs (LLM-as-judge for ingredients, numeric metrics for nutrients). Create a dataset in [LangSmith](https://smith.langchain.com/) with inputs (e.g. `img_url`) and expected outputs (e.g. `ingredients`, `carbohydrates`, `protein`, `fat`, `total_calories`) to run evaluations.

## Dependencies

### Runtime Dependencies

| Package             | Description                                       |
| ------------------- | ------------------------------------------------- |
| `fastapi[standard]` | Web framework for the API                         |
| `langchain`         | LangChain core                                    |
| `langchain-openai`  | OpenAI integration for LangChain                  |
| `langgraph`         | Stateful graph workflow (ingredients → nutrients) |
| `langsmith`         | Tracing and dataset client for evaluation         |
| `openai`            | OpenAI Python SDK                                 |
| `pymongo`           | MongoDB client                                    |
| `redis`             | Redis client for caching                          |
| `requests`          | HTTP library for image fetching                   |

### Development Dependencies

| Package  | Description                      |
| -------- | -------------------------------- |
| `loguru` | Logging library                  |
| `ruff`   | Fast Python linter and formatter |
| `pytest` | Testing framework                |

## LLM Evaluation

### What is LLM Evaluation?

| Concept        | Meaning                                         |
| -------------- | ----------------------------------------------- |
| LLM Evaluation | Measuring AI output quality in a repeatable way |
| Metric         | A test that checks one aspect of output quality |
| Ground Truth   | The "correct" reference answer (when available) |

> 🧠 **Mental model:** Metrics = automated tests for AI outputs

### Types of Evaluation Metrics

#### A) Heuristic Metrics (Rule-based)

| Property      | Description                  |
| ------------- | ---------------------------- |
| Deterministic | Same input → same result     |
| Rule-based    | Uses strings, regex, schemas |
| Fast & cheap  | No LLM needed                |
| Limitation    | Cannot judge meaning         |

**Examples:**

- `IsJson`
- Structured Output Compliance
- `RegexMatch`
- `Contains` / `Equals`

> 🧠 **Analogy:** Jest / TypeScript checks

#### B) LLM-as-a-Judge Metrics (Semantic)

| Property         | Description                 |
| ---------------- | --------------------------- |
| Uses another LLM | LLM reviews LLM output      |
| Semantic         | Understands meaning         |
| Human-like       | Similar to code review      |
| Limitation       | Not perfectly deterministic |

**Examples:**

- **Hallucination** — Did the model make things up?
- **Context Precision** — Did it use the given context correctly?
- **Context Recall** — Did it cover all the important context?
- **Usefulness** — Is the answer actually helpful?
- **Relevance** — Does it answer what was asked?

> 🧠 **Analogy:** Senior engineer review

### Classification Outcomes (YES / NO Decisions)

| Term                | Meaning           | Food App Example           |
| ------------------- | ----------------- | -------------------------- |
| True Positive (TP)  | Said YES, correct | Correctly detected peanuts |
| False Positive (FP) | Said YES, wrong   | Hallucinated ingredient    |
| True Negative (TN)  | Said NO, correct  | Correctly no peanuts       |
| False Negative (FN) | Said NO, wrong    | Missed allergen            |

> 🧠 **Rule:**
>
> - Positive / Negative → what model says
> - True / False → correctness

### Core Classification Metrics (Trust vs Coverage)

#### Precision (Hallucination Control)

| Aspect         | Meaning                    |
| -------------- | -------------------------- |
| Focus          | False Positives            |
| Question       | "Can I trust YES answers?" |
| High precision | Few hallucinations         |

**Formula:**

$$\text{Precision} = \frac{TP}{TP + FP}$$

> 🧠 **Precision** = Don't make things up

#### Recall (Miss Control)

| Aspect      | Meaning                       |
| ----------- | ----------------------------- |
| Focus       | False Negatives               |
| Question    | "Did I catch all real cases?" |
| High recall | Few misses                    |

**Formula:**

$$\text{Recall} = \frac{TP}{TP + FN}$$

> 🧠 **Recall** = Don't miss real things

### Numeric Error Metrics (Regression)

Used when output is a number, not YES/NO.

#### MAE — Mean Absolute Error

| Property              | Description                |
| --------------------- | -------------------------- |
| Treats errors equally | 20 off = 50 off (linearly) |
| Easy to explain       | Average mistake size       |

**Formula:**

$$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$$

> 📌 Calories off by ~30 kcal

#### RMSE — Root Mean Squared Error

| Property             | Description              |
| -------------------- | ------------------------ |
| Penalizes big errors | Large mistakes hurt more |
| Safety-oriented      | Good for health data     |

**Formula:**

$$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$$

> 📌 Predicting 1200 instead of 500 is punished hard

### Mapping to Your Food App

| Goal                 | Metric Type              |
| -------------------- | ------------------------ |
| App doesn't crash    | IsJson, Schema           |
| No fake ingredients  | Precision, Hallucination |
| Don't miss allergens | Recall                   |
| Reasonable calories  | MAE / RMSE               |
| Trustworthy answers  | Usefulness               |

## Run evaluation

Evaluation uses **LangSmith** to load a dataset and score the pipeline (ingredient quality via LLM judge, nutrient metrics). Set `LANGSMITH_API_KEY` (and optionally `LANGSMITH_TRACING`, `LANGSMITH_PROJECT`) in `.env`. Create a dataset named `food-image-analyzer` (or change `dataset_name` in `run_evaluation.py`) with the expected input/output fields used in `eval_dataset.py`.

From the project root:

**Local:**

```bash
cd src && uv run python -m evaluation.run_evaluation
```

**With Docker Compose** (start stack first, then run eval in a container or on the host with network access to any required services):

```bash
docker compose up --build -d
cd src && uv run python -m evaluation.run_evaluation
```

## License

See [LICENSE](LICENSE) for details.
