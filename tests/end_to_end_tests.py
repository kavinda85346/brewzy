import pytest
from flask import Flask, render_template
from flask_testing import TestCase

# Import your Flask application
from app import app  # Adjust based on your app's import path

class TestEndToEnd(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        return app

    def test_homepage(self):
        response = self.client.get('/')  # Assuming this is your route for index.html
        assert response.status_code == 200
        assert b'Explore' in response.data  # Adjust based on your actual content

# You can add more tests for other features if needed
