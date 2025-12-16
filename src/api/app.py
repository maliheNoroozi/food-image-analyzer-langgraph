from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv

from services.analysis.schemas import Ingredient

load_dotenv(find_dotenv())

app = FastAPI()

@app.get('/health')
def health_check():
    return {'status': 'healthy'}

@app.post('/ingredients', response_model: IngrediantsResponse)
def ingredients(image_url: str):
    from services.analysis.ingredients import IngredientsAnalyzer
    analyzer = IngredientsAnalyzer()
    result = analyzer.analyze(image_url = image_url)
    return result

@app.post('/nutrients', response_model: NutrientsResponse)
def nutrients(ingredients: list[Ingredient]):
    from services.analysis.nutrients import NutrientsAnalyzer
    analyzer = NutrientsAnalyzer()
    result = analyzer.analyze(ingredients = ingredients)
    return result




