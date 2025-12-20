from loguru import logger

from services.chat_gpt.gpt import ChatGPT
from services.image_processing import encode_image_by_url
from services.prompts import MealScannerPrompts
from services.analysis.schemas import IngredientsResponse

class IngredientsAnalyzer:
    def __init__(self):
        self.chat_gpt = ChatGPT()
    
    def analyze(self, image_url: str) -> IngredientsResponse :
        try:
            base64_image = encode_image_by_url(image_url)
            result = self.chat_gpt.generate_image_response_by_base64_image(
                model='gpt-4.1',
                system_prompt=MealScannerPrompts.INGREDIENTS_SYSTEM_PROMPT,
                user_prompt=MealScannerPrompts.INGREDIENTS_USER_PROMPT,
                base64_image=base64_image,
                response_format=IngredientsResponse
            )
            return result
        except Exception as error:
            logger.error(f"Error analyzing ingredients: {error}")
            raise error