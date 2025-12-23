from opik import configure
from loguru import logger

from services.opik_tracing.config import opik_config

def configure_opik():
    try:        
        configure(
            api_key=opik_config.opik_api_key,
            url=opik_config.opik_url_override,
            workspace=opik_config.opik_workspace,
            use_local=False, # Don't use my computer, use the online/server version
            force=True # Configure yourself no matter what, even if you were already configured before.
        )
        logger.info(f"Opik configured successfully for project: {opik_config.opik_project_name}")
    except Exception as error:
        logger.error(f"Error configuring Opik: {error}")
        raise error