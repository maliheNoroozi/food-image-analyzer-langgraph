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

After installation, restart your terminal or run:

### 2. install Python version 3.12.0

```bash
# Installing python and creating virtual environment at: (`.venv/`
uv venv --python 3.12.0
```

### 3. Initialize project and install dependencies and dev dependencies

```bash
uv init
```

Adding Dependencies

```bash
uv add openai
```

Adding Dependencies to a Dependency Group

```bash
uv add --group dev ipykernel
```

### 4. Install Dependencies

Install all project dependencies (like `npm install`):

```bash
# This will installs packages from `pyproject.toml`.
uv sync
```

### 5. Set Up OpenAI API Key

#### Option A: Using `.env` file (Recommended)

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your-api-key-here
```

Then load it in your terminal session:

```bash
set -a; source .env; set +a
```

Or use `python-dotenv` package to load it automatically in Python:

```python
from dotenv import load_dotenv
load_dotenv()
```

### 6. Run the Application

```bash
uv run python main.py
```

Alternatively, activate the virtual environment first:

```bash
source .venv/bin/activate
python main.py
```

To exit the chat, type `exit` or `quit`.

## Project Structure

```
meal-scanner/
├── .gitignore          # Git ignore patterns
├── .python-version     # Python version specification
├── LICENSE             # Project license
├── main.py             # Main application entry point
├── notebooks/          # Jupyter notebooks for research
│   └── research.ipynb  # Research and experimentation notebook
├── pyproject.toml      # Project dependencies (like package.json)
├── README.md           # This file
├── src/                # Source code directory
└── uv.lock             # Lock file (like package-lock.json)
```

### Using Jupyter Notebooks

To run the research notebooks:

```bash
uv run jupyter notebook notebooks/research.ipynb
```

## License

See [LICENSE](LICENSE) for details.
