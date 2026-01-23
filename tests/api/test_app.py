from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from services.analysis.schemas import Ingredient, IngredientsResponse, NutrientsResponse


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


class TestIngredientsEndpoint:
    """Tests for the ingredients analysis endpoint."""

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
    def valid_ingredients_request(self) -> dict:
        """Create a valid request payload."""
        return {
            "image_url": "https://example.com/food.jpg",
            "user_id": "user123",
        }

    @patch("api.app.ingredients_analyzer")
    def test_successful_analysis_returns_successful_status(
        self,
        mock_analyzer: MagicMock,
        sample_ingredients_response: IngredientsResponse,
        valid_ingredients_request: dict,
    ):
        """Test that successful analysis returns SUCCESSFUL status."""
        mock_analyzer.analyze.return_value = sample_ingredients_response

        from api.app import app

        client = TestClient(app)

        response = client.post("/ingredients", json=valid_ingredients_request)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "successful"
        assert data["error"] is None
        assert data["response"]["name"] == "Caesar Salad"
        assert len(data["response"]["ingredients"]) == 2
        assert data["request"] == valid_ingredients_request
        assert "processed_at" in data

    @patch("api.app.ingredients_analyzer")
    def test_failed_analysis_returns_failed_status(
        self,
        mock_analyzer: MagicMock,
        valid_ingredients_request: dict,
    ):
        """Test that failed analysis returns FAILED status with error message."""
        mock_analyzer.analyze.side_effect = Exception("Image processing failed")

        from api.app import app

        client = TestClient(app)

        response = client.post("/ingredients", json=valid_ingredients_request)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "failed"
        assert data["error"] == "Image processing failed"
        assert data["response"] is None
        assert data["request"] == valid_ingredients_request

    def test_missing_image_url_returns_validation_error(self):
        """Test that missing image_url returns 422 validation error."""
        from api.app import app

        client = TestClient(app)

        response = client.post("/ingredients", json={"user_id": "user123"})

        assert response.status_code == 422

    def test_missing_user_id_returns_validation_error(self):
        """Test that missing user_id returns 422 validation error."""
        from api.app import app

        client = TestClient(app)

        response = client.post(
            "/ingredients", json={"image_url": "https://example.com/food.jpg"}
        )

        assert response.status_code == 422

    def test_empty_body_returns_validation_error(self):
        """Test that empty request body returns 422 validation error."""
        from api.app import app

        client = TestClient(app)

        response = client.post("/ingredients", json={})

        assert response.status_code == 422

    @patch("api.app.ingredients_analyzer")
    def test_analyzer_called_with_correct_image_url(
        self,
        mock_analyzer: MagicMock,
        sample_ingredients_response: IngredientsResponse,
        valid_ingredients_request: dict,
    ):
        """Test that analyzer is called with the correct image URL."""
        mock_analyzer.analyze.return_value = sample_ingredients_response

        from api.app import app

        client = TestClient(app)

        client.post("/ingredients", json=valid_ingredients_request)

        mock_analyzer.analyze.assert_called_once_with(
            image_url="https://example.com/food.jpg"
        )


class TestNutrientsEndpoint:
    """Tests for the nutrients analysis endpoint."""

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
    def valid_nutrients_request(self) -> dict:
        """Create a valid request payload."""
        return {
            "ingredients": [
                {"ingredient_name": "Chicken breast", "portion": "150g"},
                {"ingredient_name": "Brown rice", "portion": "150g"},
            ],
            "user_id": "user123",
        }

    @patch("api.app.nutrients_analyzer")
    def test_successful_analysis_returns_successful_status(
        self,
        mock_analyzer: MagicMock,
        sample_nutrients_response: NutrientsResponse,
        valid_nutrients_request: dict,
    ):
        """Test that successful analysis returns SUCCESSFUL status."""
        mock_analyzer.analyze.return_value = sample_nutrients_response

        from api.app import app

        client = TestClient(app)

        response = client.post("/nutrients", json=valid_nutrients_request)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "successful"
        assert data["error"] is None
        assert data["response"]["total_calories"] == 450
        assert data["response"]["total_protein_g"] == 42.5
        assert data["response"]["total_carbohydrates_g"] == 55.0
        assert data["response"]["total_fats_g"] == 8.5
        assert data["response"]["total_fiber_g"] == 6.0
        assert data["request"] == valid_nutrients_request
        assert "processed_at" in data

    @patch("api.app.nutrients_analyzer")
    def test_failed_analysis_returns_failed_status(
        self,
        mock_analyzer: MagicMock,
        valid_nutrients_request: dict,
    ):
        """Test that failed analysis returns FAILED status with error message."""
        mock_analyzer.analyze.side_effect = Exception("Nutrient analysis failed")

        from api.app import app

        client = TestClient(app)

        response = client.post("/nutrients", json=valid_nutrients_request)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "failed"
        assert data["error"] == "Nutrient analysis failed"
        assert data["response"] is None
        assert data["request"] == valid_nutrients_request

    def test_missing_ingredients_returns_validation_error(self):
        """Test that missing ingredients returns 422 validation error."""
        from api.app import app

        client = TestClient(app)

        response = client.post("/nutrients", json={"user_id": "user123"})

        assert response.status_code == 422

    def test_missing_user_id_returns_validation_error(self):
        """Test that missing user_id returns 422 validation error."""
        from api.app import app

        client = TestClient(app)

        response = client.post(
            "/nutrients",
            json={
                "ingredients": [
                    {"ingredient_name": "Chicken", "portion": "100g"},
                ]
            },
        )

        assert response.status_code == 422

    def test_empty_body_returns_validation_error(self):
        """Test that empty request body returns 422 validation error."""
        from api.app import app

        client = TestClient(app)

        response = client.post("/nutrients", json={})

        assert response.status_code == 422

    def test_invalid_ingredient_format_returns_validation_error(self):
        """Test that invalid ingredient format returns 422 validation error."""
        from api.app import app

        client = TestClient(app)

        response = client.post(
            "/nutrients",
            json={
                "ingredients": [{"invalid_field": "value"}],
                "user_id": "user123",
            },
        )

        assert response.status_code == 422

    @patch("api.app.nutrients_analyzer")
    def test_empty_ingredients_list_is_valid(
        self,
        mock_analyzer: MagicMock,
        sample_nutrients_response: NutrientsResponse,
    ):
        """Test that empty ingredients list is a valid request."""
        mock_analyzer.analyze.return_value = sample_nutrients_response

        from api.app import app

        client = TestClient(app)

        response = client.post(
            "/nutrients",
            json={"ingredients": [], "user_id": "user123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "successful"

    @patch("api.app.nutrients_analyzer")
    def test_analyzer_called_with_correct_ingredients(
        self,
        mock_analyzer: MagicMock,
        sample_nutrients_response: NutrientsResponse,
        valid_nutrients_request: dict,
    ):
        """Test that analyzer is called with the correct ingredients."""
        mock_analyzer.analyze.return_value = sample_nutrients_response

        from api.app import app

        client = TestClient(app)

        client.post("/nutrients", json=valid_nutrients_request)

        # Verify analyze was called
        mock_analyzer.analyze.assert_called_once()
        # Get the ingredients argument
        call_kwargs = mock_analyzer.analyze.call_args.kwargs
        ingredients = call_kwargs["ingredients"]
        assert len(ingredients) == 2
        assert ingredients[0].ingredient_name == "Chicken breast"
        assert ingredients[0].portion == "150g"
        assert ingredients[1].ingredient_name == "Brown rice"
        assert ingredients[1].portion == "150g"
