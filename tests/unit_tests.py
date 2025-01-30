import os
import pytest
import numpy as np  # Ensure numpy is imported
from app import app, prepare_image
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_get(client):
    """Test the index route for GET requests."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'input type="file"' in response.data  # Check for the file input element
    assert b'Upload' in response.data  # Check for the upload button text

def test_index_post_no_file(client):
    """Test index route when no file is sent."""
    response = client.post('/')
    assert response.status_code == 200
    assert b'No file part' in response.data  # Check if the correct error message is returned

def test_index_post_no_selected_file(client):
    """Test index route when no selected file."""
    response = client.post('/', data={})
    assert response.status_code == 200
    assert b'No file part' in response.data  # Check if the correct error message is returned

@patch('app.load_img')
@patch('app.img_to_array')
@patch('app.tf.keras.models.load_model')
def test_prepare_image(mock_load_model, mock_img_to_array, mock_load_img):
    """Test the image preparation function."""
    mock_load_img.return_value = MagicMock()  # Mocking the image
    mock_img_to_array.return_value = np.random.rand(128, 128, 3)  # Simulating an image array
    image = prepare_image("path/to/image.jpg")
    assert image.shape == (1, 128, 128, 3)  # Shape should match the expected output

def test_index_post_with_image(client):
    """Test index route when a valid image file is uploaded."""
    test_image_path = os.path.join('tests', 'apple.png')
    assert os.path.exists(test_image_path), "Test image does not exist."  # Ensure the image exists

    with open(test_image_path, 'rb') as img:
        response = client.post('/', data={'image': img})
    assert response.status_code == 200
    assert b'Prediction:' in response.data  # Check if the prediction is displayed
