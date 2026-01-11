import hashlib
from unittest.mock import MagicMock, patch

import pytest

from services.analysis.ingredients import IngredientsAnalyzer
from services.analysis.schemas import Ingredient, IngredientsResponse


class TestIngredientsAnalyzer:
    """Unit tests for IngredientsAnalyzer class."""

    @pytest.fixture
    def sample_ingredients_response(self) -> IngredientsResponse:
        """Create a sample IngredientsResponse for testing."""
        return IngredientsResponse(
            name="Caesar Salad",
            ingredients=[
                Ingredient(ingredient_name="Romaine lettuce", portiont="2 cups"),
                Ingredient(ingredient_name="Parmesan cheese", portiont="1/4 cup"),
                Ingredient(ingredient_name="Croutons", portiont="1/2 cup"),
            ],
        )

    @pytest.fixture
    def mock_base64_image(self) -> str:
        """Return a mock base64 encoded image string."""
        return "bW9ja19iYXNlNjRfaW1hZ2VfZGF0YQ=="

    @pytest.fixture
    def expected_cache_key(self, mock_base64_image: str) -> str:
        """Return the expected cache key for the mock image."""
        image_hash = hashlib.sha256(mock_base64_image.encode()).hexdigest()
        return f"ingredients:{image_hash}"

    @patch("services.analysis.ingredients.encode_image_by_url")
    @patch("services.analysis.ingredients.RedisService")
    @patch("services.analysis.ingredients.ChatGPT")
    def test_returns_cached_result_when_available(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        mock_encode: MagicMock,
        sample_ingredients_response: IngredientsResponse,
        mock_base64_image: str,
        expected_cache_key: str,
    ):
        """Test that cached results are returned without calling ChatGPT."""
        # Arrange
        image_url = "http://example.com/food.jpg"
        mock_encode.return_value = mock_base64_image
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = sample_ingredients_response.model_dump_json()
        mock_chatgpt_instance = mock_chatgpt_class.return_value

        analyzer = IngredientsAnalyzer()

        # Act
        result = analyzer.analyze(image_url)

        # Assert
        mock_encode.assert_called_once_with(image_url)
        mock_redis_instance.get.assert_called_once_with(expected_cache_key)
        mock_chatgpt_instance.generate_image_response_by_base64_image.assert_not_called()
        mock_redis_instance.set.assert_not_called()
        assert result == sample_ingredients_response

    @patch("services.analysis.ingredients.encode_image_by_url")
    @patch("services.analysis.ingredients.RedisService")
    @patch("services.analysis.ingredients.ChatGPT")
    def test_calls_chatgpt_and_caches_result_on_cache_miss(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        mock_encode: MagicMock,
        sample_ingredients_response: IngredientsResponse,
        mock_base64_image: str,
        expected_cache_key: str,
    ):
        """Test that ChatGPT is called and result is cached when cache misses."""
        # Arrange
        image_url = "http://example.com/food.jpg"
        mock_encode.return_value = mock_base64_image
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = None  # Cache miss

        mock_chatgpt_instance = mock_chatgpt_class.return_value
        mock_chatgpt_instance.generate_image_response_by_base64_image.return_value = (
            sample_ingredients_response
        )

        analyzer = IngredientsAnalyzer()

        # Act
        result = analyzer.analyze(image_url)

        # Assert
        mock_encode.assert_called_once_with(image_url)
        mock_redis_instance.get.assert_called_once_with(expected_cache_key)
        mock_chatgpt_instance.generate_image_response_by_base64_image.assert_called_once()
        mock_redis_instance.set.assert_called_once_with(
            expected_cache_key, sample_ingredients_response.model_dump_json()
        )
        assert result == sample_ingredients_response

    @patch("services.analysis.ingredients.encode_image_by_url")
    @patch("services.analysis.ingredients.RedisService")
    @patch("services.analysis.ingredients.ChatGPT")
    def test_chatgpt_called_with_correct_parameters(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        mock_encode: MagicMock,
        sample_ingredients_response: IngredientsResponse,
        mock_base64_image: str,
    ):
        """Test that ChatGPT is called with the correct prompts and parameters."""
        # Arrange
        from services.chat_gpt.config import DEFAULT_CHATGPT_MODEL
        from services.prompts import FoodImageAnalyzerPrompts

        image_url = "http://example.com/food.jpg"
        mock_encode.return_value = mock_base64_image
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = None

        mock_chatgpt_instance = mock_chatgpt_class.return_value
        mock_chatgpt_instance.generate_image_response_by_base64_image.return_value = (
            sample_ingredients_response
        )

        analyzer = IngredientsAnalyzer()

        # Act
        analyzer.analyze(image_url)

        # Assert
        mock_chatgpt_instance.generate_image_response_by_base64_image.assert_called_once_with(
            model=DEFAULT_CHATGPT_MODEL,
            system_prompt=FoodImageAnalyzerPrompts.INGREDIENTS_SYSTEM_PROMPT,
            user_prompt=FoodImageAnalyzerPrompts.INGREDIENTS_USER_PROMPT,
            base64_image=mock_base64_image,
            response_format=IngredientsResponse,
        )

    @patch("services.analysis.ingredients.encode_image_by_url")
    @patch("services.analysis.ingredients.RedisService")
    @patch("services.analysis.ingredients.ChatGPT")
    def test_same_image_produces_same_cache_key(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        mock_encode: MagicMock,
        sample_ingredients_response: IngredientsResponse,
        mock_base64_image: str,
    ):
        """Test that the same image always produces the same cache key."""
        # Arrange
        mock_encode.return_value = mock_base64_image
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = sample_ingredients_response.model_dump_json()

        analyzer = IngredientsAnalyzer()

        # Act - Call analyze twice with different URLs but same image content
        analyzer.analyze("http://example.com/food.jpg")
        analyzer.analyze("http://different-url.com/same-image.jpg")

        # Assert - Both calls should use the same cache key
        cache_key_calls = mock_redis_instance.get.call_args_list
        assert len(cache_key_calls) == 2
        assert cache_key_calls[0] == cache_key_calls[1]

    @patch("services.analysis.ingredients.encode_image_by_url")
    @patch("services.analysis.ingredients.RedisService")
    @patch("services.analysis.ingredients.ChatGPT")
    def test_different_images_produce_different_cache_keys(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        mock_encode: MagicMock,
        sample_ingredients_response: IngredientsResponse,
    ):
        """Test that different images produce different cache keys."""
        # Arrange
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = sample_ingredients_response.model_dump_json()

        # Return different base64 for different calls
        mock_encode.side_effect = ["image_data_1", "image_data_2"]

        analyzer = IngredientsAnalyzer()

        # Act
        analyzer.analyze("http://example.com/food1.jpg")
        analyzer.analyze("http://example.com/food2.jpg")

        # Assert
        cache_key_calls = mock_redis_instance.get.call_args_list
        assert len(cache_key_calls) == 2
        assert cache_key_calls[0] != cache_key_calls[1]

    @patch("services.analysis.ingredients.encode_image_by_url")
    @patch("services.analysis.ingredients.RedisService")
    @patch("services.analysis.ingredients.ChatGPT")
    def test_raises_exception_when_image_encoding_fails(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        mock_encode: MagicMock,
    ):
        """Test that exceptions from image encoding are propagated."""
        # Arrange
        mock_encode.side_effect = Exception("Failed to fetch image")

        analyzer = IngredientsAnalyzer()

        # Act & Assert
        with pytest.raises(Exception, match="Failed to fetch image"):
            analyzer.analyze("http://example.com/bad-url.jpg")

    @patch("services.analysis.ingredients.encode_image_by_url")
    @patch("services.analysis.ingredients.RedisService")
    @patch("services.analysis.ingredients.ChatGPT")
    def test_raises_exception_when_chatgpt_fails(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        mock_encode: MagicMock,
        mock_base64_image: str,
    ):
        """Test that exceptions from ChatGPT are propagated."""
        # Arrange
        mock_encode.return_value = mock_base64_image
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = None

        mock_chatgpt_instance = mock_chatgpt_class.return_value
        mock_chatgpt_instance.generate_image_response_by_base64_image.side_effect = Exception(
            "OpenAI API error"
        )

        analyzer = IngredientsAnalyzer()

        # Act & Assert
        with pytest.raises(Exception, match="OpenAI API error"):
            analyzer.analyze("http://example.com/food.jpg")

    @patch("services.analysis.ingredients.encode_image_by_url")
    @patch("services.analysis.ingredients.RedisService")
    @patch("services.analysis.ingredients.ChatGPT")
    def test_raises_exception_when_redis_get_fails(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        mock_encode: MagicMock,
        mock_base64_image: str,
    ):
        """Test that exceptions from Redis get are propagated."""
        # Arrange
        mock_encode.return_value = mock_base64_image
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.side_effect = Exception("Redis connection error")

        analyzer = IngredientsAnalyzer()

        # Act & Assert
        with pytest.raises(Exception, match="Redis connection error"):
            analyzer.analyze("http://example.com/food.jpg")

    @patch("services.analysis.ingredients.encode_image_by_url")
    @patch("services.analysis.ingredients.RedisService")
    @patch("services.analysis.ingredients.ChatGPT")
    def test_cached_response_is_properly_deserialized(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        mock_encode: MagicMock,
        sample_ingredients_response: IngredientsResponse,
        mock_base64_image: str,
    ):
        """Test that cached JSON is properly deserialized to IngredientsResponse."""
        # Arrange
        mock_encode.return_value = mock_base64_image
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = sample_ingredients_response.model_dump_json()

        analyzer = IngredientsAnalyzer()

        # Act
        result = analyzer.analyze("http://example.com/food.jpg")

        # Assert
        assert isinstance(result, IngredientsResponse)
        assert result.name == "Caesar Salad"
        assert len(result.ingredients) == 3
        assert result.ingredients[0].ingredient_name == "Romaine lettuce"
        assert result.ingredients[0].portiont == "2 cups"

