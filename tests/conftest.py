"""Shared pytest fixtures and configuration."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Mock opik configuration before any imports that trigger it
# This prevents the need for real environment variables during tests
mock_opik_config = MagicMock()
mock_opik_config.opik_api_key = "test-api-key"
mock_opik_config.opik_project_name = "test-project"
mock_opik_config.opik_workspace = "test-workspace"
mock_opik_config.opik_url_override = "https://test.opik.com"

# Patch the config module before it gets imported by other modules
patch("services.opik_tracing.config.opik_config", mock_opik_config).start()
# Patch the configure function to do nothing
patch("services.opik_tracing.configure.configure_opik", lambda: None).start()

