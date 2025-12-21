from loguru import logger

from services.analysis.schemas import Ingredient, NutrientsResponse
from services.chat_gpt.gpt import ChatGPT
from services.prompts import FoodImageAnalyzerPrompts


class NutrientsAnalyzer:
    def __init__(self):
        self.chat_gpt = ChatGPT()

    def analyze(self, ingredients: list[Ingredient]) -> NutrientsResponse:
        try:
            ingredients_str = "\n".join([str(ingredient) for ingredient in ingredients])
            user_prompt = FoodImageAnalyzerPrompts.NUTRIENT_USER_PROMPT.format(
                ingredients_list=ingredients_str
            )
            result = self.chat_gpt.generate_parsed_response(
                model="gpt-4.1",
                system_prompt=FoodImageAnalyzerPrompts.NUTRIENT_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                response_format=NutrientsResponse,
            )
            return result
        except Exception as error:
            logger.error(f"Error analyzing ingredients: {error}")
            raise error
