"""Shared pytest fixtures and configuration."""

import os
import sys
from pathlib import Path

# Set fake environment variables BEFORE any imports
# This allows configs to initialize without real values
os.environ.setdefault("opik_api_key", "test-api-key")
os.environ.setdefault("opik_project_name", "test-project")
os.environ.setdefault("opik_workspace", "test-workspace")
os.environ.setdefault("opik_url_override", "https://test.opik.com")
os.environ.setdefault("OPENAI_API_KEY", "test-openai-api-key")

# Add src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Now we can safely patch external services to prevent actual initialization
from unittest.mock import MagicMock, patch

# Mock Opik configuration
patch("services.opik_tracing.configure.configure_opik", lambda: None).start()

# Mock OpenAI client - patch at the source (openai module) before it gets imported elsewhere
patch("openai.OpenAI", MagicMock).start()

# Mock Opik tracking
patch("opik.integrations.openai.track_openai", lambda x: x).start()
