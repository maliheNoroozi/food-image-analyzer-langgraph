from pydantic_settings import BaseSettings

# This code creates a configuration object that automatically loads required settings (strings) like API keys and project info from env file
class OpikConfig(BaseSettings):
    opik_api_key: str
    opik_project_name: str
    opik_workspace: str
    opik_url_override: str

opik_config = OpikConfig()