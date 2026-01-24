from pydantic import BaseModel


class DatasetItem(BaseModel):
    img_url: str
    ingredients: list[str]
    carbohydrates: float
    protein: float
    fat: float
    total_calories: float


class IngredientConfusionMatrix(BaseModel):
    true_positive: int
    false_positive: int
    false_negative: int


class NutrientItems(BaseModel):
    carbohydrates: float
    protein: float
    fat: float
    total_calories: float


class EvaluationOutput(BaseModel):
    ingredients: list[str]
    nutrients: NutrientItems


class EvaluationResult(BaseModel):
    llm_output: EvaluationOutput
    expected_output: EvaluationOutput
