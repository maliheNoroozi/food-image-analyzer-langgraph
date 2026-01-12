"""Shared pytest fixtures and configuration."""

import os
import sys
from pathlib import Path

# Set fake environment variables BEFORE any imports
# This allows OpikConfig (pydantic-settings) to initialize without real values
os.environ.setdefault("opik_api_key", "test-api-key")
os.environ.setdefault("opik_project_name", "test-project")
os.environ.setdefault("opik_workspace", "test-workspace")
os.environ.setdefault("opik_url_override", "https://test.opik.com")

# Add src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Now we can safely patch the configure function to prevent actual Opik initialization
from unittest.mock import patch

patch("services.opik_tracing.configure.configure_opik", lambda: None).start()

