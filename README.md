# food-image-analyzer

AI-powered food image analyzer that analyzes food images to extract ingredients and nutritional information using OpenAI's Vision API.

## Overview

This application provides:

- 🍽️ **Ingredient Detection**: Analyze food images to identify ingredients and their quantities
- 📊 **Nutritional Analysis**: Calculate detailed nutritional information (calories, macros, vitamins, minerals)
- 🚀 **FastAPI REST API**: Modern, fast API endpoints for integration
- 🔍 **Smart Environment Loading**: Automatic `.env` file discovery with parent directory traversal
- 📓 **Research Notebooks**: Jupyter notebooks for experimentation and development

### How It Works

1. **Upload/provide a food image URL**
2. **AI Vision Analysis**: OpenAI's GPT-4 Vision model identifies ingredients
3. **Nutritional Calculation**: Analyzes nutritional content based on identified ingredients
4. **Structured Response**: Returns detailed JSON with ingredients, quantities, and nutrients

## Prerequisites

- Python 3.12 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
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

### 4. Set Up OpenAI API Key

#### Option A: Using `.env` File (Recommended)

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your-api-key-here
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

**Alternative approaches:**

```python
# Simple approach - looks in current directory only
load_dotenv()

# Explicit path - requires exact location
load_dotenv('.env')

# With traversal - automatically finds .env in parent dirs (CURRENT APPROACH)
load_dotenv(find_dotenv())
```

**Loading .env in terminal sessions:**

If you need to load the `.env` file in your terminal session:

```bash
set -a; source .env; set +a
```

#### Option B: Export as Environment Variable

**macOS/Linux:**

```bash
export OPENAI_API_KEY=your-api-key-here
```

**Windows (PowerShell):**

```powershell
$env:OPENAI_API_KEY = "your-api-key-here"
```

**Windows (Command Prompt):**

```cmd
set OPENAI_API_KEY=your-api-key-here
```

### 5. Run the Application

#### FastAPI Server

Start the FastAPI development server:

```bash
PYTHONPATH=. uv run fastapi dev src/api/app.py
```

The API will be available at `http://localhost:8000`

**API Endpoints:**

- `GET /` - Health check endpoint
- `POST /ingredients` - Analyze image to extract ingredients
  - Parameter: `image_url` (string) - URL of the food image
  - Returns: List of ingredients with quantities
- `POST /nutrients` - Calculate nutritional information
  - Body: List of `Ingredient` objects
  - Returns: Detailed nutritional analysis

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
export PYTHONPATH="${PYTHONPATH}:/Users/malihehnorouzi/Desktop/Projects/food-image-analyzer"
```

**Windows (PowerShell):**

```powershell
# run with PYTHONPATH inline
$env:PYTHONPATH = "."; python main.py
```

To make it permanent, add to your PowerShell profile:

```powershell
$env:PYTHONPATH = "C:\Users\YourUsername\Desktop\Projects\food-image-analyzer"
```

**Windows (Command Prompt):**

```cmd
# run with PYTHONPATH inline
set PYTHONPATH=. && python main.py
```

To make it permanent, use System Environment Variables:

1. Search for "Environment Variables" in Windows Settings
2. Add or edit `PYTHONPATH` variable
3. Set value to `C:\Users\YourUsername\Desktop\Projects\food-image-analyzer`

## Project Structure

```
food-image-analyzer/
├── .env                    # Environment variables (create this)
├── .gitignore              # Git ignore patterns
├── .python-version         # Python version specification
├── LICENSE                 # Project license
├── main.py                 # Command-line application entry point
├── notebooks/              # Jupyter notebooks for research
│   └── research.ipynb      # Research and experimentation notebook
├── pyproject.toml          # Project dependencies and configuration
├── README.md               # This file
├── src/                    # Source code directory
│   ├── api/                # FastAPI application
│   │   └── app.py          # API endpoints and server setup
│   └── services/           # Service modules
│       ├── __init__.py     # Package initializer
│       ├── analysis/       # food analysis services
│       │   ├── ingredients.py  # Ingredient analysis
│       │   ├── nutrients.py    # Nutrient analysis
│       │   └── schemas.py      # Data schemas
│       ├── chat_gpt/       # OpenAI ChatGPT integration
│       │   ├── __init__.py
│       │   ├── config.py   # API configuration
│       │   └── gpt.py      # GPT client
│       ├── image_processing.py  # Image processing utilities
│       └── prompts.py      # AI prompts and templates
└── uv.lock                 # Dependency lock file
```

**Key Files:**

- **`.env`**: Environment variables (API keys) - auto-discovered via parent directory traversal
- **`src/api/app.py`**: FastAPI REST API with ingredient and nutrient endpoints
- **`main.py`**: Command-line interface for direct usage
- **`src/services/analysis/`**: Core analysis logic for ingredients and nutrients
- **`src/services/chat_gpt/`**: OpenAI API integration and configuration

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
uv run ruff check --fix .             # Automatically fix linting violations (unused imports, undefined names, bad patterns, style issues, etc.).
uv run ruff format .                  # Format code (indentation, line length, quotes, wrapping, spacing) to ensure consistent style
uv run ruff check --select I --fix    # Sort, remove, organize and groups import statements automatically
```

## License

See [LICENSE](LICENSE) for details.
