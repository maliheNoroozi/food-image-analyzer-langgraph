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

    EVALUATION_SYSTEM_PROMPT = "You are an impartial expert judge."
    EVALUATION_INGREDIENTS_USER_PROMPT = """\
Given the predicted ingredients: {predicted_ingredients} and the ground truth ingredients: {expected_ingredients}, 
calculate the true positives (tp), false positives (fp), and false negatives (fn).
"""
