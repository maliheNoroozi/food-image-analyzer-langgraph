from pydantic_settings import BaseSettings

class MongoDBConfig(BaseSettings):
    mongodb_host: str = "localhost"
    mongodb_port: int = 27017
    mongodb_database: str = "food-image-analyzer"

mongodb_config = MongoDBConfig()