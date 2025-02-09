# import pickle
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.datasets import make_classification

# # Generate sample dataset (Replace this with your Kaggle dataset)
# X, y = make_classification(n_samples=1000, n_features=4, random_state=42)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model
# model = RandomForestClassifier()
# model.fit(X_train, y_train)

# # Save the trained model
# with open('crop_model.pkl', 'wb') as file:
#     pickle.dump(model, file)

# print("Model saved as 'crop_model.pkl'")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load data from the CSV
data = pd.read_csv('Plant_Parameters.csv')

# Feature columns
X = data[['pH', 'temperature', 'moisture', 'nutrient']]

# Target column (crop type)
y = data['crop_type']

# Convert categorical labels to numeric using LabelEncoder
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model to a file
joblib.dump(model, 'crop_model.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')

print("Model trained and saved successfully.")