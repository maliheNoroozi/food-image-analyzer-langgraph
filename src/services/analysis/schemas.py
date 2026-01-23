from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    ingredient_name: str
    portion: str


class IngredientsResponse(BaseModel):
    name: str
    ingredients: list[Ingredient]


class NutrientsResponse(BaseModel):
    total_calories: float = Field(description="Total calories in kcal")
    total_protein_g: float = Field(description="Total protein in grams")
    total_carbohydrates_g: float = Field(description="Total carbohydrates in grams")
    total_fats_g: float = Field(description="Total fats in grams")
    total_fiber_g: float = Field(description="Total fiber in grams")
