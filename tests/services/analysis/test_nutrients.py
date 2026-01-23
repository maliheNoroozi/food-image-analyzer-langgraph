from unittest.mock import MagicMock, patch

import pytest

from services.analysis.nutrients import NutrientsAnalyzer
from services.analysis.schemas import Ingredient, NutrientsResponse


class TestNutrientsAnalyzer:
    """Unit tests for NutrientsAnalyzer class."""

    @pytest.fixture
    def sample_ingredients(self) -> list[Ingredient]:
        """Create sample ingredients for testing."""
        return [
            Ingredient(ingredient_name="Chicken breast", portion="150g"),
            Ingredient(ingredient_name="Brown rice", portion="150g"),
            Ingredient(ingredient_name="Broccoli", portion="100g"),
        ]

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
    def expected_cache_key(self, sample_ingredients: list[Ingredient]) -> str:
        """Return the expected cache key for the sample ingredients."""
        ingredients_key = "_".join(
            [f"{i.ingredient_name}:{i.portion}" for i in sample_ingredients]
        )
        return f"nutrients:{ingredients_key}"

    @patch("services.analysis.nutrients.RedisService")
    @patch("services.analysis.nutrients.ChatGPT")
    def test_returns_cached_result_when_available(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        sample_ingredients: list[Ingredient],
        sample_nutrients_response: NutrientsResponse,
        expected_cache_key: str,
    ):
        """Test that cached results are returned without calling ChatGPT."""
        # Arrange
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = sample_nutrients_response.model_dump_json()
        mock_chatgpt_instance = mock_chatgpt_class.return_value

        analyzer = NutrientsAnalyzer()

        # Act
        result = analyzer.analyze(sample_ingredients)

        # Assert
        mock_redis_instance.get.assert_called_once_with(expected_cache_key)
        mock_chatgpt_instance.generate_parsed_response.assert_not_called()
        mock_redis_instance.set.assert_not_called()
        assert result == sample_nutrients_response

    @patch("services.analysis.nutrients.RedisService")
    @patch("services.analysis.nutrients.ChatGPT")
    def test_calls_chatgpt_and_caches_result_on_cache_miss(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        sample_ingredients: list[Ingredient],
        sample_nutrients_response: NutrientsResponse,
        expected_cache_key: str,
    ):
        """Test that ChatGPT is called and result is cached when cache misses."""
        # Arrange
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = None  # Cache miss

        mock_chatgpt_instance = mock_chatgpt_class.return_value
        mock_chatgpt_instance.generate_parsed_response.return_value = (
            sample_nutrients_response
        )

        analyzer = NutrientsAnalyzer()

        # Act
        result = analyzer.analyze(sample_ingredients)

        # Assert
        mock_redis_instance.get.assert_called_once_with(expected_cache_key)
        mock_chatgpt_instance.generate_parsed_response.assert_called_once()
        mock_redis_instance.set.assert_called_once_with(
            expected_cache_key, sample_nutrients_response.model_dump_json()
        )
        assert result == sample_nutrients_response

    @patch("services.analysis.nutrients.RedisService")
    @patch("services.analysis.nutrients.ChatGPT")
    def test_chatgpt_called_with_correct_parameters(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        sample_ingredients: list[Ingredient],
        sample_nutrients_response: NutrientsResponse,
    ):
        """Test that ChatGPT is called with the correct prompts and parameters."""
        # Arrange
        from services.chat_gpt.config import DEFAULT_CHATGPT_MODEL
        from services.prompts import FoodImageAnalyzerPrompts

        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = None

        mock_chatgpt_instance = mock_chatgpt_class.return_value
        mock_chatgpt_instance.generate_parsed_response.return_value = (
            sample_nutrients_response
        )

        analyzer = NutrientsAnalyzer()

        # Act
        analyzer.analyze(sample_ingredients)

        # Assert
        ingredients_str = "\n".join([str(ingredient) for ingredient in sample_ingredients])
        expected_user_prompt = FoodImageAnalyzerPrompts.NUTRIENT_USER_PROMPT.format(
            ingredients_list=ingredients_str
        )
        mock_chatgpt_instance.generate_parsed_response.assert_called_once_with(
            model=DEFAULT_CHATGPT_MODEL,
            system_prompt=FoodImageAnalyzerPrompts.NUTRIENT_SYSTEM_PROMPT,
            user_prompt=expected_user_prompt,
            response_format=NutrientsResponse,
        )

    @patch("services.analysis.nutrients.RedisService")
    @patch("services.analysis.nutrients.ChatGPT")
    def test_same_ingredients_produce_same_cache_key(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        sample_ingredients: list[Ingredient],
        sample_nutrients_response: NutrientsResponse,
    ):
        """Test that the same ingredients always produce the same cache key."""
        # Arrange
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = sample_nutrients_response.model_dump_json()

        analyzer = NutrientsAnalyzer()

        # Act - Call analyze twice with the same ingredients
        analyzer.analyze(sample_ingredients)
        analyzer.analyze(sample_ingredients)

        # Assert - Both calls should use the same cache key
        cache_key_calls = mock_redis_instance.get.call_args_list
        assert len(cache_key_calls) == 2
        assert cache_key_calls[0] == cache_key_calls[1]

    @patch("services.analysis.nutrients.RedisService")
    @patch("services.analysis.nutrients.ChatGPT")
    def test_different_ingredients_produce_different_cache_keys(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        sample_nutrients_response: NutrientsResponse,
    ):
        """Test that different ingredients produce different cache keys."""
        # Arrange
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = sample_nutrients_response.model_dump_json()

        ingredients_1 = [
            Ingredient(ingredient_name="Chicken", portion="100g"),
        ]
        ingredients_2 = [
            Ingredient(ingredient_name="Beef", portion="100g"),
        ]

        analyzer = NutrientsAnalyzer()

        # Act
        analyzer.analyze(ingredients_1)
        analyzer.analyze(ingredients_2)

        # Assert
        cache_key_calls = mock_redis_instance.get.call_args_list
        assert len(cache_key_calls) == 2
        assert cache_key_calls[0] != cache_key_calls[1]

    @patch("services.analysis.nutrients.RedisService")
    @patch("services.analysis.nutrients.ChatGPT")
    def test_raises_exception_when_chatgpt_fails(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        sample_ingredients: list[Ingredient],
    ):
        """Test that exceptions from ChatGPT are propagated."""
        # Arrange
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = None

        mock_chatgpt_instance = mock_chatgpt_class.return_value
        mock_chatgpt_instance.generate_parsed_response.side_effect = Exception(
            "OpenAI API error"
        )

        analyzer = NutrientsAnalyzer()

        # Act & Assert
        with pytest.raises(Exception, match="OpenAI API error"):
            analyzer.analyze(sample_ingredients)

    @patch("services.analysis.nutrients.RedisService")
    @patch("services.analysis.nutrients.ChatGPT")
    def test_raises_exception_when_redis_get_fails(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        sample_ingredients: list[Ingredient],
    ):
        """Test that Redis get failures fall back to ChatGPT."""
        # Arrange
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.side_effect = Exception("Redis connection error")
        mock_chatgpt_instance = mock_chatgpt_class.return_value
        mock_chatgpt_instance.generate_parsed_response.return_value = NutrientsResponse(
            total_calories=100,
            total_protein_g=10.0,
            total_carbohydrates_g=5.0,
            total_fats_g=2.0,
            total_fiber_g=1.0,
        )

        analyzer = NutrientsAnalyzer()

        # Act
        result = analyzer.analyze(sample_ingredients)

        # Assert
        mock_chatgpt_instance.generate_parsed_response.assert_called_once()
        mock_redis_instance.set.assert_called_once()
        assert isinstance(result, NutrientsResponse)

    @patch("services.analysis.nutrients.RedisService")
    @patch("services.analysis.nutrients.ChatGPT")
    def test_raises_exception_when_redis_set_fails(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        sample_ingredients: list[Ingredient],
        sample_nutrients_response: NutrientsResponse,
    ):
        """Test that Redis set failures do not prevent responses."""
        # Arrange
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = None
        mock_redis_instance.set.side_effect = Exception("Redis write error")

        mock_chatgpt_instance = mock_chatgpt_class.return_value
        mock_chatgpt_instance.generate_parsed_response.return_value = (
            sample_nutrients_response
        )

        analyzer = NutrientsAnalyzer()

        # Act
        result = analyzer.analyze(sample_ingredients)

        # Assert
        assert result == sample_nutrients_response

    @patch("services.analysis.nutrients.RedisService")
    @patch("services.analysis.nutrients.ChatGPT")
    def test_cached_response_is_properly_deserialized(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        sample_ingredients: list[Ingredient],
        sample_nutrients_response: NutrientsResponse,
    ):
        """Test that cached JSON is properly deserialized to NutrientsResponse."""
        # Arrange
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = sample_nutrients_response.model_dump_json()

        analyzer = NutrientsAnalyzer()

        # Act
        result = analyzer.analyze(sample_ingredients)

        # Assert
        assert isinstance(result, NutrientsResponse)
        assert result.total_calories == 450
        assert result.total_protein_g == 42.5
        assert result.total_carbohydrates_g == 55.0
        assert result.total_fats_g == 8.5
        assert result.total_fiber_g == 6.0

    @patch("services.analysis.nutrients.RedisService")
    @patch("services.analysis.nutrients.ChatGPT")
    def test_empty_ingredients_list(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
    ):
        """Test behavior with an empty ingredients list."""
        # Arrange
        empty_response = NutrientsResponse(
            total_calories=0,
            total_protein_g=0.0,
            total_carbohydrates_g=0.0,
            total_fats_g=0.0,
            total_fiber_g=0.0,
        )
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = None

        mock_chatgpt_instance = mock_chatgpt_class.return_value
        mock_chatgpt_instance.generate_parsed_response.return_value = empty_response

        analyzer = NutrientsAnalyzer()

        # Act
        result = analyzer.analyze([])

        # Assert
        mock_redis_instance.get.assert_called_once_with("nutrients:")
        assert result == empty_response

    @patch("services.analysis.nutrients.RedisService")
    @patch("services.analysis.nutrients.ChatGPT")
    def test_ingredients_order_affects_cache_key(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
        sample_nutrients_response: NutrientsResponse,
    ):
        """Test that ingredient order affects the cache key."""
        # Arrange
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = sample_nutrients_response.model_dump_json()

        ingredients_order_1 = [
            Ingredient(ingredient_name="Chicken", portion="100g"),
            Ingredient(ingredient_name="Rice", portion="150g"),
        ]
        ingredients_order_2 = [
            Ingredient(ingredient_name="Rice", portion="150g"),
            Ingredient(ingredient_name="Chicken", portion="100g"),
        ]

        analyzer = NutrientsAnalyzer()

        # Act
        analyzer.analyze(ingredients_order_1)
        analyzer.analyze(ingredients_order_2)

        # Assert - Different order should produce different cache keys
        cache_key_calls = mock_redis_instance.get.call_args_list
        assert len(cache_key_calls) == 2
        assert cache_key_calls[0] != cache_key_calls[1]

    @patch("services.analysis.nutrients.RedisService")
    @patch("services.analysis.nutrients.ChatGPT")
    def test_single_ingredient(
        self,
        mock_chatgpt_class: MagicMock,
        mock_redis_class: MagicMock,
    ):
        """Test analysis with a single ingredient."""
        # Arrange
        single_ingredient = [Ingredient(ingredient_name="Apple", portion="1 medium")]
        expected_response = NutrientsResponse(
            total_calories=95,
            total_protein_g=0.5,
            total_carbohydrates_g=25.0,
            total_fats_g=0.3,
            total_fiber_g=4.4,
        )
        mock_redis_instance = mock_redis_class.return_value
        mock_redis_instance.get.return_value = None

        mock_chatgpt_instance = mock_chatgpt_class.return_value
        mock_chatgpt_instance.generate_parsed_response.return_value = expected_response

        analyzer = NutrientsAnalyzer()

        # Act
        result = analyzer.analyze(single_ingredient)

        # Assert
        mock_redis_instance.get.assert_called_once_with("nutrients:Apple:1 medium")
        assert result == expected_response
