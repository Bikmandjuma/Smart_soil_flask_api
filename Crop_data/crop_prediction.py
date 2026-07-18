import os
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from flask import Blueprint, jsonify, request
import requests
from openai import OpenAI
from Crop_data.dataset import dataset
from Crop_data.laravel_url_api import Laravel_url_api

crop_prediction_bp = Blueprint('crop_prediction_bp', __name__)

# =====================================================
# Groq (OpenAI-compatible) client for agronomy advice
# =====================================================
GROQ_MODEL = "llama-3.3-70b-versatile"

# Simple in-process cache so repeated requests for the same crop don't
# hit the Groq API again — the Vue frontend polls every second, so
# without this we'd be re-generating the same advice on every poll cycle.
_agronomy_advice_cache = {}


def _get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )


def get_agronomy_advice(crop_name):
    """
    Calls Groq's OpenAI-compatible chat completions endpoint to get
    fertilization, planting season, and irrigation guidance for a crop.
    Returns a dict with keys: fertilization, planting_season, irrigation.
    Raises an exception on failure — the caller is responsible for
    turning that into an appropriate HTTP response.
    """
    if crop_name in _agronomy_advice_cache:
        return _agronomy_advice_cache[crop_name]

    client = _get_groq_client()
    if client is None:
        raise RuntimeError("GROQ_API_KEY is not configured on the server")

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an agronomy assistant. Given a crop name, respond ONLY with a JSON "
                    "object with exactly these keys: fertilization, planting_season, irrigation. "
                    "Each value should be 2-4 concise sentences of practical, general guidance."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Crop: {crop_name}. Provide fertilization recommendations, the best "
                    "planting season, and an irrigation schedule."
                ),
            },
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    content = response.choices[0].message.content
    advice = json.loads(content)

    normalized_advice = {
        "fertilization": advice.get("fertilization", ""),
        "planting_season": advice.get("planting_season", ""),
        "irrigation": advice.get("irrigation", ""),
    }

    _agronomy_advice_cache[crop_name] = normalized_advice
    return normalized_advice


def _agronomy_advice_response(crop_name):
    if not crop_name:
        return jsonify({"message": "Missing 'crop' query parameter"}), 400

    try:
        advice = get_agronomy_advice(crop_name)
        return jsonify(advice)
    except RuntimeError as e:
        return jsonify({"message": str(e)}), 500
    except Exception as e:
        return jsonify({"message": f"Failed to generate agronomy advice: {str(e)}"}), 500


# Query-param style: /api/crop_agronomy_advice?crop=rice
@crop_prediction_bp.route('/api/crop_agronomy_advice', methods=['GET'])
def crop_agronomy_advice_query():
    return _agronomy_advice_response(request.args.get('crop'))


# Path-param style: /api/crop_agronomy_advice/rice
# Added defensively so this works regardless of which URL shape the
# frontend ends up calling.
@crop_prediction_bp.route('/api/crop_agronomy_advice/<crop_name>', methods=['GET'])
def crop_agronomy_advice_path(crop_name):
    return _agronomy_advice_response(crop_name)


# =====================================================
# Crop prediction (unchanged from your original logic)
# =====================================================
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