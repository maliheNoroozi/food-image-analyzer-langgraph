from evaluation.schema import IngredientConfusionMatrix
from services.chat_gpt.config import DEFAULT_CHATGPT_MODEL
from services.chat_gpt.gpt import ChatGPT
from services.prompts import FoodImageAnalyzerPrompts


def judge_ingredients(predicted_ingredients, expected_ingredients) -> dict:
    chat_gpt = ChatGPT()

    user_prompt = FoodImageAnalyzerPrompts.EVALUATION_INGREDIENTS_USER_PROMPT.format(
        predicted_ingredients=predicted_ingredients,
        expected_ingredients=expected_ingredients,
    )

    result = chat_gpt.generate_parsed_response(
        system_prompt=FoodImageAnalyzerPrompts.EVALUATION_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_format=IngredientConfusionMatrix,
        model=DEFAULT_CHATGPT_MODEL,
    )

    return {
        "true_positive": result.true_positive,
        "false_positive": result.false_positive,
        "false_negative": result.false_negative,
    }
