import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

print("Starting model training script...")

# Load the dataset
df = pd.read_csv('D:\\cardio-health-predictor\\data\\cardio_train.csv', sep=';')

# --- 1. Preprocessing and Feature Engineering ---
# Convert age to years
df['age_years'] = (df['age'] / 365).round().astype(int)

# Calculate BMI
df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)

# Remove unrealistic data points (outliers)
df.drop(df[(df['ap_hi'] > 250) | (df['ap_hi'] < 40)].index, inplace=True)
df.drop(df[(df['ap_lo'] > 200) | (df['ap_lo'] < 40)].index, inplace=True)
# Also remove BMI outliers
df.drop(df[(df['bmi'] > 60) | (df['bmi'] < 10)].index, inplace=True)

# Drop original columns that are no longer needed
df_processed = df.drop(['id', 'age'], axis=1)

# --- 2. Define Features (X) and Target (y) ---
X = df_processed.drop('cardio', axis=1)
y = df_processed['cardio']

# Ensure the feature order is consistent for later use in the API
feature_order = list(X.columns)
print(f"Feature order: {feature_order}")


# --- 3. Split Data ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- 4. Scale Numerical Features ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- 5. Train the Model ---
print("Training the RandomForestClassifier...")
model = RandomForestClassifier(n_estimators=120, random_state=42, max_depth=10, min_samples_leaf=5)
model.fit(X_train_scaled, y_train)

# --- 6. Evaluate the Model ---
print("Evaluating the model...")
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# --- 7. Save Model Artifacts ---
# Define the path to the app directory
output_dir = 'D:\\cardio-health-predictor\\app'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the scaler and the model
joblib.dump(scaler, os.path.join(output_dir, 'scaler.joblib'))
print(f"Scaler saved to {os.path.join(output_dir, 'scaler.joblib')}")

joblib.dump(model, os.path.join(output_dir, 'model.joblib'))
print(f"Model saved to {os.path.join(output_dir, 'model.joblib')}")

print("\nModel training and saving complete.")