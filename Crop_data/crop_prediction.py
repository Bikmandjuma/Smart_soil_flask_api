import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from flask import Blueprint, jsonify, request
import requests
from Crop_data.dataset import dataset
from Crop_data.laravel_url_api import Laravel_url_api

crop_prediction_bp = Blueprint('crop_prediction_bp', __name__)

@crop_prediction_bp.route('/api/crop_predicted', methods=['GET'])
def get_crop_prediction():
    
    response = requests.get(Laravel_url_api)
    
    if response.status_code != 200:
        return jsonify({"message": "Failed to fetch data from Laravel API"}), 400

    data_from_laravel = response.json()

    required_fields = ['N', 'P', 'K', 'temperature', 'pH', 'soil_moisture', 'conductivity']
    
    if not all(field in data_from_laravel for field in required_fields):
        
        return jsonify({"message": "Missing necessary data for crop prediction"}), 400

    data = dataset()

    X = data[['N', 'P', 'K', 'temperature', 'soil_moisture', 'pH', 'conductivity']]
    y = data['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(random_state=0)
    model.fit(X_train, y_train)

    new_data = pd.DataFrame({
        "N": [data_from_laravel['N']],
        "P": [data_from_laravel['P']],
        "K": [data_from_laravel['K']],
        "temperature": [data_from_laravel['temperature']],
        "pH": [data_from_laravel['pH']],
        "soil_moisture": [data_from_laravel['soil_moisture']],
        "conductivity": [data_from_laravel['conductivity']]
    })

    new_data = new_data[X.columns]

    invalid_conditions = (
        (new_data['N'][0] == 0 and new_data['P'][0] == 0 and new_data['K'][0] == 0) or
        (new_data['temperature'][0] <= 0) or
        (new_data['soil_moisture'][0] < 0.05) or
        (new_data['pH'][0] < 4 or new_data['pH'][0] > 10) or
        (new_data['conductivity'][0] == 0)
    )

    if invalid_conditions:
        return jsonify({"message": "No crop is recommended for the given conditions. The environment is unsuitable for farming."})

    predicted_probabilities = model.predict_proba(new_data)

    predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)
    filtered_predictions = predictions_df.T[predictions_df.T[0] > 0].sort_values(by=0, ascending=False)

    if filtered_predictions.empty:
        return jsonify({"message": "No crop is recommended for the given conditions. The environment is unsuitable for farming."})
    else:
        most_probable_crop = filtered_predictions.index[0]
        return jsonify({
            "predicted_probabilities": filtered_predictions.to_dict(),
            "most_probable_crop": most_probable_crop
        })
