from redis import Redis
from services.cache.config import redis_config
from loguru import logger

class RedisService:
    def __init__(self):
        self.redis = Redis(redis_config.redis_host, port=redis_config.redis_port, db=redis_config.redis_db, decode_responses=True)

    def get(self, key:str) -> str:
        try:
            logger.info(f"Cached result found for key {key}")
            return self.redis.get(key)
        except Exception as error:
            logger.error(f"Error getting key {key}: {error}")
            raise error


    def set(self, key: str, value: str) -> None:
        try:
            logger.info(f"Setting result for key {key}")
            return self.redis.set(key, value)
        except Exception as error:
             logger.error(f"Error setting key {key}: {error}")
             raise error