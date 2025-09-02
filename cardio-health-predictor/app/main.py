from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# --- Load Model Artifacts ---
model = joblib.load('D:\\cardio-health-predictor\\app\\model.joblib')
scaler = joblib.load('D:\\cardio-health-predictor\\app\\scaler.joblib')
print("Model and scaler loaded successfully.")

# Define the feature order (MUST be the same as during training)
feature_order = [
    'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc',
    'smoke', 'alco', 'active', 'age_years', 'bmi'
]

def generate_recommendations(user_data, prediction_proba):
    """Generates personalized health recommendations."""
    recommendations = []
    
    risk_percentage = prediction_proba * 100
    if risk_percentage > 50:
        recommendations.append(f"Our analysis indicates a high risk ({risk_percentage:.0f}%). It is strongly recommended to consult a healthcare professional for a comprehensive evaluation.")
    else:
        recommendations.append(f"Our analysis indicates a low risk ({100 - risk_percentage:.0f}% to remain low-risk). This is great! Continue to maintain a healthy lifestyle.")
    
    if user_data.get('bmi', 0) >= 30:
        recommendations.append(f"Your BMI of {user_data['bmi']:.2f} is in the obese range. Focusing on a balanced diet and regular physical activity can significantly improve your health.")
    elif user_data.get('bmi', 0) >= 25:
        recommendations.append(f"Your BMI of {user_data['bmi']:.2f} is in the overweight range. Small changes in diet and exercise can help manage your weight effectively.")

    if user_data.get('ap_hi', 0) >= 140 or user_data.get('ap_lo', 0) >= 90:
        recommendations.append("Your blood pressure is elevated. Consider reducing sodium intake, managing stress, and discussing this with your doctor.")
    
    if user_data.get('cholesterol', 1) > 1:
        recommendations.append("Your cholesterol level is above normal. A diet rich in fiber, fruits, vegetables, and low in saturated fats is advisable.")
        
    if user_data.get('active', 1) == 0:
        recommendations.append("Increasing physical activity is highly beneficial. Aim for at least 30 minutes of moderate exercise most days of the week.")

    return recommendations

# Route for the home page (which will serve the HTML)
@app.route('/')
def home():
    return render_template('index.html')

# Route for the prediction logic
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)

        # --- Data Preparation ---
        
        data['bmi'] = data['weight'] / ((data['height'] / 100) ** 2)

        # Create a feature array in the correct order
        features = np.array([data[feature] for feature in feature_order]).reshape(1, -1)
        
        # --- Scaling and Prediction ---
        scaled_features = scaler.transform(features)
        prediction_proba = model.predict_proba(scaled_features)[0][1] # Probability for class 1
        
        # --- Generate Recommendations ---
        recommendations = generate_recommendations(data, prediction_proba)
        
        return jsonify({
            'prediction_probability': round(prediction_proba, 3),
            'recommendations': recommendations
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)