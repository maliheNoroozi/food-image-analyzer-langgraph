import sys
from datetime import datetime
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import opik
from services.opik_tracing.configure import configure_opik
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
load_dotenv(find_dotenv())  # Must run BEFORE importing opik
configure_opik()
app = FastAPI()
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
