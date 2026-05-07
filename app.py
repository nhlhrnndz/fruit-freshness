from flask import Flask, request, jsonify, render_template
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Load the trained model
model = load_model('fruit_freshness_model.h5')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    return np.expand_dims(image, axis=0)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed. Use PNG, JPG, or JPEG'}), 400

    try:
        image = Image.open(file)
        processed_image = preprocess_image(image)

        prediction = model.predict(processed_image)[0][0]

        if prediction > 0.5:
            result = "Fresh"
            confidence = float(prediction) * 100
        else:
            result = "Not Fresh"
            confidence = float(1 - prediction) * 100

        return jsonify({
            'prediction': result,
            'confidence': round(confidence, 2),
            'raw_score': float(prediction)
        })

    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 
