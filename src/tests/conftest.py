"""Shared pytest fixtures and configuration."""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Set fake environment variables BEFORE any imports
# This allows configs to initialize without real values
os.environ.setdefault("OPENAI_API_KEY", "test-openai-api-key")

# Add src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Now we can safely patch external services to prevent actual initialization
# Mock OpenAI client - patch at the source (openai module) before it gets imported elsewhere
patch("openai.OpenAI", MagicMock).start()

# Mock MongoDB client to avoid real connection attempts in tests
patch("services.database.client.MongoClient", MagicMock).start()

# Mock MongoDB service to prevent module-level initialization side effects
patch("services.database.client.MongoDBService", MagicMock).start()

# Mock FoodLLM so app lifespan can create it without real Redis/OpenAI
patch("api.app.FoodLLM", MagicMock).start()
