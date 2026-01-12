# food-image-analyzer

AI-powered food image analyzer that analyzes food images to extract ingredients and nutritional information using OpenAI's Vision API.

## Overview

This application provides:

- 🍽️ **Ingredient Detection**: Analyze food images to identify ingredients and their quantities
- 📊 **Nutritional Analysis**: Calculate detailed nutritional information (calories, macros, fiber)
- 🚀 **FastAPI REST API**: Modern, fast API endpoints for integration
- 🔄 **Redis Caching**: Cache analysis results for improved performance
- 📡 **Opik Tracing**: Integrated observability and tracing for API calls
- 🔍 **Smart Environment Loading**: Automatic `.env` file discovery with parent directory traversal
- 📓 **Research Notebooks**: Jupyter notebooks for experimentation and development

### How It Works

1. **Upload/provide a food image URL**
2. **AI Vision Analysis**: OpenAI's GPT-4.1 Vision model identifies ingredients
3. **Nutritional Calculation**: Analyzes nutritional content based on identified ingredients
4. **Structured Response**: Returns detailed JSON with ingredients, quantities, and nutrients

## Prerequisites

- Python 3.12 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Opik API key ([Get one here](https://www.comet.com/site/products/opik/))
- Redis server (optional, for caching)
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

### 4. Set Up Environment Variables

#### Option A: Using `.env` File (Recommended)

Create a `.env` file in the project root:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Opik Tracing Configuration
OPIK_API_KEY=your-opik-api-key-here
OPIK_PROJECT_NAME=food-image-analyzer
OPIK_WORKSPACE=your-opik-workspace
OPIK_URL_OVERRIDE=https://www.comet.com/opik/api

# Redis Configuration (optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

**Understanding Environment Variable Loading:**

load it in your terminal session:

```bash
set -a; source .env; set +a
```

This project uses `python-dotenv` to automatically load environment variables from the `.env` file. The application is configured with smart `.env` file discovery using `find_dotenv()`:

```python
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
```

**How `find_dotenv()` Works:**

The `find_dotenv()` function intelligently searches for your `.env` file by **traversing parent directories**. This means:

1. **Starts at the current file's location** (e.g., `src/api/app.py`)
2. **Searches upward** through each parent directory:
   - `src/api/` → no `.env` found
   - `src/` → no `.env` found
   - `food-image-analyzer/` (project root) → ✓ `.env` found!
3. **Returns the path** to the first `.env` file it finds
4. **Loads the variables** into your application's environment

**Benefits of this approach:**

- ✅ Works regardless of where you run your Python files from
- ✅ No need to specify absolute paths
- ✅ Single `.env` file at project root serves entire codebase
- ✅ Consistent across different subdirectories (`src/api/`, `src/services/`, etc.)

#### Option B: Export as Environment Variable

**macOS/Linux:**

```bash
export OPENAI_API_KEY=your-api-key-here
export OPIK_API_KEY=your-opik-api-key-here
export OPIK_PROJECT_NAME=food-image-analyzer
export OPIK_WORKSPACE=your-opik-workspace
export OPIK_URL_OVERRIDE=https://www.comet.com/opik/api
```

**Windows (PowerShell):**

```powershell
$env:OPENAI_API_KEY = "your-api-key-here"
$env:OPIK_API_KEY = "your-opik-api-key-here"
```

### 5. Run Redis (Optional)

If you want to enable caching, start a Redis server:

```bash
# Using Docker
docker run -d -p 6379:6379 redis:latest

# Or using Homebrew (macOS)
brew services start redis
```

### 6. Run the Application

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

## API Endpoints

| Method | Endpoint       | Description                          |
| ------ | -------------- | ------------------------------------ |
| `GET`  | `/`            | Welcome message                      |
| `GET`  | `/health`      | Health check endpoint                |
| `POST` | `/ingredients` | Analyze image to extract ingredients |
| `POST` | `/nutrients`   | Calculate nutritional information    |

### POST `/ingredients`

Analyze a food image to extract ingredients.

**Request Body:**

```json
{
  "image_url": "https://example.com/food-image.jpg",
  "user_id": "user-123"
}
```

**Response:**

```json
{
  "status": "successful",
  "processed_at": "2026-01-12T10:30:00Z",
  "request": {
    "image_url": "https://example.com/food-image.jpg",
    "user_id": "user-123"
  },
  "response": {
    "name": "Caesar Salad",
    "ingredients": [
      { "ingredient_name": "Romaine lettuce", "portiont": "2 cups" },
      { "ingredient_name": "Parmesan cheese", "portiont": "30g" },
      { "ingredient_name": "Croutons", "portiont": "1/2 cup" }
    ]
  },
  "error": null
}
```

### POST `/nutrients`

Calculate nutritional information from ingredients.

**Request Body:**

```json
{
  "ingredients": [
    { "ingredient_name": "Romaine lettuce", "portiont": "2 cups" },
    { "ingredient_name": "Parmesan cheese", "portiont": "30g" }
  ],
  "user_id": "user-123"
}
```

**Response:**

```json
{
  "status": "successful",
  "processed_at": "2026-01-12T10:30:00Z",
  "request": { ... },
  "response": {
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
food-image-analyzer/
├── .env                    # Environment variables (create this)
├── .github/                # GitHub configuration
│   └── workflows/
│       └── tests.yml       # CI/CD test workflow
├── .gitignore              # Git ignore patterns
├── .python-version         # Python version specification
├── Dockerfile              # Docker container configuration
├── LICENSE                 # Project license
├── main.py                 # Command-line application entry point
├── notebooks/              # Jupyter notebooks for research
│   └── research.ipynb      # Research and experimentation notebook
├── pyproject.toml          # Project dependencies and configuration
├── README.md               # This file
├── src/                    # Source code directory
│   ├── api/                # FastAPI application
│   │   ├── __init__.py     # Package initializer
│   │   ├── app.py          # API endpoints and server setup
│   │   └── schemas.py      # API request/response schemas (Pydantic models)
│   └── services/           # Service modules
│       ├── __init__.py     # Package initializer
│       ├── analysis/       # Food analysis services
│       │   ├── ingredients.py  # Ingredient detection using GPT Vision
│       │   ├── nutrients.py    # Nutritional analysis
│       │   └── schemas.py      # Data models (Ingredient, IngredientsResponse, NutrientsResponse)
│       ├── cache/          # Redis caching service
│       │   ├── __init__.py
│       │   ├── client.py   # RedisService for get/set operations
│       │   └── config.py   # Redis connection configuration
│       ├── chat_gpt/       # OpenAI ChatGPT integration
│       │   ├── __init__.py
│       │   ├── config.py   # Default model configuration (gpt-4.1)
│       │   └── gpt.py      # ChatGPT client with text, parsed, and image response methods
│       ├── image_processing.py  # Image encoding utilities (base64)
│       ├── opik_tracing/   # Opik observability integration
│       │   ├── config.py   # Opik configuration settings
│       │   └── configure.py # Opik setup and initialization
│       └── prompts.py      # AI prompts for ingredient and nutrient analysis
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── conftest.py         # Pytest fixtures and configuration
│   ├── api/                # API endpoint tests
│   │   ├── __init__.py
│   │   └── test_app.py     # FastAPI app tests
│   └── services/           # Service tests
│       ├── __init__.py
│       └── analysis/       # Analysis service tests
│           ├── __init__.py
│           ├── test_ingredients.py  # Ingredient analysis tests
│           └── test_nutrients.py    # Nutrient analysis tests
└── uv.lock                 # Dependency lock file
```

### Key Components

| Component                | Path                                   | Description                                       |
| ------------------------ | -------------------------------------- | ------------------------------------------------- |
| **API Layer**            | `src/api/`                             | FastAPI REST endpoints with Pydantic schemas      |
| **Ingredients Analyzer** | `src/services/analysis/ingredients.py` | Uses GPT-4.1 Vision to detect food ingredients    |
| **Nutrients Analyzer**   | `src/services/analysis/nutrients.py`   | Calculates nutritional values from ingredients    |
| **ChatGPT Client**       | `src/services/chat_gpt/gpt.py`         | OpenAI API wrapper with structured output support |
| **Redis Cache**          | `src/services/cache/`                  | Caching layer for analysis results                |
| **Opik Tracing**         | `src/services/opik_tracing/`           | Observability and request tracing                 |
| **Image Processing**     | `src/services/image_processing.py`     | Base64 encoding for images                        |
| **Prompts**              | `src/services/prompts.py`              | AI prompts for analysis tasks                     |

### Using Jupyter Notebooks

To run the research notebooks:

```bash
uv run jupyter notebook notebooks/research.ipynb
```

## Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for fast Python linting and formatting.

### Running Ruff

**Check for linting issues:**

```bash
uv run ruff check .
```

**Auto-fix linting issues:**

```bash
uv run ruff check --fix .
```

**Format code:**

```bash
uv run ruff format .
```

**Check formatting (without making changes):**

```bash
uv run ruff format --check .
```

### Recommended Workflow

Before committing code, run:

```bash
uv run ruff check --fix .             # Automatically fix linting violations
uv run ruff format .                  # Format code for consistent style
uv run ruff check --select I --fix    # Sort and organize import statements
```

## Running Tests

This project uses [pytest](https://docs.pytest.org/) for unit testing.

### Run All Tests

```bash
uv run pytest
```

### Run Tests with Verbose Output

```bash
uv run pytest -v
```

### Run a Specific Test File

```bash
uv run pytest tests/api/test_app.py
```

### Run Tests with Coverage

```bash
uv run pytest --cov=src
```

## CI/CD

This project uses GitHub Actions for continuous integration. Tests are automatically run on:

- Push to `main` branch
- Pull requests to `main` branch

See `.github/workflows/tests.yml` for the workflow configuration.

## Dependencies

### Runtime Dependencies

| Package             | Description                            |
| ------------------- | -------------------------------------- |
| `fastapi[standard]` | Modern web framework for building APIs |
| `openai`            | OpenAI Python SDK for GPT models       |
| `opik`              | Observability and tracing platform     |
| `requests`          | HTTP library for image fetching        |

### Development Dependencies

| Package     | Description                      |
| ----------- | -------------------------------- |
| `ipykernel` | Jupyter notebook kernel          |
| `loguru`    | Logging library                  |
| `redis`     | Redis client for caching         |
| `ruff`      | Fast Python linter and formatter |
| `pytest`    | Testing framework                |

## License

See [LICENSE](LICENSE) for details.
