from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from loguru import logger
from typing_extensions import TypedDict

from services.image_processing import encode_image_by_url
from services.llm.config import FOOD_LLM_MODEL, FOOD_LLM_TEMPERATURE
from services.llm.schemas import IngredientsResponse, NutrientsResponse
from services.prompts import FoodImageAnalyzerPrompts


class State(TypedDict):
    image_url: str
    ingredients_response: IngredientsResponse
    nutrients_response: NutrientsResponse


class FoodLLM:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=FOOD_LLM_MODEL,
            temperature=FOOD_LLM_TEMPERATURE,
        )
        self.chain = self.build_workflow()

    def analyze_ingredients(self, state: State):
        try:
            base64_image = encode_image_by_url(state["image_url"])

            messages = [
                {
                    "role": "system",
                    "content": FoodImageAnalyzerPrompts.INGREDIENTS_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": FoodImageAnalyzerPrompts.INGREDIENTS_USER_PROMPT,
                        },
                        {
                            "type": "image",
                            "base64": base64_image,
                            "mime_type": "image/jpeg",
                        },
                    ],
                },
            ]

            structured_llm = self.llm.with_structured_output(IngredientsResponse)
            result = structured_llm.invoke(messages)
            return {"ingredients_response": result}
        except Exception as error:
            logger.error(f"Error analyzing ingredients: {error}")
            raise error

    def analyze_nutrients(self, state: State):
        try:
            ingredients = state["ingredients_response"].ingredients
            ingredients_str = "\n".join([str(ingredient) for ingredient in ingredients])
            user_prompt = FoodImageAnalyzerPrompts.NUTRIENT_USER_PROMPT.format(
                ingredients_list=ingredients_str
            )

            messages = [
                {
                    "role": "system",
                    "content": FoodImageAnalyzerPrompts.NUTRIENT_SYSTEM_PROMPT,
                },
                {"role": "user", "content": user_prompt},
            ]

            structured_llm = self.llm.with_structured_output(NutrientsResponse)
            result = structured_llm.invoke(messages)
            return {"nutrients_response": result}
        except Exception as error:
            logger.error(f"Error analyzing nutrients: {error}")
            raise error

    def build_workflow(self):
        workflow = StateGraph(State)

        # Add nodes
        workflow.add_node("analyze_ingredients", self.analyze_ingredients)
        workflow.add_node("analyze_nutrients", self.analyze_nutrients)

        # Add edges to connect nodes
        workflow.add_edge(START, "analyze_ingredients")
        workflow.add_edge("analyze_ingredients", "analyze_nutrients")
        workflow.add_edge("analyze_nutrients", END)

        # Compile
        chain = workflow.compile()

        return chain

    def invoke(self, image_url: str) -> State:
        state = self.chain.invoke({"image_url": image_url})
        return {
            "ingredients_response": state["ingredients_response"],
            "nutrients_response": state["nutrients_response"],
        }
