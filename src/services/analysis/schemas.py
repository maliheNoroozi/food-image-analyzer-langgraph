from pydantic import BaseModel

class Ingredient(BaseModel):
    ingredient_name: str
    portiont: str

class IngrediantsResponse(BaseModel):
    name: str
    ingredients: list[Ingredient]