Earthquake Magnitude Prediction System

A Machine Learning powered web application that predicts earthquake magnitude based on seismic and geospatial parameters. Built using Random Forest Regression and deployed using Flask with an interactive frontend.

------------------------------------------------------------

Project Overview

This system predicts earthquake magnitude using historical seismic data and displays:

- Predicted Magnitude
- Strength Category (Weak / Moderate / Strong / Severe)
- Strong Probability Score
- Visual Gauge Chart
- Earthquake Impact Summary

The application includes:
- Model training script
- Saved ML model (.pkl)
- Flask backend API
- Interactive frontend (HTML + CSS + JS + Chart.js)

------------------------------------------------------------

Machine Learning Model

- Algorithm: Random Forest Regressor
- Library: scikit-learn
- Evaluation Metric: Mean Absolute Error (MAE)
- Model File: eq_model_bundle_new.pkl

Model training script:
See train_model_new.py

Saved model:
eq_model_bundle_new.pkl

------------------------------------------------------------

Flask Backend

Main Flask application:
app.py

Features:
- REST API endpoint `/predict`
- JSON-based request validation
- Error handling
- Strength classification logic
- Probability calculation

------------------------------------------------------------

Frontend

JavaScript  
Handles:
- Form submission
- API request
- Dynamic UI updates
- Gauge chart rendering

File: script.js

CSS Styling  
Modern responsive UI with gradient theme and result cards.

File: style.css

------------------------------------------------------------

Requirements

All dependencies are listed in requirements.txt

Key libraries:
- Flask
- scikit-learn
- numpy
- pandas
- joblib
- matplotlib

Install dependencies:

pip install -r requirements.txt

------------------------------------------------------------

How to Run the Project

Step 1: Clone the Repository

git clone <your-repository-link>  
cd earthquake-predictor  

Step 2: Install Dependencies

pip install -r requirements.txt  

Step 3: Run Flask App

python app.py  

Step 4: Open Browser

http://127.0.0.1:5000/

------------------------------------------------------------

Input Features

The model expects the following numerical inputs:

- Latitude
- Longitude
- Depth
- Magnitude
- Number of Stations (nst)
- Gap
- Minimum Distance (dmin)
- RMS
- Horizontal Error
- Depth Error
- Magnitude Error

------------------------------------------------------------

API Endpoint

POST /predict

Request Body (JSON):

{
  "latitude": 10,
  "longitude": 20,
  "depth": 15,
  "mag": 4.5,
  "nst": 30,
  "gap": 50,
  "dmin": 0.1,
  "rms": 0.5,
  "horizontalError": 0.2,
  "depthError": 0.3,
  "magError": 0.1
}

Response:

{
  "magnitude": 5.23,
  "strength": "STRONG",
  "color": "orange",
  "probability": 0.523,
  "summary": "Intensity: Moderate..."
}

------------------------------------------------------------

Strength Categories

Magnitude < 3.0   → Weak (Green)  
3.0 – 4.5         → Moderate (Yellow)  
4.5 – 6.0         → Strong (Orange)  
> 6.0             → Severe (Red)

------------------------------------------------------------

Key Highlights

- End-to-End ML Pipeline  
- Data Preprocessing  
- Model Evaluation  
- Model Serialization (Joblib)  
- REST API Development  
- Interactive Chart Visualization  
- Responsive UI  
- Error Handling & Validation  

------------------------------------------------------------

Future Improvements

- Deploy to AWS / Render / Heroku
- Add authentication system
- Store predictions in database
- Add historical earthquake visualization
- Improve model with hyperparameter tuning

------------------------------------------------------------

Author

Sri Ram Charan Maddala  
B.Tech Student | Machine Learning & AI Enthusiast  

------------------------------------------------------------

License

This project is for educational and academic purposes.
