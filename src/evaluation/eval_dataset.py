from opik import Dataset
from pydantic import ValidationError

from evaluation.llm_judging import judge_ingredients
from evaluation.schema import (
    DatasetItem,
    EvaluationOutput,
    EvaluationResult,
    NutrientItems,
)
from evaluation.scoring import score_nutrients
from services.analysis.ingredients import IngredientsAnalyzer
from services.analysis.nutrients import NutrientsAnalyzer


REQUIRED_DATASET_FIELDS = (
    "img_url",
    "ingredients",
    "carbohydrates",
    "protein",
    "fat",
    "total_calories",
)

def evaluate_dataset_item(
    dataset_item: dict,
    ingredient_analyzer: IngredientsAnalyzer | None = None,
    nutrient_analyzer: NutrientsAnalyzer | None = None,
) -> dict:
    for key in REQUIRED_DATASET_FIELDS:
        if key not in dataset_item:
            raise KeyError(f"Missing required dataset field: {key}")

    ingredient_analyzer = ingredient_analyzer or IngredientsAnalyzer()
    ingredients_result = ingredient_analyzer.analyze(image_url=dataset_item['img_url'])

    nutrient_analyzer = nutrient_analyzer or NutrientsAnalyzer()
    nutrient_result = nutrient_analyzer.analyze(
        ingredients=ingredients_result.ingredients
    )

    llm_output = {
        "ingredients": [
            ingredient.ingredient_name for ingredient in ingredients_result.ingredients
        ],
        "nutrients": {
            "carbohydrates": nutrient_result.total_carbohydrates_g,
            "protein": nutrient_result.total_protein_g,
            "fat": nutrient_result.total_fats_g,
            "total_calories": nutrient_result.total_calories,
        },
    }
    expected_output = {
        "ingredients": dataset_item["ingredients"],
        "nutrients": {
            "carbohydrates": dataset_item["carbohydrates"],
            "protein": dataset_item["protein"],
            "fat": dataset_item["fat"],
            "total_calories": dataset_item["total_calories"],
        },
    }

    return {"llm_output": llm_output, "expected_output": expected_output}

def evaluate_dataset(dataset: Dataset) -> list[dict]:
    scores = []

    ingredient_analyzer = IngredientsAnalyzer()
    nutrient_analyzer = NutrientsAnalyzer()

    for dataset_item in dataset.get_items():
        try:
            evaluation_result = evaluate_dataset_item(
                dataset_item=dataset_item,
                ingredient_analyzer=ingredient_analyzer,
                nutrient_analyzer=nutrient_analyzer,
            )
            score_ingredients = judge_ingredients(
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
        except (KeyError, ValueError, TypeError, ValidationError):
            continue
    return scores
