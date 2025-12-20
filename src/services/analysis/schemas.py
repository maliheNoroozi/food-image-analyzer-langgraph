from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    ingredient_name: str
    portiont: str


class IngredientsResponse(BaseModel):
    name: str
    ingredients: list[Ingredient]


class NutrientsResponse(BaseModel):
    total_calories: int
    total_protein_g: float = Field(description="Total protein in grams")
    total_carbohydrates_g: float = Field(description="Total carbohydrates in grams")
    total_fats_g: float = Field(description="Total fats in grams")
    total_fiber_g: float = Field(description="Total fiber in grams")
