from langchain_openai import ChatOpenAI
from services.llm.config import FOOD_LLM_MODEL

from evaluation.schema import IngredientConfusionMatrix
from services.prompts import FoodImageAnalyzerPrompts


class IngredientsJudger:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=FOOD_LLM_MODEL,
            temperature=0,
        )
        self.structured_llm = self.llm.with_structured_output(IngredientConfusionMatrix)

    def invoke(self, predicted_ingredients, expected_ingredients) -> dict:
        messages = [
            {
                "role": "system",
                "content": FoodImageAnalyzerPrompts.EVALUATION_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": FoodImageAnalyzerPrompts.EVALUATION_INGREDIENTS_USER_PROMPT.format(
                            predicted_ingredients=predicted_ingredients,
                            expected_ingredients=expected_ingredients,
                        ),
                    },
                ],
            },
        ]

        result = self.structured_llm.invoke(messages)

        return {
            "true_positive": result.true_positive,
            "false_positive": result.false_positive,
            "false_negative": result.false_negative,
        }
