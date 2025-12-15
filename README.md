# meal-scanner

AI-powered meal scanner using OpenAI's API.

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

Then load it in your terminal session:

```bash
set -a; source .env; set +a
```

Or use `python-dotenv` package to load it automatically in Python:

```bash
uv add python-dotenv
```

```python
from dotenv import load_dotenv
load_dotenv()
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
export PYTHONPATH="${PYTHONPATH}:/Users/malihehnorouzi/Desktop/Projects/meal-scanner"
```

**Windows (PowerShell):**

```powershell
# run with PYTHONPATH inline
$env:PYTHONPATH = "."; python main.py
```

To make it permanent, add to your PowerShell profile:

```powershell
$env:PYTHONPATH = "C:\Users\YourUsername\Desktop\Projects\meal-scanner"
```

**Windows (Command Prompt):**

```cmd
# run with PYTHONPATH inline
set PYTHONPATH=. && python main.py
```

To make it permanent, use System Environment Variables:

1. Search for "Environment Variables" in Windows Settings
2. Add or edit `PYTHONPATH` variable
3. Set value to `C:\Users\YourUsername\Desktop\Projects\meal-scanner`

## Project Structure

```
meal-scanner/
├── .gitignore              # Git ignore patterns
├── .python-version         # Python version specification
├── LICENSE                 # Project license
├── main.py                 # Main application entry point
├── notebooks/              # Jupyter notebooks for research
│   └── research.ipynb      # Research and experimentation notebook
├── pyproject.toml          # Project dependencies and configuration
├── README.md               # This file
├── src/                    # Source code directory
│   └── services/           # Service modules
│       ├── __init__.py     # Package initializer
│       ├── analysis/       # Meal analysis services
│       │   ├── ingredients.py  # Ingredient analysis
│       │   ├── nutrients.py    # Nutrient analysis
│       │   └── schemas.py      # Data schemas
│       ├── chat_gpt/       # OpenAI ChatGPT integration
│       │   ├── __init__.py
│       │   ├── config.py   # API configuration
│       │   └── gpt.py      # GPT client
│       ├── image_processing.py  # Image processing utilities
│       └── prompts.py      # AI prompts and templates
└── uv.lock                 # Dependency lock
```

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
# Fix linting issues and format code
uv run ruff check --fix .
uv run ruff format .
```

## License

See [LICENSE](LICENSE) for details.
