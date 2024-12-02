import os
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
model = tf.keras.models.load_model('trained_model.keras', compile=False)

def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image = image.resize((128, 128))  # Adjust size to match your model input
    image_array = np.array(image) / 255.0  # Normalize pixel values
    return np.expand_dims(image_array, axis=0)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['image']  # Accept image file
        image_bytes = file.read()
        input_data = preprocess_image(image_bytes)
        predictions = model.predict(input_data)
        predicted_class = np.argmax(predictions, axis=-1)[0]
        return jsonify({'predicted_class': int(predicted_class), 'confidence': float(np.max(predictions))})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/', methods=['GET'])
def home():
    return "Plant Disease Detection API is running!"

if __name__ == '__main__':
    # Use 5001 for Render deployment, but allow dynamic port if Render uses a different one.
    port = int(os.environ.get('PORT', 5001))  # Defaults to 5001 if no dynamic port
    app.run(host='0.0.0.0', port=port)