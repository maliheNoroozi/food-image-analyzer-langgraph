from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from services.llm.schemas import Ingredient, IngredientsResponse, NutrientsResponse


class Status(Enum):
    FAILED = "failed"
    SUCCESSFUL = "successful"


class IngredientsEndpointRequest(BaseModel):
    image_url: str = Field(
        ...,
        description="The URL of the image to analyze",
        example="https://images.pexels.com/photos/699953/pexels-photo-699953.jpeg",
    )


class IngredientsEndpointResponse(BaseModel):
    status: Status
    processed_at: datetime
    request: IngredientsEndpointRequest
    response: IngredientsResponse | None = None
    error: str | None = None


class NutrientsEndpointRequest(BaseModel):
    ingredients: list[Ingredient] = Field(
        ...,
        description="The ingredients to analyze",
        example=[
            {"ingredient_name": "shrimp", "portion": "2 large shrimp"},
            {"ingredient_name": "flat rice noodles", "portion": "1.5 cups cooked"},
            {"ingredient_name": "quail eggs", "portion": "2 eggs, hard-boiled"},
            {"ingredient_name": "onion", "portion": "1/4 cup, sliced"},
            {"ingredient_name": "green onions", "portion": "2 tbsp, chopped"},
            {"ingredient_name": "red chili peppers", "portion": "2-3 slices"},
            {"ingredient_name": "cilantro", "portion": "2 tbsp, chopped"},
            {"ingredient_name": "mint leaves", "portion": "a few leaves"},
        ],
    )


class NutrientsEndpointResponse(BaseModel):
    status: Status
    processed_at: datetime
    request: NutrientsEndpointRequest
    response: NutrientsResponse | None = None
    error: str | None = None


class FoodAnalysisEndpointRequest(IngredientsEndpointRequest):
    pass


class FoodAnalysisEndpointResponse(BaseModel):
    status: Status
    processed_at: datetime
    request: FoodAnalysisEndpointRequest
    nutrients_response: NutrientsResponse | None = None
    ingredients_response: IngredientsResponse | None = None
    error: str | None = None
