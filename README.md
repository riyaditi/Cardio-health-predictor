#  CardioCheck AI: Cardiovascular Health Predictor 🩺

## Project Overview

**CardioCheck AI** is a web application that leverages a machine learning model to predict the risk of cardiovascular disease based on a user's health metrics. The application provides an intuitive user interface to input health data and receive an instant risk assessment, complete with a visual gauge and personalized, non-prescriptive health recommendations.

This project was developed as an end-to-end data science application, covering everything from data cleaning and model training to deploying the model via a REST API and building a user-friendly frontend.

---

## ✨ Key Features
<img width="1922" height="1082" alt="image" src="https://github.com/user-attachments/assets/e6b5b36c-380b-470c-a8e7-3f3f1a12f957" />

* **📈 AI-Powered Prediction:** Utilizes a `RandomForestClassifier` trained on a dataset of 70,000 patient records to predict risk probability.
* **📊 Interactive UI:** A clean, modern, and responsive user interface for easy data input.
* ** görsel Risk Gauge:** Displays the prediction result on an animated gauge chart for immediate visual feedback.
* **❤️ Personalized Recommendations:** Generates actionable health advice based on the user's specific input data and predicted risk.
* **🚀 REST API Backend:** The model is served via a Flask API, decoupling the ML logic from the frontend.

---

## 🛠️ Technology Stack

* **Backend:** Python, Flask
* **Machine Learning:** Pandas, Scikit-learn
* **Frontend:** HTML, CSS, JavaScript
* **Visualization:** Gauge.js
* **Model Serialization:** Joblib

---

## 📂 Project Structure
