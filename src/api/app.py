from datetime import datetime

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
from services.opik_tracing.configure import configure_opik
from services.database.client import MongoDBService

load_dotenv(find_dotenv())
configure_opik()
app = FastAPI()
mongodb_service = MongoDBService()
ingredients_analyzer = IngredientsAnalyzer()
nutrients_analyzer = NutrientsAnalyzer()


@app.get("/")
def root():
    return {"message": "Welcome to the Food Image Analyzer API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/ingredients")
def ingredients(request: IngredientsEndpointRequest) -> IngredientsEndpointResponse:
    try:
        result = ingredients_analyzer.analyze(image_url=request.image_url)
        response = IngredientsEndpointResponse(
            status=Status.SUCCESSFUL,
            processed_at=datetime.utcnow(),
            request=request,
            response=result,
            error=None,
        )
        mongodb_service.insert_one("ingredients-analyzer", response.model_dump(mode="json"))
        return response
    except Exception as error:
        response = IngredientsEndpointResponse(
            status=Status.FAILED,
            processed_at=datetime.utcnow(),
            request=request,
            response=None,
            error=str(error),
        )
        mongodb_service.insert_one("ingredients-analyzer", response.model_dump(mode="json"))
        return response


@app.post("/nutrients")
def nutrients(request: NutrientsEndpointRequest) -> NutrientsEndpointResponse:
    try:
        result = nutrients_analyzer.analyze(ingredients=request.ingredients)
        response = NutrientsEndpointResponse(
            status=Status.SUCCESSFUL,
            processed_at=datetime.utcnow(),
            request=request,
            response=result,
            error=None,
        )
        mongodb_service.insert_one(
            "nutrients_analyzer-analyzer",
            response.model_dump(mode="json"),
        )
        return response
    except Exception as error:
        response = NutrientsEndpointResponse(
            status=Status.FAILED,
            processed_at=datetime.utcnow(),
            request=request,
            response=None,
            error=str(error),
        )
        mongodb_service.insert_one("nutrients_analyzer", response.model_dump(mode="json"))
        return response