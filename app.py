import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS 
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
CORS(app)
model = tf.keras.models.load_model('trained_model.keras', compile=False)

# List of class names
class_name = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

def preprocess_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image = image.resize((128, 128))  # Resize image to match model input size
        image_array = np.array(image) # Normalize pixel values
        return np.expand_dims(image_array, axis=0)  # Add batch dimension
    except Exception as e:
        raise ValueError(f"Error in processing image: {str(e)}")

@app.route('/')
def home():
    return render_template('model_form.html')  # Render the form

@app.route('/predict', methods=['POST'])
def predict():
    try:

        # Get the image file from the POST request
        file = request.files['image']
        image_bytes = file.read()
        
        # Preprocess the image
        input_data = preprocess_image(image_bytes)
        
        # Get predictions from the model
        predictions = model.predict(input_data)
        
        # Get the predicted class index and confidence
        predicted_class = np.argmax(predictions, axis=-1)[0]
        confidence = float(np.max(predictions))
        
        # Map the class index to the class name
        predicted_label = class_name[predicted_class]

        # Return the response with the prediction
        return jsonify({
            'predicted_class': int(predicted_class),
            'class_label': predicted_label,
            'confidence': confidence
        })
    
    except Exception as e:
        # Return error message if an exception occurs
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Start the Flask app