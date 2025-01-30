import os
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_image(client):
    """Test the image upload functionality."""
    # Use the apple.png image from the tests folder
    test_image_path = os.path.join('tests', 'apple.png')
    assert os.path.exists(test_image_path), "Test image does not exist."  # Ensure the image exists

    with open(test_image_path, 'rb') as img:
        response = client.post('/', data={'image': img})
    assert response.status_code == 200
    assert b'Prediction:' in response.data  # Check if the prediction is displayed

def test_search_recipes(client):
    """Test the search functionality for recipes with 'strawberries'."""
    response = client.post('/search', data={'Ingredient': 'strawberries'})
    assert response.status_code == 200
    assert b"Recipes containing 'strawberries'" in response.data  # Check if the ingredient heading is present
    assert b'recipes' in response.data or b'No recipes found containing' in response.data  # Check for recipes or no results

def test_search_no_recipes(client):
    """Test the search functionality when no recipes are found."""
    response = client.post('/search', data={'Ingredient': 'unknowningredient'})
    assert response.status_code == 200
    assert b"No recipes found containing 'unknowningredient'." in response.data  # Check the no recipes found message
