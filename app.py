from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import os

app = Flask(__name__)

MODEL_PATH = "eq_model_bundle_new.pkl"

# Load model
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)

model = load_model()

def get_strength_category(mag):
    if mag < 3.0:
        return "WEAK", "green"
    elif mag < 4.5:
        return "MODERATE", "yellow"
    elif mag < 6.0:
        return "STRONG", "orange"
    else:
        return "SEVERE", "red"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate all required fields are present
        required_fields = ['latitude', 'longitude', 'depth', 'mag', 'nst', 'gap', 'dmin', 'rms', 'horizontalError', 'depthError', 'magError']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        values = [
            float(data['latitude']),
            float(data['longitude']),
            float(data['depth']),
            float(data['mag']),
            float(data['nst']),
            float(data['gap']),
            float(data['dmin']),
            float(data['rms']),
            float(data['horizontalError']),
            float(data['depthError']),
            float(data['magError'])
        ]
        
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        X = np.array([values])
        mag = model.predict(X)[0]
        
        strength, color = get_strength_category(mag)
        probability = round(min(max(mag / 10, 0), 1), 3)
        
        # Generate summary
        if strength == "WEAK":
            summary = "Intensity: Very Light\nDamage: None\nImpact: Minimal"
        elif strength == "MODERATE":
            summary = "Intensity: Light\nDamage: Low\nImpact: Minimal"
        elif strength == "STRONG":
            summary = "Intensity: Moderate\nDamage: Noticeable\nImpact: Medium"
        else:
            summary = "Intensity: Severe\nDamage: High\nImpact: Significant"
        
        return jsonify({
            'magnitude': round(mag, 2),
            'strength': strength,
            'color': color,
            'probability': probability,
            'summary': summary
        })
    
    except Exception as e:
        app.logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
