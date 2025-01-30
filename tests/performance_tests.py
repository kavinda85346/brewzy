import pytest
from flask import Flask

# Assuming your Flask app is in a file named app.py
from app import app  # Adjust the import according to your app structure

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index_benchmark(benchmark, client):
    # This will benchmark the index route
    response = benchmark(client.get, '/')
    assert response.status_code == 200
