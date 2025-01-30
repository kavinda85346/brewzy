from flask import Flask, render_template, request, jsonify, session
import os
import uuid
import json
import tensorflow as tf
import numpy as np
from keras.preprocessing.image import img_to_array, load_img
from models.recipe_classifier import get_beverage_recipes

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = Flask(__name__)

# Set a strong secret key for session management
app.secret_key = os.urandom(24)

# Enhance session security settings
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)

# Load the pre-trained model
model = tf.keras.models.load_model('models/fruit_veg_classifier.h5')

# Load the class indices
with open('models/class_indices.json', 'r') as json_file:
    class_indices = json.load(json_file)

# Reverse the class_indices dictionary to get the index to label mapping
index_to_label = {v: k for k, v in class_indices.items()}

def prepare_image(image_path):
    try:
        image = load_img(image_path, target_size=(128, 128))  # Ensure the target size matches the model input
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = image.astype('float32') / 255.0  # Ensure the image is scaled correctly
        return image
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    beverages = []
    predicted_class_label = None

    if request.method == 'POST':
        file = request.files.get('image', None)
        if not file or file.filename == '':
            return "No file selected"
        
        try:
            # Save uploaded image
            unique_filename = str(uuid.uuid4()) + "_" + file.filename
            filepath = os.path.join('static', 'uploads', unique_filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)

            # Prepare the image and make prediction
            image = prepare_image(filepath)
            if image is None:
                return "Error processing the uploaded image."

            # Perform prediction
            prediction = model.predict(image)
            predicted_class_index = np.argmax(prediction)
            predicted_class_label = index_to_label.get(predicted_class_index, "Unknown")

            # Get beverage recipes based on the predicted ingredient
            beverages = get_beverage_recipes(predicted_class_label)

            # Store the predicted class label in the session
            session['predicted_class_label'] = predicted_class_label

            # Remove the image after processing
            os.remove(filepath)

        except Exception as e:
            print(f"Error during prediction or file handling: {e}")
            return "An error occurred while processing the image."

    return render_template('index.html', prediction=predicted_class_label, beverages=beverages)

@app.route('/get_recipe', methods=['GET'])
def get_recipe():
    recipe_name = request.args.get('recipe_name')
    
    # Retrieve the predicted class label from the session
    predicted_class_label = session.get('predicted_class_label')

    # If no predicted class label in session, return an error
    if not predicted_class_label:
        return jsonify({"error": "No predicted class label found"}), 400

    beverages = get_beverage_recipes(predicted_class_label)

    # Find the selected recipe
    selected_recipe = next((b for b in beverages if b['Recipe Name'] == recipe_name), None)
    
    if selected_recipe:
        return jsonify(selected_recipe)
    else:
        return jsonify({"error": "Recipe not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
