from typing import Optional

from loguru import logger
from redis import Redis
from redis.exceptions import RedisError

from services.cache.config import redis_config


class RedisService:
    def __init__(self):
        self.redis = Redis(
            redis_config.redis_host,
            port=redis_config.redis_port,
            db=redis_config.redis_db,
            decode_responses=True,
        )

    def get(self, key: str) -> Optional[str]:
        try:
            value = self.redis.get(key)
            if value is not None:
                logger.info("Cache hit")
            else:
                logger.info("Cache miss")
            return value
        except RedisError as error:
            logger.error(f"Redis error retrieving key: {error}")
            return None

    def set(self, key: str, value: str) -> bool:
        try:
            self.redis.set(key, value)
            logger.info("Successfully set cache value")
            return True
        except RedisError as error:
            logger.error(f"Redis error setting key: {error}")
            return False
