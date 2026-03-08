import hashlib
from unittest.mock import MagicMock, patch

import pytest

from services.llm.food_llm import FoodLLM, State
from services.llm.schemas import Ingredient, IngredientsResponse, NutrientsResponse


@patch("services.llm.food_llm.ChatOpenAI")
@patch("services.llm.food_llm.RedisService")
class TestFoodLLM:
    """Unit tests for FoodLLM class."""

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
    def mock_base64_image(self) -> str:
        """Return a mock base64 encoded image string."""
        return "bW9ja19iYXNlNjRfaW1hZ2VfZGF0YQ=="

    def test_build_workflow_compiles_chain(
        self,
        mock_redis_class: MagicMock,
        mock_chat_openai_class: MagicMock,
    ):
        """Test that build_workflow returns a compiled StateGraph."""
        mock_redis_class.return_value.get.return_value = None
        mock_redis_class.return_value.set.return_value = None
        mock_llm = MagicMock()
        mock_structured = MagicMock()
        mock_structured.invoke.return_value = IngredientsResponse(
            name="Test", ingredients=[]
        )
        mock_llm.with_structured_output.return_value = mock_structured
        mock_chat_openai_class.return_value = mock_llm

        food_llm = FoodLLM()

        assert food_llm.chain is not None
        mock_chat_openai_class.assert_called_once()

    @patch("services.llm.food_llm.encode_image_by_url")
    def test_invoke_returns_ingredients_and_nutrients(
        self,
        mock_encode: MagicMock,
        mock_redis_class: MagicMock,
        mock_chat_openai_class: MagicMock,
        sample_ingredients_response: IngredientsResponse,
        sample_nutrients_response: NutrientsResponse,
        mock_base64_image: str,
    ):
        """Test that invoke returns both ingredients_response and nutrients_response."""
        mock_encode.return_value = mock_base64_image
        mock_redis_class.return_value.get.return_value = None
        mock_redis_class.return_value.set.return_value = None

        mock_llm = MagicMock()
        mock_structured = MagicMock()
        mock_structured.invoke.side_effect = [
            sample_ingredients_response,
            sample_nutrients_response,
        ]
        mock_llm.with_structured_output.return_value = mock_structured
        mock_chat_openai_class.return_value = mock_llm

        food_llm = FoodLLM()
        result = food_llm.invoke(image_url="https://example.com/food.jpg")

        assert "ingredients_response" in result
        assert "nutrients_response" in result
        assert result["ingredients_response"] == sample_ingredients_response
        assert result["nutrients_response"] == sample_nutrients_response
        mock_encode.assert_called_once_with("https://example.com/food.jpg")

    @patch("services.llm.food_llm.encode_image_by_url")
    def test_analyze_ingredients_returns_cached_result_when_available(
        self,
        mock_encode: MagicMock,
        mock_redis_class: MagicMock,
        mock_chat_openai_class: MagicMock,
        sample_ingredients_response: IngredientsResponse,
        mock_base64_image: str,
    ):
        """Test that analyze_ingredients returns cached result without calling LLM."""
        mock_encode.return_value = mock_base64_image
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = sample_ingredients_response.model_dump_json()
        mock_redis_instance.set.return_value = None

        mock_llm = MagicMock()
        mock_chat_openai_class.return_value = mock_llm

        food_llm = FoodLLM()
        state: State = {
            "image_url": "https://example.com/food.jpg",
            "ingredients_response": None,
            "nutrients_response": None,
        }
        result = food_llm.analyze_ingredients(state)

        assert result == {"ingredients_response": sample_ingredients_response}
        mock_llm.with_structured_output.assert_not_called()

    @patch("services.llm.food_llm.encode_image_by_url")
    def test_analyze_ingredients_calls_llm_and_caches_on_cache_miss(
        self,
        mock_encode: MagicMock,
        mock_redis_class: MagicMock,
        mock_chat_openai_class: MagicMock,
        sample_ingredients_response: IngredientsResponse,
        mock_base64_image: str,
    ):
        """Test that analyze_ingredients calls LLM and caches when cache misses."""
        mock_encode.return_value = mock_base64_image
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = None
        mock_redis_instance.set.return_value = None

        mock_llm = MagicMock()
        mock_structured = MagicMock()
        mock_structured.invoke.return_value = sample_ingredients_response
        mock_llm.with_structured_output.return_value = mock_structured
        mock_chat_openai_class.return_value = mock_llm

        food_llm = FoodLLM()
        state: State = {
            "image_url": "https://example.com/food.jpg",
            "ingredients_response": None,
            "nutrients_response": None,
        }
        result = food_llm.analyze_ingredients(state)

        assert result["ingredients_response"] == sample_ingredients_response
        mock_llm.with_structured_output.assert_called_once()
        mock_redis_instance.set.assert_called_once()

    @patch("services.llm.food_llm.encode_image_by_url")
    def test_analyze_ingredients_raises_when_encoding_fails(
        self,
        mock_encode: MagicMock,
        mock_redis_class: MagicMock,
        mock_chat_openai_class: MagicMock,
    ):
        """Test that analyze_ingredients raises when image encoding fails."""
        mock_encode.side_effect = Exception("Failed to fetch image")
        mock_redis_class.return_value.get.return_value = None

        mock_llm = MagicMock()
        mock_chat_openai_class.return_value = mock_llm

        food_llm = FoodLLM()
        state: State = {
            "image_url": "https://example.com/bad.jpg",
            "ingredients_response": None,
            "nutrients_response": None,
        }

        with pytest.raises(Exception, match="Failed to fetch image"):
            food_llm.analyze_ingredients(state)

    def test_analyze_nutrients_returns_cached_result_when_available(
        self,
        mock_redis_class: MagicMock,
        mock_chat_openai_class: MagicMock,
        sample_ingredients_response: IngredientsResponse,
        sample_nutrients_response: NutrientsResponse,
    ):
        """Test that analyze_nutrients returns cached result without calling LLM."""
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = sample_nutrients_response.model_dump_json()
        mock_redis_instance.set.return_value = None

        mock_llm = MagicMock()
        mock_chat_openai_class.return_value = mock_llm

        food_llm = FoodLLM()
        state: State = {
            "image_url": "https://example.com/food.jpg",
            "ingredients_response": sample_ingredients_response,
            "nutrients_response": None,
        }
        result = food_llm.analyze_nutrients(state)

        assert result == {"nutrients_response": sample_nutrients_response}
        mock_llm.with_structured_output.assert_not_called()

    def test_analyze_nutrients_calls_llm_on_cache_miss(
        self,
        mock_redis_class: MagicMock,
        mock_chat_openai_class: MagicMock,
        sample_ingredients_response: IngredientsResponse,
        sample_nutrients_response: NutrientsResponse,
    ):
        """Test that analyze_nutrients calls LLM when cache misses."""
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = None
        mock_redis_instance.set.return_value = None

        mock_llm = MagicMock()
        mock_structured = MagicMock()
        mock_structured.invoke.return_value = sample_nutrients_response
        mock_llm.with_structured_output.return_value = mock_structured
        mock_chat_openai_class.return_value = mock_llm

        food_llm = FoodLLM()
        state: State = {
            "image_url": "https://example.com/food.jpg",
            "ingredients_response": sample_ingredients_response,
            "nutrients_response": None,
        }
        result = food_llm.analyze_nutrients(state)

        assert result["nutrients_response"] == sample_nutrients_response
        mock_llm.with_structured_output.assert_called_once()
        mock_redis_instance.set.assert_called_once()

    @patch("services.llm.food_llm.encode_image_by_url")
    def test_ingredients_cache_key_based_on_image_hash(
        self,
        mock_encode: MagicMock,
        mock_redis_class: MagicMock,
        mock_chat_openai_class: MagicMock,
        sample_ingredients_response: IngredientsResponse,
        mock_base64_image: str,
    ):
        """Test that ingredients cache key is derived from image hash."""
        mock_encode.return_value = mock_base64_image
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = sample_ingredients_response.model_dump_json()
        mock_redis_instance.set.return_value = None

        mock_llm = MagicMock()
        mock_chat_openai_class.return_value = mock_llm

        food_llm = FoodLLM()
        expected_key = f"ingredients:{hashlib.sha256(mock_base64_image.encode()).hexdigest()}"

        state: State = {
            "image_url": "https://example.com/food.jpg",
            "ingredients_response": None,
            "nutrients_response": None,
        }
        food_llm.analyze_ingredients(state)

        mock_redis_instance.get.assert_called_once_with(expected_key)
