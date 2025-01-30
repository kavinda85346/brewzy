import os
import json

# Function to classify recipes based on the presence of an ingredient
def classify_recipe_by_ingredient(ingredient, recipes):
    matched_recipes = []
    ingredient = ingredient.lower()  # Ensure case-insensitive comparison
    for recipe in recipes:
        # Check if the predicted ingredient is in any of the recipe's ingredient fields
        ingredients_str = ' '.join([recipe['Ingredients']['Main Ingredients'], 
                                    recipe['Ingredients'].get('Sweeteners', ''),
                                    recipe['Ingredients'].get('Flavorings/Spices', ''),
                                    recipe['Ingredients'].get('Liquids/Mixers', ''),
                                    recipe['Ingredients'].get('Garnishes', ''),
                                    recipe['Ingredients'].get('Ice or Frozen Ingredients', '')]).lower()
        if ingredient in ingredients_str:
            matched_recipes.append(recipe)
    return matched_recipes

# Function to load and return beverage recipes matching the ingredient
def get_beverage_recipes(predicted_ingredient):
    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))  
    # Construct the full path to the smoothie_recipes.json file
    file_path = os.path.join(current_dir, 'smoothie_recipes.json')  
    # Load the beverage recipes from the JSON file
    with open(file_path, 'r') as file:
        recipes = json.load(file)  
    # Apply the classification function
    return classify_recipe_by_ingredient(predicted_ingredient, recipes)
