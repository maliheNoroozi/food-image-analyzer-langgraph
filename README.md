# meal-scanner

AI-powered meal scanner using OpenAI's API.

## Prerequisites

- Python 3.12 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- `uv` package manager (recommended)

## Getting Started

### 1. Install `uv` Package Manager

`uv` is a fast Python package manager (similar to npm/pnpm for JavaScript):

```bash
# macOS/Linux
brew install uv
```

After installation, restart your terminal or run:

### 2. Install Dependencies

Install all project dependencies (like `npm install`):

```bash
uv sync
```

This creates a virtual environment (`.venv/`) and installs packages from `pyproject.toml`.

### 3. Set Up OpenAI API Key

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

### 4. Run the Application

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
├── main.py              # Main application entry point
├── notebooks/           # Jupyter notebooks for research
├── pyproject.toml       # Project dependencies (like package.json)
├── uv.lock             # Lock file (like package-lock.json)
└── README.md           # This file
```

### Using Jupyter Notebooks

To run the research notebooks:

```bash
uv run jupyter notebook notebooks/research.ipynb
```

## License

See [LICENSE](LICENSE) for details.
