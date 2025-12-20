from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from services.analysis.schemas import IngredientsResponse, Ingredient, NutrientsResponse

class Status(Enum):
    FAILED = 'failed'
    SUCCESSFUL = 'successful'

class IngredientsEndpointRequest(BaseModel):
    image_url: str
    user_id: str

class IngredientsEndpointResponse(BaseModel):
    status: Status
    processed_at: datetime
    request: IngredientsEndpointRequest
    response: IngredientsResponse | None = None
    error: str | None = None

class NutrientsEndpointRequest(BaseModel):
    ingredients: list[Ingredient]
    user_id: str

class NutrientsEndpointResponse(BaseModel):
    status: Status
    processed_at: datetime
    request: NutrientsEndpointRequest
    response: NutrientsResponse | None = None
    error: str | None = None
