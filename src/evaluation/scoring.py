import math

NUTRIENTS = ("carbohydrates", "protein", "fat", "total_calories")


def _safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def score_nutrients(predicted_nutrients: dict, expected_nutrients: dict) -> dict:
    result = {}
    for nutrient in NUTRIENTS:
        expected_value = expected_nutrients[nutrient]
        predicted_value = predicted_nutrients[nutrient]
        if expected_value == 0:
            result[nutrient + "_se"] = 0
            result[nutrient + "_ae"] = 0
            continue
        ratio_error = 1 - predicted_value / expected_value
        result[nutrient + "_se"] = ratio_error**2
        result[nutrient + "_ae"] = abs(ratio_error)
    return result


def aggregate_scores(scores: list[dict]) -> dict:
    if not scores:
        return {
            "ingredient_recall": 0,
            "ingredient_precision": 0,
            "ingredient_f1_score": 0,
            "carbohydrates_rmse": 0,
            "protein_rmse": 0,
            "fat_rmse": 0,
            "total_calories_rmse": 0,
            "carbohydrates_mae": 0,
            "protein_mae": 0,
            "fat_mae": 0,
            "total_calories_mae": 0,
        }

    ingredients_false_positive = 0
    ingredients_false_negative = 0
    ingredients_true_positive = 0

    carbohydrates_rmse = 0
    protein_rmse = 0
    fat_rmse = 0
    total_calories_rmse = 0
    carbohydrates_mae = 0
    protein_mae = 0
    fat_mae = 0
    total_calories_mae = 0

    for score in scores:
        ingredient_score = score["ingredient_score"]
        nutrient_score = score["nutrient_score"]

        ingredients_false_positive += ingredient_score["false_positive"]
        ingredients_false_negative += ingredient_score["false_negative"]
        ingredients_true_positive += ingredient_score["true_positive"]

        carbohydrates_rmse += nutrient_score["carbohydrates_se"]
        protein_rmse += nutrient_score["protein_se"]
        fat_rmse += nutrient_score["fat_se"]
        total_calories_rmse += nutrient_score["total_calories_se"]

        carbohydrates_mae += nutrient_score["carbohydrates_ae"]
        protein_mae += nutrient_score["protein_ae"]
        fat_mae += nutrient_score["fat_ae"]
        total_calories_mae += nutrient_score["total_calories_ae"]

    ingredient_recall = _safe_divide(
        ingredients_true_positive,
        ingredients_true_positive + ingredients_false_negative,
    )

    ingredient_precision = _safe_divide(
        ingredients_true_positive,
        ingredients_true_positive + ingredients_false_positive,
    )

    ingredient_f1_score = _safe_divide(
        2 * ingredients_true_positive,
        2 * ingredients_true_positive
        + ingredients_false_positive
        + ingredients_false_negative,
    )

    carbohydrates_rmse = math.sqrt(carbohydrates_rmse / len(scores))
    protein_rmse = math.sqrt(protein_rmse / len(scores))
    fat_rmse = math.sqrt(fat_rmse / len(scores))
    total_calories_rmse = math.sqrt(total_calories_rmse / len(scores))

    carbohydrates_mae = carbohydrates_mae / len(scores)
    protein_mae = protein_mae / len(scores)
    fat_mae = fat_mae / len(scores)
    total_calories_mae = total_calories_mae / len(scores)

    return {
        "ingredient_recall": ingredient_recall,
        "ingredient_precision": ingredient_precision,
        "ingredient_f1_score": ingredient_f1_score,
        "carbohydrates_rmse": carbohydrates_rmse,
        "protein_rmse": protein_rmse,
        "fat_rmse": fat_rmse,
        "total_calories_rmse": total_calories_rmse,
        "carbohydrates_mae": carbohydrates_mae,
        "protein_mae": protein_mae,
        "fat_mae": fat_mae,
        "total_calories_mae": total_calories_mae,
    }
