# import os
# import json
# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from flask import Blueprint, jsonify, request
# import requests
# from openai import OpenAI
# from Crop_data.dataset import dataset
# from Crop_data.laravel_url_api import Laravel_url_api

# crop_prediction_bp = Blueprint('crop_prediction_bp', __name__)

# # =====================================================
# # Groq (OpenAI-compatible) client for agronomy advice
# # =====================================================
# GROQ_MODEL = "llama-3.3-70b-versatile"

# # Simple in-process cache so repeated requests for the same crop don't
# # hit the Groq API again — the Vue frontend polls every second, so
# # without this we'd be re-generating the same advice on every poll cycle.
# _agronomy_advice_cache = {}


# def _get_groq_client():
#     api_key = os.environ.get("GROQ_API_KEY")
#     if not api_key:
#         return None
#     return OpenAI(
#         api_key=api_key,
#         base_url="https://api.groq.com/openai/v1",
#     )


# def get_agronomy_advice(crop_name):
#     """
#     Calls Groq's OpenAI-compatible chat completions endpoint to get
#     fertilization, planting season, and irrigation guidance for a crop.
#     Returns a dict with keys: fertilization, planting_season, irrigation.
#     Raises an exception on failure — the caller is responsible for
#     turning that into an appropriate HTTP response.
#     """
#     if crop_name in _agronomy_advice_cache:
#         return _agronomy_advice_cache[crop_name]

#     client = _get_groq_client()
#     if client is None:
#         raise RuntimeError("GROQ_API_KEY is not configured on the server")

#     response = client.chat.completions.create(
#         model=GROQ_MODEL,
#         response_format={"type": "json_object"},
#         messages=[
#             {
#                 "role": "system",
#                 "content": (
#                     "You are an agronomy assistant. Given a crop name, respond ONLY with a JSON "
#                     "object with exactly these keys: fertilization, planting_season, irrigation. "
#                     "Each value should be 2-4 concise sentences of practical, general guidance."
#                 ),
#             },
#             {
#                 "role": "user",
#                 "content": (
#                     f"Crop: {crop_name}. Provide fertilization recommendations, the best "
#                     "planting season, and an irrigation schedule."
#                 ),
#             },
#         ],
#         temperature=0.3,
#         max_tokens=1024,
#     )

#     content = response.choices[0].message.content
#     advice = json.loads(content)

#     normalized_advice = {
#         "fertilization": advice.get("fertilization", ""),
#         "planting_season": advice.get("planting_season", ""),
#         "irrigation": advice.get("irrigation", ""),
#     }

#     _agronomy_advice_cache[crop_name] = normalized_advice
#     return normalized_advice


# def _agronomy_advice_response(crop_name):
#     if not crop_name:
#         return jsonify({"message": "Missing 'crop' query parameter"}), 400

#     try:
#         advice = get_agronomy_advice(crop_name)
#         return jsonify(advice)
#     except RuntimeError as e:
#         return jsonify({"message": str(e)}), 500
#     except Exception as e:
#         return jsonify({"message": f"Failed to generate agronomy advice: {str(e)}"}), 500


# # Query-param style: /api/crop_agronomy_advice?crop=rice
# @crop_prediction_bp.route('/api/crop_agronomy_advice', methods=['GET'])
# def crop_agronomy_advice_query():
#     return _agronomy_advice_response(request.args.get('crop'))


# # Path-param style: /api/crop_agronomy_advice/rice
# # Added defensively so this works regardless of which URL shape the
# # frontend ends up calling.
# @crop_prediction_bp.route('/api/crop_agronomy_advice/<crop_name>', methods=['GET'])
# def crop_agronomy_advice_path(crop_name):
#     return _agronomy_advice_response(crop_name)


# # =====================================================
# # Crop prediction (unchanged from your original logic)
# # =====================================================
# @crop_prediction_bp.route('/api/crop_predicted', methods=['GET'])
# def get_crop_prediction():

#     response = requests.get(Laravel_url_api)

#     if response.status_code != 200:
#         return jsonify({"message": "Failed to fetch data from Laravel API"}), 400
#     data_from_laravel = response.json()
#     required_fields = ['N', 'P', 'K', 'temperature', 'pH', 'soil_moisture', 'conductivity']

#     if not all(field in data_from_laravel for field in required_fields):

#         return jsonify({"message": "Missing necessary data for crop prediction"}), 400
#     data = dataset()
#     X = data[['N', 'P', 'K', 'temperature', 'soil_moisture', 'pH', 'conductivity']]
#     y = data['label']
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#     model = RandomForestClassifier(random_state=0)
#     model.fit(X_train, y_train)
#     new_data = pd.DataFrame({
#         "N": [data_from_laravel['N']],
#         "P": [data_from_laravel['P']],
#         "K": [data_from_laravel['K']],
#         "temperature": [data_from_laravel['temperature']],
#         "pH": [data_from_laravel['pH']],
#         "soil_moisture": [data_from_laravel['soil_moisture']],
#         "conductivity": [data_from_laravel['conductivity']]
#     })
#     new_data = new_data[X.columns]
#     invalid_conditions = (
#         (new_data['N'][0] == 0 and new_data['P'][0] == 0 and new_data['K'][0] == 0) or
#         (new_data['temperature'][0] <= 0) or
#         (new_data['soil_moisture'][0] < 0.05) or
#         (new_data['pH'][0] < 4 or new_data['pH'][0] > 10) or
#         (new_data['conductivity'][0] == 0)
#     )
#     if invalid_conditions:
#         return jsonify({"message": "No crop is recommended for the given conditions. The environment is unsuitable for farming."})
#     predicted_probabilities = model.predict_proba(new_data)
#     predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)
#     filtered_predictions = predictions_df.T[predictions_df.T[0] > 0].sort_values(by=0, ascending=False)
#     if filtered_predictions.empty:
#         return jsonify({"message": "No crop is recommended for the given conditions. The environment is unsuitable for farming."})
#     else:
#         most_probable_crop = filtered_predictions.index[0]
#         return jsonify({
#             "predicted_probabilities": filtered_predictions.to_dict(),
#             "most_probable_crop": most_probable_crop
#         })

# import os
# import json
# from datetime import datetime, timedelta

# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from flask import Blueprint, jsonify, request
# import requests
# from openai import OpenAI

# from Crop_data.dataset import dataset
# from Crop_data.laravel_url_api import Laravel_url_api

# crop_prediction_bp = Blueprint('crop_prediction_bp', __name__)

# # =====================================================
# # Groq (OpenAI-compatible) client for agronomy advice
# # =====================================================
# GROQ_MODEL = "llama-3.3-70b-versatile"

# # Cache key includes weather_condition, so advice regenerates when
# # on-site ambient conditions change even for the same crop.
# _agronomy_advice_cache = {}


# def _get_groq_client():
#     api_key = os.environ.get("GROQ_API_KEY")
#     if not api_key:
#         return None
#     return OpenAI(
#         api_key=api_key,
#         base_url="https://api.groq.com/openai/v1",
#     )


# def get_agronomy_advice(crop_name, weather_condition=None):
#     """
#     Calls Groq's OpenAI-compatible chat completions endpoint to get
#     fertilization, planting season, and irrigation guidance for a crop,
#     adjusted for current on-site ambient conditions (DHT11) when available.
#     """
#     cache_key = (crop_name, weather_condition)
#     if cache_key in _agronomy_advice_cache:
#         return _agronomy_advice_cache[cache_key]

#     client = _get_groq_client()
#     if client is None:
#         raise RuntimeError("GROQ_API_KEY is not configured on the server")

#     weather_note = (
#         f" The current on-site ambient temperature and humidity (measured by a "
#         f"DHT11 sensor near the crop) indicate conditions that are: {weather_condition}. "
#         "Explicitly mention how this ambient condition should adjust irrigation "
#         "frequency and fertilizer timing right now. Do not reference forecasts, "
#         "rain chances, or multi-day weather patterns — only the immediate on-site reading."
#         if weather_condition
#         else ""
#     )

#     response = client.chat.completions.create(
#         model=GROQ_MODEL,
#         response_format={"type": "json_object"},
#         messages=[
#             {
#                 "role": "system",
#                 "content": (
#                     "You are an agronomy assistant. Given a crop name, respond ONLY with a JSON "
#                     "object with exactly these keys: fertilization, planting_season, irrigation. "
#                     "Each value should be 2-4 concise sentences of practical, general guidance. "
#                     "Always factor in current on-site ambient conditions when they are provided, "
#                     "and say explicitly how the advice changes because of them."
#                 ),
#             },
#             {
#                 "role": "user",
#                 "content": (
#                     f"Crop: {crop_name}. Provide fertilization recommendations, the best "
#                     f"planting season, and an irrigation schedule.{weather_note}"
#                 ),
#             },
#         ],
#         temperature=0.3,
#         max_tokens=1024,
#     )

#     content = response.choices[0].message.content
#     advice = json.loads(content)

#     normalized_advice = {
#         "fertilization": advice.get("fertilization", ""),
#         "planting_season": advice.get("planting_season", ""),
#         "irrigation": advice.get("irrigation", ""),
#     }

#     _agronomy_advice_cache[cache_key] = normalized_advice
#     return normalized_advice


# def _agronomy_advice_response(crop_name, weather_condition=None):
#     if not crop_name:
#         return jsonify({"message": "Missing 'crop' query parameter"}), 400

#     try:
#         advice = get_agronomy_advice(crop_name, weather_condition)
#         return jsonify(advice)
#     except RuntimeError as e:
#         return jsonify({"message": str(e)}), 500
#     except Exception as e:
#         return jsonify({"message": f"Failed to generate agronomy advice: {str(e)}"}), 500


# def _weather_condition_from_request():
#     """Builds a human-readable ambient condition string from query params
#     like ?weather_temperature=28.8&weather_humidity=46.5, only when the
#     values fall inside the DHT11's real sensing range."""
#     temp = request.args.get('weather_temperature', type=float)
#     humidity = request.args.get('weather_humidity', type=float)
#     if not is_dht11_reading_valid(temp, humidity):
#         return None
#     return classify_weather(temp, humidity)


# @crop_prediction_bp.route('/api/crop_agronomy_advice', methods=['GET'])
# def crop_agronomy_advice_query():
#     return _agronomy_advice_response(
#         request.args.get('crop'),
#         _weather_condition_from_request(),
#     )


# @crop_prediction_bp.route('/api/crop_agronomy_advice/<crop_name>', methods=['GET'])
# def crop_agronomy_advice_path(crop_name):
#     return _agronomy_advice_response(crop_name, _weather_condition_from_request())


# # =====================================================
# # DHT11 ambient sensor helpers
# # =====================================================

# # DHT11 hard operating limits per its datasheet (0-50°C ±2°C, 20-90% RH ±5%).
# # A reading outside this range means the sensor glitched, is disconnected,
# # or the row is corrupt — not that real ambient conditions are that extreme.
# DHT11_TEMP_RANGE = (0, 50)
# DHT11_HUMIDITY_RANGE = (20, 90)

# # How old a DB row's created_at can be before we no longer trust it as
# # "live" ambient data for a real-time dashboard.
# STALE_READING_THRESHOLD = timedelta(minutes=5)


# def is_dht11_reading_valid(weather_temperature, weather_humidity):
#     if weather_temperature is None or weather_humidity is None:
#         return False
#     t_lo, t_hi = DHT11_TEMP_RANGE
#     h_lo, h_hi = DHT11_HUMIDITY_RANGE
#     return (t_lo <= weather_temperature <= t_hi) and (h_lo <= weather_humidity <= h_hi)


# def is_reading_stale(created_at_value):
#     """created_at_value can be a string like '2026-07-17 21:39:53' or None.
#     Returns True if we can't parse it or it's older than the threshold."""
#     if not created_at_value:
#         return False  # can't judge staleness without a timestamp; don't block on it

#     try:
#         created_at = datetime.strptime(str(created_at_value), "%Y-%m-%d %H:%M:%S")
#     except ValueError:
#         return False

#     return (datetime.now() - created_at) > STALE_READING_THRESHOLD


# def classify_weather(weather_temperature, weather_humidity):
#     """Turns raw DHT11 readings into a short descriptive label,
#     e.g. 'hot and humid', used in the UI and in the LLM prompt."""
#     if weather_temperature >= 30:
#         temp_desc = "hot"
#     elif weather_temperature >= 20:
#         temp_desc = "warm"
#     elif weather_temperature >= 10:
#         temp_desc = "mild"
#     else:
#         temp_desc = "cold"

#     if weather_humidity >= 70:
#         humidity_desc = "humid"
#     elif weather_humidity >= 40:
#         humidity_desc = "moderate humidity"
#     else:
#         humidity_desc = "dry"

#     return f"{temp_desc} and {humidity_desc}"


# # Approximate ideal (temperature °C, humidity %) ranges per crop, used to
# # re-rank the model's candidate crops by how well current ambient
# # conditions suit each one. Tune to match your dataset's exact crop labels.
# CROP_WEATHER_PROFILE = {
#     "rice": {"temp": (20, 27), "humidity": (80, 90)},
#     "maize": {"temp": (18, 26), "humidity": (55, 75)},
#     "chickpea": {"temp": (17, 21), "humidity": (14, 20)},
#     "kidneybeans": {"temp": (15, 25), "humidity": (18, 25)},
#     "pigeonpeas": {"temp": (18, 37), "humidity": (30, 70)},
#     "mothbeans": {"temp": (24, 32), "humidity": (40, 65)},
#     "mungbean": {"temp": (27, 30), "humidity": (80, 90)},
#     "blackgram": {"temp": (25, 35), "humidity": (60, 70)},
#     "lentil": {"temp": (18, 30), "humidity": (60, 70)},
#     "pomegranate": {"temp": (18, 25), "humidity": (85, 95)},
#     "banana": {"temp": (25, 30), "humidity": (75, 85)},
#     "mango": {"temp": (27, 36), "humidity": (45, 55)},
#     "grapes": {"temp": (8, 42), "humidity": (80, 85)},
#     "watermelon": {"temp": (24, 27), "humidity": (80, 90)},
#     "muskmelon": {"temp": (27, 30), "humidity": (90, 95)},
#     "apple": {"temp": (21, 24), "humidity": (90, 95)},
#     "orange": {"temp": (10, 35), "humidity": (90, 95)},
#     "papaya": {"temp": (23, 44), "humidity": (90, 95)},
#     "coconut": {"temp": (25, 30), "humidity": (90, 100)},
#     "cotton": {"temp": (22, 26), "humidity": (70, 85)},
#     "jute": {"temp": (24, 27), "humidity": (70, 90)},
#     "coffee": {"temp": (23, 28), "humidity": (50, 70)},
# }


# def _score_range(value, lo, hi):
#     if lo <= value <= hi:
#         return 1.0
#     span = (hi - lo) or 1
#     distance = min(abs(value - lo), abs(value - hi))
#     return max(0.0, 1 - (distance / span))


# def weather_suitability_score(crop, weather_temperature, weather_humidity):
#     """Returns 0-1: how well current ambient conditions match this crop's
#     ideal growing range. Falls back to 1.0 (no penalty) if the crop isn't
#     in the profile table."""
#     profile = CROP_WEATHER_PROFILE.get(str(crop).lower())
#     if not profile:
#         return 1.0

#     temp_lo, temp_hi = profile["temp"]
#     hum_lo, hum_hi = profile["humidity"]

#     temp_score = _score_range(weather_temperature, temp_lo, temp_hi)
#     hum_score = _score_range(weather_humidity, hum_lo, hum_hi)
#     return (temp_score + hum_score) / 2


# # =====================================================
# # Crop prediction, weather-aware (DHT11-backed)
# # =====================================================
# @crop_prediction_bp.route('/api/crop_predicted', methods=['GET'])
# def get_crop_prediction():

#     response = requests.get(Laravel_url_api)

#     if response.status_code != 200:
#         return jsonify({"message": "Failed to fetch data from Laravel API"}), 400

#     data_from_laravel = response.json()
#     required_fields = [
#         'N', 'P', 'K', 'temperature', 'pH', 'soil_moisture', 'conductivity',
#         'weather_temperature', 'weather_humidity',
#     ]

#     if not all(field in data_from_laravel for field in required_fields):
#         return jsonify({"message": "Missing necessary data for crop prediction"}), 400

#     weather_temperature = data_from_laravel['weather_temperature']
#     weather_humidity = data_from_laravel['weather_humidity']
#     created_at = data_from_laravel.get('created_at')

#     base_response = {
#         "weather_temperature": weather_temperature,
#         "weather_humidity": weather_humidity,
#     }

#     # A reading outside DHT11's physical range means the sensor glitched
#     # or disconnected — treat as missing/untrustworthy data, not real
#     # extreme weather, and don't let it block soil-based prediction logic.
#     if not is_dht11_reading_valid(weather_temperature, weather_humidity):
#         return jsonify({
#             **base_response,
#             "message": "Ambient sensor (DHT11) reading unavailable or out of range",
#         })

#     if is_reading_stale(created_at):
#         return jsonify({
#             **base_response,
#             "message": "Ambient sensor (DHT11) reading is stale — check device connectivity",
#             "created_at": created_at,
#         })

#     weather_condition = classify_weather(weather_temperature, weather_humidity)
#     base_response["weather_condition"] = weather_condition

#     data = dataset()
#     X = data[['N', 'P', 'K', 'temperature', 'soil_moisture', 'pH', 'conductivity']]
#     y = data['label']
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#     model = RandomForestClassifier(random_state=0)
#     model.fit(X_train, y_train)

#     new_data = pd.DataFrame({
#         "N": [data_from_laravel['N']],
#         "P": [data_from_laravel['P']],
#         "K": [data_from_laravel['K']],
#         "temperature": [data_from_laravel['temperature']],
#         "pH": [data_from_laravel['pH']],
#         "soil_moisture": [data_from_laravel['soil_moisture']],
#         "conductivity": [data_from_laravel['conductivity']]
#     })
#     new_data = new_data[X.columns]

#     invalid_conditions = (
#         (new_data['N'][0] == 0 and new_data['P'][0] == 0 and new_data['K'][0] == 0) or
#         (new_data['temperature'][0] <= 0) or
#         (new_data['soil_moisture'][0] < 0.05) or
#         (new_data['pH'][0] < 4 or new_data['pH'][0] > 10) or
#         (new_data['conductivity'][0] == 0)
#     )

#     if invalid_conditions:
#         return jsonify({
#             **base_response,
#             "message": "No crop is recommended for the given conditions. The environment is unsuitable for farming."
#         })

#     predicted_probabilities = model.predict_proba(new_data)
#     predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)
#     filtered_predictions = predictions_df.T[predictions_df.T[0] > 0].sort_values(by=0, ascending=False)

#     if filtered_predictions.empty:
#         return jsonify({
#             **base_response,
#             "message": "No crop is recommended for the given conditions. The environment is unsuitable for farming."
#         })

#     # Re-rank the model's candidates by how well current ambient
#     # conditions suit each crop.
#     filtered_predictions = filtered_predictions.copy()
#     filtered_predictions["weather_score"] = [
#         weather_suitability_score(crop, weather_temperature, weather_humidity)
#         for crop in filtered_predictions.index
#     ]
#     filtered_predictions["weather_adjusted"] = filtered_predictions[0] * filtered_predictions["weather_score"]
#     filtered_predictions = filtered_predictions.sort_values(by="weather_adjusted", ascending=False)

#     most_probable_crop = filtered_predictions.index[0]

#     return jsonify({
#         **base_response,
#         "predicted_probabilities": filtered_predictions[[0]].to_dict(),
#         "weather_adjusted_probabilities": filtered_predictions[["weather_adjusted"]].rename(
#             columns={"weather_adjusted": 0}
#         ).to_dict(),
#         "most_probable_crop": most_probable_crop
#     })

# import os
# import json
# from datetime import datetime, timedelta

# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from flask import Blueprint, jsonify, request
# import requests
# from openai import OpenAI

# from Crop_data.dataset import dataset
# from Crop_data.laravel_url_api import Laravel_url_api

# crop_prediction_bp = Blueprint('crop_prediction_bp', __name__)

# # =====================================================
# # Groq (OpenAI-compatible) client for agronomy advice
# # =====================================================
# GROQ_MODEL = "llama-3.3-70b-versatile"

# # Cache key includes weather_condition, so advice regenerates when
# # on-site ambient conditions change even for the same crop.
# _agronomy_advice_cache = {}


# def _get_groq_client():
#     api_key = os.environ.get("GROQ_API_KEY")
#     if not api_key:
#         return None
#     return OpenAI(
#         api_key=api_key,
#         base_url="https://api.groq.com/openai/v1",
#     )


# def get_agronomy_advice(crop_name, weather_condition=None):
#     """
#     Calls Groq's OpenAI-compatible chat completions endpoint to get
#     fertilization, planting season, and irrigation guidance for a crop,
#     adjusted for current on-site ambient conditions (DHT11) when available.
#     """
#     cache_key = (crop_name, weather_condition)
#     if cache_key in _agronomy_advice_cache:
#         return _agronomy_advice_cache[cache_key]

#     client = _get_groq_client()
#     if client is None:
#         raise RuntimeError("GROQ_API_KEY is not configured on the server")

#     weather_note = (
#         f" The current on-site ambient temperature and humidity (measured by a "
#         f"DHT11 sensor near the crop) indicate conditions that are: {weather_condition}. "
#         "Explicitly mention how this ambient condition should adjust irrigation "
#         "frequency and fertilizer timing right now. Do not reference forecasts, "
#         "rain chances, or multi-day weather patterns — only the immediate on-site reading."
#         if weather_condition
#         else " No ambient sensor reading is currently available, so give general "
#         "guidance without referencing specific weather conditions."
#     )

#     response = client.chat.completions.create(
#         model=GROQ_MODEL,
#         response_format={"type": "json_object"},
#         messages=[
#             {
#                 "role": "system",
#                 "content": (
#                     "You are an agronomy assistant. Given a crop name, respond ONLY with a JSON "
#                     "object with exactly these keys: fertilization, planting_season, irrigation. "
#                     "Each value should be 2-4 concise sentences of practical, general guidance. "
#                     "Always factor in current on-site ambient conditions when they are provided, "
#                     "and say explicitly how the advice changes because of them."
#                 ),
#             },
#             {
#                 "role": "user",
#                 "content": (
#                     f"Crop: {crop_name}. Provide fertilization recommendations, the best "
#                     f"planting season, and an irrigation schedule.{weather_note}"
#                 ),
#             },
#         ],
#         temperature=0.3,
#         max_tokens=1024,
#     )

#     content = response.choices[0].message.content
#     advice = json.loads(content)

#     normalized_advice = {
#         "fertilization": advice.get("fertilization", ""),
#         "planting_season": advice.get("planting_season", ""),
#         "irrigation": advice.get("irrigation", ""),
#     }

#     _agronomy_advice_cache[cache_key] = normalized_advice
#     return normalized_advice


# def _agronomy_advice_response(crop_name, weather_condition=None):
#     if not crop_name:
#         return jsonify({"message": "Missing 'crop' query parameter"}), 400

#     try:
#         advice = get_agronomy_advice(crop_name, weather_condition)
#         return jsonify(advice)
#     except RuntimeError as e:
#         return jsonify({"message": str(e)}), 500
#     except Exception as e:
#         return jsonify({"message": f"Failed to generate agronomy advice: {str(e)}"}), 500


# def _weather_condition_from_request():
#     """Builds a human-readable ambient condition string from query params
#     like ?weather_temperature=28.8&weather_humidity=46.5, only when the
#     values are present and fall inside the DHT11's real sensing range.
#     Returns None for missing (NULL) or out-of-range values — the advice
#     endpoint then just skips weather-specific guidance."""
#     temp = request.args.get('weather_temperature', type=float)
#     humidity = request.args.get('weather_humidity', type=float)
#     if ambient_reading_status(temp, humidity) != "ok":
#         return None
#     return classify_weather(temp, humidity)


# @crop_prediction_bp.route('/api/crop_agronomy_advice', methods=['GET'])
# def crop_agronomy_advice_query():
#     return _agronomy_advice_response(
#         request.args.get('crop'),
#         _weather_condition_from_request(),
#     )


# @crop_prediction_bp.route('/api/crop_agronomy_advice/<crop_name>', methods=['GET'])
# def crop_agronomy_advice_path(crop_name):
#     return _agronomy_advice_response(crop_name, _weather_condition_from_request())


# # =====================================================
# # DHT11 ambient sensor helpers
# # =====================================================

# # DHT11 hard operating limits per its datasheet (0-50°C ±2°C, 20-90% RH ±5%).
# # A reading outside this range means the sensor glitched, is disconnected,
# # or the row is corrupt — not that real ambient conditions are that extreme.
# DHT11_TEMP_RANGE = (0, 50)
# DHT11_HUMIDITY_RANGE = (20, 90)

# # How old a DB row's created_at can be before we no longer trust it as
# # "live" ambient data for a real-time dashboard.
# STALE_READING_THRESHOLD = timedelta(minutes=5)


# def ambient_reading_status(weather_temperature, weather_humidity):
#     """Classifies the ambient reading into one of three states:
#     - 'missing'      : DHT11 not wired/reporting for this row (NULL in DB,
#                         e.g. older rows before the sensor was added)
#     - 'out_of_range' : sensor reported something outside its physical spec
#                         (wiring fault, bad read)
#     - 'ok'           : usable reading
#     """
#     if weather_temperature is None or weather_humidity is None:
#         return "missing"
#     t_lo, t_hi = DHT11_TEMP_RANGE
#     h_lo, h_hi = DHT11_HUMIDITY_RANGE
#     if not (t_lo <= weather_temperature <= t_hi and h_lo <= weather_humidity <= h_hi):
#         return "out_of_range"
#     return "ok"


# def is_reading_stale(created_at_value):
#     """created_at_value can be a string like '2026-07-17 21:39:53' or None.
#     Returns True only if it parses AND is older than the threshold."""
#     if not created_at_value:
#         return False  # can't judge staleness without a timestamp; don't block on it

#     try:
#         created_at = datetime.strptime(str(created_at_value), "%Y-%m-%d %H:%M:%S")
#     except ValueError:
#         return False

#     return (datetime.now() - created_at) > STALE_READING_THRESHOLD


# def classify_weather(weather_temperature, weather_humidity):
#     """Turns raw DHT11 readings into a short descriptive label,
#     e.g. 'hot and humid', used in the UI and in the LLM prompt."""
#     if weather_temperature >= 30:
#         temp_desc = "hot"
#     elif weather_temperature >= 20:
#         temp_desc = "warm"
#     elif weather_temperature >= 10:
#         temp_desc = "mild"
#     else:
#         temp_desc = "cold"

#     if weather_humidity >= 70:
#         humidity_desc = "humid"
#     elif weather_humidity >= 40:
#         humidity_desc = "moderate humidity"
#     else:
#         humidity_desc = "dry"

#     return f"{temp_desc} and {humidity_desc}"


# # Approximate ideal (temperature °C, humidity %) ranges per crop, used to
# # re-rank the model's candidate crops by how well current ambient
# # conditions suit each one. Tune to match your dataset's exact crop labels.
# CROP_WEATHER_PROFILE = {
#     "rice": {"temp": (20, 27), "humidity": (80, 90)},
#     "maize": {"temp": (18, 26), "humidity": (55, 75)},
#     "chickpea": {"temp": (17, 21), "humidity": (14, 20)},
#     "kidneybeans": {"temp": (15, 25), "humidity": (18, 25)},
#     "pigeonpeas": {"temp": (18, 37), "humidity": (30, 70)},
#     "mothbeans": {"temp": (24, 32), "humidity": (40, 65)},
#     "mungbean": {"temp": (27, 30), "humidity": (80, 90)},
#     "blackgram": {"temp": (25, 35), "humidity": (60, 70)},
#     "lentil": {"temp": (18, 30), "humidity": (60, 70)},
#     "pomegranate": {"temp": (18, 25), "humidity": (85, 95)},
#     "banana": {"temp": (25, 30), "humidity": (75, 85)},
#     "mango": {"temp": (27, 36), "humidity": (45, 55)},
#     "grapes": {"temp": (8, 42), "humidity": (80, 85)},
#     "watermelon": {"temp": (24, 27), "humidity": (80, 90)},
#     "muskmelon": {"temp": (27, 30), "humidity": (90, 95)},
#     "apple": {"temp": (21, 24), "humidity": (90, 95)},
#     "orange": {"temp": (10, 35), "humidity": (90, 95)},
#     "papaya": {"temp": (23, 44), "humidity": (90, 95)},
#     "coconut": {"temp": (25, 30), "humidity": (90, 100)},
#     "cotton": {"temp": (22, 26), "humidity": (70, 85)},
#     "jute": {"temp": (24, 27), "humidity": (70, 90)},
#     "coffee": {"temp": (23, 28), "humidity": (50, 70)},
# }


# def _score_range(value, lo, hi):
#     if lo <= value <= hi:
#         return 1.0
#     span = (hi - lo) or 1
#     distance = min(abs(value - lo), abs(value - hi))
#     return max(0.0, 1 - (distance / span))


# def weather_suitability_score(crop, weather_temperature, weather_humidity):
#     """Returns 0-1: how well current ambient conditions match this crop's
#     ideal growing range. Falls back to 1.0 (no penalty) if the crop isn't
#     in the profile table."""
#     profile = CROP_WEATHER_PROFILE.get(str(crop).lower())
#     if not profile:
#         return 1.0

#     temp_lo, temp_hi = profile["temp"]
#     hum_lo, hum_hi = profile["humidity"]

#     temp_score = _score_range(weather_temperature, temp_lo, temp_hi)
#     hum_score = _score_range(weather_humidity, hum_lo, hum_hi)
#     return (temp_score + hum_score) / 2


# # =====================================================
# # Crop prediction, weather-aware (DHT11-backed)
# # =====================================================
# @crop_prediction_bp.route('/api/crop_predicted', methods=['GET'])
# def get_crop_prediction():

#     response = requests.get(Laravel_url_api)

#     if response.status_code != 200:
#         return jsonify({"message": "Failed to fetch data from Laravel API"}), 400

#     data_from_laravel = response.json()
#     required_fields = ['N', 'P', 'K', 'temperature', 'pH', 'soil_moisture', 'conductivity']

#     if not all(field in data_from_laravel for field in required_fields):
#         return jsonify({"message": "Missing necessary data for crop prediction"}), 400

#     # weather_temperature / weather_humidity may legitimately be NULL for
#     # rows recorded before the DHT11 was wired up — treat as optional.
#     weather_temperature = data_from_laravel.get('weather_temperature')
#     weather_humidity = data_from_laravel.get('weather_humidity')
#     created_at = data_from_laravel.get('created_at')

#     base_response = {
#         "weather_temperature": weather_temperature,
#         "weather_humidity": weather_humidity,
#         "created_at": created_at,
#     }

#     ambient_status = ambient_reading_status(weather_temperature, weather_humidity)
#     weather_condition = None

#     if ambient_status == "missing":
#         # No DHT11 data for this row — soil prediction still runs below,
#         # just without weather-fit re-ranking or weather-aware advice.
#         base_response["weather_condition"] = None
#         base_response["ambient_status"] = "missing"

#     elif ambient_status == "out_of_range":
#         return jsonify({
#             **base_response,
#             "ambient_status": "out_of_range",
#             "message": "Ambient sensor (DHT11) reading out of physical range — check wiring",
#         })

#     else:  # "ok"
#         if is_reading_stale(created_at):
#             return jsonify({
#                 **base_response,
#                 "ambient_status": "stale",
#                 "message": "Ambient sensor (DHT11) reading is stale — check device connectivity",
#             })
#         weather_condition = classify_weather(weather_temperature, weather_humidity)
#         base_response["weather_condition"] = weather_condition
#         base_response["ambient_status"] = "ok"

#     data = dataset()
#     X = data[['N', 'P', 'K', 'temperature', 'soil_moisture', 'pH', 'conductivity']]
#     y = data['label']
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#     model = RandomForestClassifier(random_state=0)
#     model.fit(X_train, y_train)

#     new_data = pd.DataFrame({
#         "N": [data_from_laravel['N']],
#         "P": [data_from_laravel['P']],
#         "K": [data_from_laravel['K']],
#         "temperature": [data_from_laravel['temperature']],
#         "pH": [data_from_laravel['pH']],
#         "soil_moisture": [data_from_laravel['soil_moisture']],
#         "conductivity": [data_from_laravel['conductivity']]
#     })
#     new_data = new_data[X.columns]

#     invalid_conditions = (
#         (new_data['N'][0] == 0 and new_data['P'][0] == 0 and new_data['K'][0] == 0) or
#         (new_data['temperature'][0] <= 0) or
#         (new_data['soil_moisture'][0] < 0.05) or
#         (new_data['pH'][0] < 4 or new_data['pH'][0] > 10) or
#         (new_data['conductivity'][0] == 0)
#     )

#     if invalid_conditions:
#         return jsonify({
#             **base_response,
#             "message": "No crop is recommended for the given conditions. The environment is unsuitable for farming."
#         })

#     predicted_probabilities = model.predict_proba(new_data)
#     predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)
#     filtered_predictions = predictions_df.T[predictions_df.T[0] > 0].sort_values(by=0, ascending=False)

#     if filtered_predictions.empty:
#         return jsonify({
#             **base_response,
#             "message": "No crop is recommended for the given conditions. The environment is unsuitable for farming."
#         })

#     # Re-rank only when we actually have a usable ambient reading;
#     # otherwise weather_score is neutral (1.0) and ranking falls back
#     # to the model's raw probabilities.
#     filtered_predictions = filtered_predictions.copy()
#     if weather_condition:
#         filtered_predictions["weather_score"] = [
#             weather_suitability_score(crop, weather_temperature, weather_humidity)
#             for crop in filtered_predictions.index
#         ]
#     else:
#         filtered_predictions["weather_score"] = 1.0

#     filtered_predictions["weather_adjusted"] = filtered_predictions[0] * filtered_predictions["weather_score"]
#     filtered_predictions = filtered_predictions.sort_values(by="weather_adjusted", ascending=False)

#     most_probable_crop = filtered_predictions.index[0]

#     return jsonify({
#         **base_response,
#         "predicted_probabilities": filtered_predictions[[0]].to_dict(),
#         "weather_adjusted_probabilities": filtered_predictions[["weather_adjusted"]].rename(
#             columns={"weather_adjusted": 0}
#         ).to_dict(),
#         "most_probable_crop": most_probable_crop
#     })

import os
import json
from datetime import datetime, timedelta

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from flask import Blueprint, jsonify, request
import requests
from openai import OpenAI

from Crop_data.dataset import dataset
from Crop_data.laravel_url_api import Laravel_url_api

crop_prediction_bp = Blueprint('crop_prediction_bp', __name__)

GROQ_MODEL = "llama-3.3-70b-versatile"
_agronomy_advice_cache = {}


def _get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")


def get_agronomy_advice(crop_name, weather_condition=None):
    cache_key = (crop_name, weather_condition)
    if cache_key in _agronomy_advice_cache:
        return _agronomy_advice_cache[cache_key]

    client = _get_groq_client()
    if client is None:
        raise RuntimeError("GROQ_API_KEY is not configured on the server")

    weather_note = (
        f" The current on-site ambient temperature and humidity (measured by a "
        f"DHT11 sensor near the crop) indicate conditions that are: {weather_condition}. "
        "Explicitly mention how this ambient condition should adjust irrigation "
        "frequency and fertilizer timing right now. Do not reference forecasts, "
        "rain chances, or multi-day weather patterns — only the immediate on-site reading."
        if weather_condition
        else " No ambient sensor reading is currently available, so give general "
        "guidance without referencing specific weather conditions."
    )

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an agronomy assistant. Given a crop name, respond ONLY with a JSON "
                    "object with exactly these keys: fertilization, planting_season, irrigation. "
                    "Each value should be 2-4 concise sentences of practical, general guidance. "
                    "Always factor in current on-site ambient conditions when they are provided, "
                    "and say explicitly how the advice changes because of them."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Crop: {crop_name}. Provide fertilization recommendations, the best "
                    f"planting season, and an irrigation schedule.{weather_note}"
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

    _agronomy_advice_cache[cache_key] = normalized_advice
    return normalized_advice


def _agronomy_advice_response(crop_name, weather_condition=None):
    if not crop_name:
        return jsonify({"message": "Missing 'crop' query parameter"}), 400

    try:
        advice = get_agronomy_advice(crop_name, weather_condition)
        return jsonify(advice)
    except RuntimeError as e:
        return jsonify({"message": str(e)}), 500
    except Exception as e:
        return jsonify({"message": f"Failed to generate agronomy advice: {str(e)}"}), 500


def _weather_condition_from_request():
    temp = request.args.get('weather_temperature', type=float)
    humidity = request.args.get('weather_humidity', type=float)
    if ambient_reading_status(temp, humidity) != "ok":
        return None
    return classify_weather(temp, humidity)


@crop_prediction_bp.route('/api/crop_agronomy_advice', methods=['GET'])
def crop_agronomy_advice_query():
    return _agronomy_advice_response(
        request.args.get('crop'),
        _weather_condition_from_request(),
    )


@crop_prediction_bp.route('/api/crop_agronomy_advice/<crop_name>', methods=['GET'])
def crop_agronomy_advice_path(crop_name):
    return _agronomy_advice_response(crop_name, _weather_condition_from_request())


# =====================================================
# DHT11 ambient sensor helpers
# =====================================================
DHT11_TEMP_RANGE = (0, 50)
DHT11_HUMIDITY_RANGE = (20, 90)
STALE_READING_THRESHOLD = timedelta(minutes=5)


def ambient_reading_status(weather_temperature, weather_humidity):
    if weather_temperature is None or weather_humidity is None:
        return "missing"
    t_lo, t_hi = DHT11_TEMP_RANGE
    h_lo, h_hi = DHT11_HUMIDITY_RANGE
    if not (t_lo <= weather_temperature <= t_hi and h_lo <= weather_humidity <= h_hi):
        return "out_of_range"
    return "ok"


def is_reading_stale(created_at_value):
    if not created_at_value:
        return False
    try:
        created_at = datetime.strptime(str(created_at_value), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return False
    return (datetime.now() - created_at) > STALE_READING_THRESHOLD


def classify_weather(weather_temperature, weather_humidity):
    if weather_temperature >= 30:
        temp_desc = "hot"
    elif weather_temperature >= 20:
        temp_desc = "warm"
    elif weather_temperature >= 10:
        temp_desc = "mild"
    else:
        temp_desc = "cold"

    if weather_humidity >= 70:
        humidity_desc = "humid"
    elif weather_humidity >= 40:
        humidity_desc = "moderate humidity"
    else:
        humidity_desc = "dry"

    return f"{temp_desc} and {humidity_desc}"


# =====================================================
# Crop weather profile — now derived from the ACTUAL training
# dataset instead of a hand-typed table. We compute each crop's
# real observed temperature range from `dataset()`. Humidity isn't
# in this dataset (it uses soil_moisture/conductivity instead of
# ambient humidity), so humidity scoring is skipped unless you add
# an ambient-humidity column to your training data later.
# =====================================================
_crop_temp_profile_cache = None


def get_crop_temp_profile():
    """Builds {crop_label: (min_temp, max_temp)} once from the dataset
    and caches it in-process. Uses the 10th-90th percentile instead of
    raw min/max so a single outlier row doesn't skew a crop's range."""
    global _crop_temp_profile_cache
    if _crop_temp_profile_cache is not None:
        return _crop_temp_profile_cache

    data = dataset()
    profile = {}
    for label, group in data.groupby('label'):
        temps = group['temperature']
        profile[str(label).lower()] = (
            temps.quantile(0.10),
            temps.quantile(0.90),
        )

    _crop_temp_profile_cache = profile
    return profile


def _score_range(value, lo, hi):
    if lo <= value <= hi:
        return 1.0
    span = (hi - lo) or 1
    distance = min(abs(value - lo), abs(value - hi))
    return max(0.0, 1 - (distance / span))


def weather_suitability_score(crop, weather_temperature):
    """Returns 0-1: how well the current ambient temperature matches this
    crop's observed temperature range in the training data. Falls back to
    1.0 (no penalty) if the crop isn't found."""
    profile = get_crop_temp_profile()
    temp_range = profile.get(str(crop).lower())
    if not temp_range:
        return 1.0

    temp_lo, temp_hi = temp_range
    return _score_range(weather_temperature, temp_lo, temp_hi)


# =====================================================
# Crop prediction, weather-aware (DHT11-backed)
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

    weather_temperature = data_from_laravel.get('weather_temperature')
    weather_humidity = data_from_laravel.get('weather_humidity')
    created_at = data_from_laravel.get('created_at')

    base_response = {
        "weather_temperature": weather_temperature,
        "weather_humidity": weather_humidity,
        "created_at": created_at,
    }

    ambient_status = ambient_reading_status(weather_temperature, weather_humidity)
    weather_condition = None

    if ambient_status == "missing":
        base_response["weather_condition"] = None
        base_response["ambient_status"] = "missing"

    elif ambient_status == "out_of_range":
        return jsonify({
            **base_response,
            "ambient_status": "out_of_range",
            "message": "Ambient sensor (DHT11) reading out of physical range — check wiring",
        })

    else:  # "ok"
        if is_reading_stale(created_at):
            return jsonify({
                **base_response,
                "ambient_status": "stale",
                "message": "Ambient sensor (DHT11) reading is stale — check device connectivity",
            })
        weather_condition = classify_weather(weather_temperature, weather_humidity)
        base_response["weather_condition"] = weather_condition
        base_response["ambient_status"] = "ok"

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
        return jsonify({
            **base_response,
            "message": "No crop is recommended for the given conditions. The environment is unsuitable for farming."
        })

    predicted_probabilities = model.predict_proba(new_data)
    predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)
    filtered_predictions = predictions_df.T[predictions_df.T[0] > 0].sort_values(by=0, ascending=False)

    if filtered_predictions.empty:
        return jsonify({
            **base_response,
            "message": "No crop is recommended for the given conditions. The environment is unsuitable for farming."
        })

    filtered_predictions = filtered_predictions.copy()
    if weather_condition:
        filtered_predictions["weather_score"] = [
            weather_suitability_score(crop, weather_temperature)
            for crop in filtered_predictions.index
        ]
    else:
        filtered_predictions["weather_score"] = 1.0

    filtered_predictions["weather_adjusted"] = filtered_predictions[0] * filtered_predictions["weather_score"]
    filtered_predictions = filtered_predictions.sort_values(by="weather_adjusted", ascending=False)

    most_probable_crop = filtered_predictions.index[0]

    return jsonify({
        **base_response,
        "predicted_probabilities": filtered_predictions[[0]].to_dict(),
        "weather_adjusted_probabilities": filtered_predictions[["weather_adjusted"]].rename(
            columns={"weather_adjusted": 0}
        ).to_dict(),
        "most_probable_crop": most_probable_crop
    })