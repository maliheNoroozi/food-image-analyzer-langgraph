from pydantic import ValidationError
from services.llm.food_llm import FoodLLM

from evaluation.llm_judging import IngredientsJudger
from evaluation.scoring import score_nutrients
from langsmith import Client
from langsmith.schemas import Dataset
from loguru import logger


REQUIRED_INPUTS_DATASET_FIELDS = ("img_url",)

REQUIRED_OUTPUTS_DATASET_FIELDS = (
    "ingredients",
    "carbohydrates",
    "protein",
    "fat",
    "total_calories",
)


def evaluate_dataset_item(
    dataset_item: dict,
    food_llm: FoodLLM,
) -> dict:
    for key in REQUIRED_INPUTS_DATASET_FIELDS:
        if key not in dataset_item.inputs:
            raise KeyError(f"Missing required dataset inputs field: {key}")

    for key in REQUIRED_OUTPUTS_DATASET_FIELDS:
        if key not in dataset_item.outputs:
            raise KeyError(f"Missing required dataset outputs field: {key}")

    llm_result = food_llm.invoke(image_url=dataset_item.inputs["img_url"])

    llm_output = {
        "ingredients": [
            ingredient.ingredient_name
            for ingredient in llm_result["ingredients_response"].ingredients
        ],
        "nutrients": {
            "carbohydrates": llm_result["nutrients_response"].total_carbohydrates_g,
            "protein": llm_result["nutrients_response"].total_protein_g,
            "fat": llm_result["nutrients_response"].total_fats_g,
            "total_calories": llm_result["nutrients_response"].total_calories,
        },
    }
    expected_output = {
        "ingredients": dataset_item.outputs["ingredients"],
        "nutrients": {
            "carbohydrates": dataset_item.outputs["carbohydrates"],
            "protein": dataset_item.outputs["protein"],
            "fat": dataset_item.outputs["fat"],
            "total_calories": dataset_item.outputs["total_calories"],
        },
    }

    return {"llm_output": llm_output, "expected_output": expected_output}


def evaluate_dataset(client: Client, dataset: Dataset) -> list[dict]:
    scores = []

    food_llm = FoodLLM()
    ingredients_judger = IngredientsJudger()

    for dataset_item in client.list_examples(dataset_id=dataset.id):
        try:
            evaluation_result = evaluate_dataset_item(
                dataset_item=dataset_item,
                food_llm=food_llm,
            )

            score_ingredients = ingredients_judger.invoke(
                predicted_ingredients=evaluation_result["llm_output"]["ingredients"],
                expected_ingredients=evaluation_result["expected_output"][
                    "ingredients"
                ],
            )

            score_nutrient = score_nutrients(
                predicted_nutrients=evaluation_result["llm_output"]["nutrients"],
                expected_nutrients=evaluation_result["expected_output"]["nutrients"],
            )

            scores.append(
                {
                    "ingredient_score": score_ingredients,
                    "nutrient_score": score_nutrient,
                }
            )
        except (KeyError, ValueError, TypeError, ValidationError) as error:
            logger.error({"error": error})
            continue
        break
    return scores
