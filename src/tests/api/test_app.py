from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from services.llm.schemas import Ingredient, IngredientsResponse, NutrientsResponse


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_returns_welcome_message(self):
        """Test that root endpoint returns welcome message."""
        from api.app import app

        client = TestClient(app)

        response = client.get("/")

        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Food Image Analyzer API"}


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_returns_healthy_status(self):
        """Test that health endpoint returns healthy status."""
        from api.app import app

        client = TestClient(app)

        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestFoodAnalysisEndpoint:
    """Tests for the food analysis endpoint."""

    @pytest.fixture
    def sample_ingredients_response(self) -> IngredientsResponse:
        """Create a sample IngredientsResponse for testing."""
        return IngredientsResponse(
            name="Caesar Salad",
            ingredients=[
                Ingredient(ingredient_name="Romaine lettuce", portion="200g"),
                Ingredient(ingredient_name="Parmesan cheese", portion="30g"),
            ],
        )

    @pytest.fixture
    def sample_nutrients_response(self) -> NutrientsResponse:
        """Create a sample NutrientsResponse for testing."""
        return NutrientsResponse(
            total_calories=450,
            total_protein_g=42.5,
            total_carbohydrates_g=55.0,
            total_fats_g=8.5,
            total_fiber_g=6.0,
        )

    @pytest.fixture
    def valid_food_analysis_request(self) -> dict:
        """Create a valid request payload."""
        return {
            "image_url": "https://example.com/food.jpg",
        }

    @patch("api.app.mongodb_service", MagicMock())
    @patch("api.app.food_llm")
    def test_successful_analysis_returns_successful_status(
        self,
        mock_food_llm: MagicMock,
        sample_ingredients_response: IngredientsResponse,
        sample_nutrients_response: NutrientsResponse,
        valid_food_analysis_request: dict,
    ):
        """Test that successful analysis returns SUCCESSFUL status."""
        mock_food_llm.invoke.return_value = {
            "ingredients_response": sample_ingredients_response,
            "nutrients_response": sample_nutrients_response,
        }

        from api.app import app

        client = TestClient(app)

        response = client.post("/food-analysis", json=valid_food_analysis_request)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "successful"
        assert data["error"] is None
        assert data["ingredients_response"]["name"] == "Caesar Salad"
        assert len(data["ingredients_response"]["ingredients"]) == 2
        assert data["nutrients_response"]["total_calories"] == 450
        assert data["request"] == valid_food_analysis_request
        assert "processed_at" in data

    @patch("api.app.mongodb_service", MagicMock())
    @patch("api.app.food_llm")
    def test_failed_analysis_returns_500(
        self,
        mock_food_llm: MagicMock,
        valid_food_analysis_request: dict,
    ):
        """Test that failed analysis returns 500 with error detail."""
        mock_food_llm.invoke.side_effect = Exception("Image processing failed")

        from api.app import app

        client = TestClient(app)

        response = client.post("/food-analysis", json=valid_food_analysis_request)

        assert response.status_code == 500
        assert "Image processing failed" in response.json().get("detail", "")

    def test_missing_image_url_returns_validation_error(self):
        """Test that missing image_url returns 422 validation error."""
        from api.app import app

        client = TestClient(app)

        response = client.post("/food-analysis", json={})

        assert response.status_code == 422

    def test_empty_body_returns_validation_error(self):
        """Test that empty request body returns 422 validation error."""
        from api.app import app

        client = TestClient(app)

        response = client.post("/food-analysis", json={})

        assert response.status_code == 422

    @patch("api.app.mongodb_service", MagicMock())
    @patch("api.app.food_llm")
    def test_food_llm_called_with_correct_image_url(
        self,
        mock_food_llm: MagicMock,
        sample_ingredients_response: IngredientsResponse,
        sample_nutrients_response: NutrientsResponse,
        valid_food_analysis_request: dict,
    ):
        """Test that food_llm.invoke is called with the correct image URL."""
        mock_food_llm.invoke.return_value = {
            "ingredients_response": sample_ingredients_response,
            "nutrients_response": sample_nutrients_response,
        }

        from api.app import app

        client = TestClient(app)

        client.post("/food-analysis", json=valid_food_analysis_request)

        mock_food_llm.invoke.assert_called_once_with(
            image_url="https://example.com/food.jpg"
        )
