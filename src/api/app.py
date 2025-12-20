import sys
from datetime import datetime
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

from api.schemas import (
    IngredientsEndpointRequest,
    IngredientsEndpointResponse,
    NutrientsEndpointRequest,
    NutrientsEndpointResponse,
    Status,
)
from services.analysis.ingredients import IngredientsAnalyzer
from services.analysis.nutrients import NutrientsAnalyzer

load_dotenv(find_dotenv())

app = FastAPI()
ingredients_analyzer = IngredientsAnalyzer()
nutrients_analyzer = NutrientsAnalyzer()


@app.get("/")
def root():
    return {"message": "Welcome to the Meal Scanner API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/ingredients")
def ingredients(request: IngredientsEndpointRequest) -> IngredientsEndpointResponse:
    try:
        result = ingredients_analyzer.analyze(image_url=request.image_url)
        return IngredientsEndpointResponse(
            status=Status.SUCCESSFUL,
            processed_at=datetime.utcnow(),
            request=request,
            response=result,
            error=None,
        )
    except Exception as error:
        return IngredientsEndpointResponse(
            status=Status.FAILED,
            processed_at=datetime.utcnow(),
            request=request,
            response=None,
            error=str(error),
        )


@app.post("/nutrients")
def nutrients(request: NutrientsEndpointRequest) -> NutrientsEndpointResponse:
    try:
        result = nutrients_analyzer.analyze(ingredients=request.ingredients)
        return NutrientsEndpointResponse(
            status=Status.SUCCESSFUL,
            processed_at=datetime.utcnow(),
            request=request,
            response=result,
            error=None,
        )
    except Exception as error:
        return NutrientsEndpointResponse(
            status=Status.FAILED,
            processed_at=datetime.utcnow(),
            request=request,
            response=None,
            error=str(error),
        )
