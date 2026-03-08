from contextlib import asynccontextmanager
from datetime import datetime

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, HTTPException, status
from loguru import logger

from api.schemas import (
    FoodAnalysisEndpointRequest,
    FoodAnalysisEndpointResponse,
    Status,
)
from services.database.client import MongoDBService
from services.llm.food_llm import FoodLLM

load_dotenv(find_dotenv())
food_llm = None
mongodb_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI app.
    Handles startup and shutdown of the app.
    """
    try:
        global food_llm, mongodb_service
        food_llm = FoodLLM()
        mongodb_service = MongoDBService()
    except Exception as error:
        logger.error(f"Error starting the app: {error}")
        raise
    yield
    # Shutdown the app.


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Welcome to the Food Image Analyzer API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/food-analysis")
def food_analysis(request: FoodAnalysisEndpointRequest) -> FoodAnalysisEndpointResponse:
    try:
        result = food_llm.invoke(image_url=request.image_url)
        response = FoodAnalysisEndpointResponse(
            status=Status.SUCCESSFUL,
            processed_at=datetime.utcnow(),
            request=request,
            ingredients_response=result.get("ingredients_response"),
            nutrients_response=result.get("nutrients_response"),
            error=None,
        )
        mongodb_service.insert_one("analysis-results", response.model_dump(mode="json"))
        return response
    except Exception as error:
        response = FoodAnalysisEndpointResponse(
            status=Status.FAILED,
            processed_at=datetime.utcnow(),
            request=request,
            ingredients_response=None,
            nutrients_response=None,
            error=str(error),
        )
        mongodb_service.insert_one("analysis-results", response.model_dump(mode="json"))
        logger.error(f"Error analyzing food image: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
