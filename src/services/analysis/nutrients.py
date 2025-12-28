from loguru import logger

from services.analysis.schemas import Ingredient, NutrientsResponse
from services.cache.client import RedisService
from services.chat_gpt.config import DEFAULT_CHATGPT_MODEL
from services.chat_gpt.gpt import ChatGPT
from services.prompts import FoodImageAnalyzerPrompts


class NutrientsAnalyzer:
    def __init__(self):
        self.chat_gpt = ChatGPT()
        self.redis_server = RedisService()

    def analyze(self, ingredients: list[Ingredient]) -> NutrientsResponse:
        try:
            ingredients_key = "_".join(
                [f"{i.ingredient_name}:{i.portiont}" for i in ingredients]
            )
            cache_key = f"nutrients:{ingredients_key}"
            cached_result = self.redis_server.get(cache_key)
            if cached_result:
                return NutrientsResponse.model_validate_json(cached_result)
            ingredients_str = "\n".join([str(ingredient) for ingredient in ingredients])
            user_prompt = FoodImageAnalyzerPrompts.NUTRIENT_USER_PROMPT.format(
                ingredients_list=ingredients_str
            )
            result = self.chat_gpt.generate_parsed_response(
                model=DEFAULT_CHATGPT_MODEL,
                system_prompt=FoodImageAnalyzerPrompts.NUTRIENT_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                response_format=NutrientsResponse,
            )
            self.redis_server.set(cache_key, result.model_dump_json())
            return result
        except Exception as error:
            logger.error(f"Error analyzing ingredients: {error}")
            raise error
