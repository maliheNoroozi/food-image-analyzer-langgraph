import hashlib

from loguru import logger

from services.analysis.schemas import IngredientsResponse
from services.cache.client import RedisService
from services.chat_gpt.config import DEFAULT_CHATGPT_MODEL
from services.chat_gpt.gpt import ChatGPT
from services.image_processing import encode_image_by_url
from services.prompts import FoodImageAnalyzerPrompts


class IngredientsAnalyzer:
    def __init__(self):
        self.chat_gpt = ChatGPT()
        self.redis_server = RedisService()

    def analyze(self, image_url: str) -> IngredientsResponse:
        try:
            base64_image = encode_image_by_url(image_url)
            image_hash = hashlib.sha256(base64_image.encode()).hexdigest()
            cache_key = f"ingredients:{image_hash}"
            cached_result = self.redis_server.get(cache_key)
            if cached_result:
                return IngredientsResponse.model_validate_json(cached_result)
            result = self.chat_gpt.generate_image_response_by_base64_image(
                model=DEFAULT_CHATGPT_MODEL,
                system_prompt=FoodImageAnalyzerPrompts.INGREDIENTS_SYSTEM_PROMPT,
                user_prompt=FoodImageAnalyzerPrompts.INGREDIENTS_USER_PROMPT,
                base64_image=base64_image,
                response_format=IngredientsResponse,
            )
            self.redis_server.set(cache_key, result.model_dump_json())
            return result
        except Exception as error:
            logger.error(f"Error analyzing ingredients: {error}")
            raise error
