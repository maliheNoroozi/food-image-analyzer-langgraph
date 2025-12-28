from pydantic_settings import BaseSettings

class RedisConfig(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0


redis_config = RedisConfig()