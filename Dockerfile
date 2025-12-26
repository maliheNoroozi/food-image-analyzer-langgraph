# 1) Start from a small Python image
FROM python:3.12-slim

# 3) Install uv inside the container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 2) Set a working folder inside the container
WORKDIR /app

# 4) Copy only dependency files first (better caching)
COPY pyproject.toml uv.lock .

# 5) Install dependencies
RUN uv sync --no-dev

# 6) Copy ONLY the src folder into the container
COPY src/ .

# 7) Set the PYTHONPATH environment variable
ENV PYTHONPATH=.   

# 8) Set the PYTHONBUFFERED environment variable
ENV PYTHONUNBUFFERED=1

# 8) Expose FastAPI port
EXPOSE 8000

# 9) Start FastAPI
CMD ["uv", "run", "fastapi", "dev", "api/app.py", "--host", "0.0.0.0", "--port", "8000"]
