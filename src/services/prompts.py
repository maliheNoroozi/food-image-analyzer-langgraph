class MealScannerPrompts:
    INGREDIENTS_SYSTEM_PROMPT = """
You are a helpful assistant that analyzes food images to extract meal names and ingredients with their portions.
"""

    INGREDIENTS_USER_PROMPT = """
Analyze the image, meal name, extract any ingredients, and estimate their portions.
"""

    NUTRIENT_SYSTEM_PROMPT = """
You are a helpful assistant that analyzes food ingredients and their portions and estimates their nutritional values.
"""

    NUTRIENT_USER_PROMPT = """
Analyze the foloowing ingredients and and their portions and estimate the following:
- Total Calories
- Total Protein in grams
- Total Carbohydrates in grams
- Total Fats in grams
- Total Fiber in grams

Ingredients:
{ingredients_list}
"""
