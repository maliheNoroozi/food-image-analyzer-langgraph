class FoodImageAnalyzerPrompts:
    INGREDIENTS_SYSTEM_PROMPT = """
You are a helpful assistant that analyzes food images to extract food names and ingredients with their portions.
"""

    INGREDIENTS_USER_PROMPT = """
Analyze the image, food names, extract any ingredients, and estimate their portions.
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

    SCORE_INGREDIENTS_SYSTEM_PROMPT = """
You are a helpful assistant that scores the accuracy of the ingredients extracted from a food image.
"""

    SCORE_INGREDIENTS_USER_PROMPT = """
Score the accuracy of the ingredients extracted from a food image.
The ingredients are:
{ingredients_list}
The expected ingredients are:
{expected_ingredients_list}
Return the score in a JSON with {score_response_format} format.
"""

    SCORE_NUTRIENTS_SYSTEM_PROMPT = """
You are a helpful assistant that scores the accuracy of the nutrients extracted from a food image.
"""

    SCORE_NUTRIENTS_USER_PROMPT = """
Score the accuracy of the nutrients extracted from a food image.
The nutrients are:
{nutrients_list}
The expected nutrients are:
{expected_nutrients_list}
Return the score in a JSON with {score_response_format} format.
"""