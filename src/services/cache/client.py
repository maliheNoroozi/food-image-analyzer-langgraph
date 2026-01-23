from loguru import logger
from redis import Redis

from services.cache.config import redis_config


class RedisService:
    def __init__(self):
        self.redis = Redis(
            redis_config.redis_host,
            port=redis_config.redis_port,
            db=redis_config.redis_db,
            decode_responses=True,
        )

    def get(self, key: str) -> str:
        try:
            result = self.redis.get(key)
            logger.info(f"Cached result found for key {key}")
            return result
        except Exception as error:
            logger.error(f"Key {key} not found in redis cache: {error}")

    def set(self, key: str, value: str) -> None:
        try:
            result = self.redis.set(key, value)
            logger.info(f"Setting result for key {key}")
            return result
        except Exception as error:
            logger.error(f"Could not set key {key}: {error}")
