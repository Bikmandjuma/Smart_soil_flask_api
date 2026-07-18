# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from dataset import dataset

# # Load the data using the dataset function
# data = dataset()

# # Prepare feature columns (X) and target column (y)
# X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
# y = data['label']

# # Split the data into training and testing sets
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model
# model = RandomForestClassifier(random_state=0)
# model.fit(X_train, y_train)

# # Define the new data for prediction (these are the input values for which you want the prediction)
# new_data = pd.DataFrame({
#     'N': [20],
#     'P': [32],
#     'K': [53],
#     'temperature': [20.8],
#     'humidity': [82.0],
#     'ph': [6.5],
#     'rainfall': [150.9]
# })

# # Make a prediction for the new data
# predicted_crop = model.predict(new_data)

# # Display the predicted crop
# print(f"The predicted crop for the given conditions is: {predicted_crop[0]}")

#=============================================================================================================

# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from dataset import dataset

# # Load the data using the dataset function
# data = dataset()

# # Prepare feature columns (X) and target column (y)
# X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
# y = data['label']

# # Split the data into training and testing sets
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model
# model = RandomForestClassifier(random_state=0)
# model.fit(X_train, y_train)

# # Define the new data for prediction (these are the input values for which you want the prediction)
# new_data = pd.DataFrame({
#     'N': [20],
#     'P': [32],
#     'K': [53],
#     'temperature': [20.8],
#     'humidity': [82.0],
#     'ph': [6.5],
#     'rainfall': [150.9]
# })

# # Get the predicted probabilities for each crop
# predicted_probabilities = model.predict_proba(new_data)

# # Create a DataFrame with the predicted probabilities for each crop
# predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)

# # Display the predicted probabilities for each crop
# print(f"Predicted probabilities for each crop:\n{predictions_df}")

# # Get the top 3 most likely crops based on the predicted probabilities
# top_crops = predictions_df.T.sort_values(by=0, ascending=False).head(3)
# print(f"\nTop 3 predicted crops for the given conditions:\n{top_crops}")

# # Optionally, you can display the most probable crop:
# most_probable_crop = predictions_df.idxmax(axis=1)
# print(f"\nThe most probable crop for the given conditions is: {most_probable_crop[0]}")

#======================================================================================================================

# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from dataset import dataset  # Assuming your dataset function is in the "dataset.py" file

# # Load the data using the dataset function
# data = dataset()

# # Prepare feature columns (X) and target column (y)
# X = data[['pH', 'Soil EC', 'Phosphorus', 'Potassium', 'Urea', 'T.S.P', 'M.O.P', 'Moisture', 'Temperature']]
# y = data['Plant Type']

# # Split the data into training and testing sets
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model
# model = RandomForestClassifier(random_state=0)
# model.fit(X_train, y_train)

# # Define the new data for prediction (new soil conditions)
# new_data = pd.DataFrame({
#     'pH': [6.5],  # example pH value
#     'Soil EC': [0.3],  # example soil electrical conductivity
#     'Phosphorus': [12.5],  # example phosphorus content
#     'Potassium': [150],  # example potassium content
#     'Urea': [45],  # example urea value
#     'T.S.P': [18],  # example TSP value
#     'M.O.P': [22],  # example MOP value
#     'Moisture': [75],  # example moisture level
#     'Temperature': [52]  # example temperature
# })

# # Get the predicted probabilities for each crop
# predicted_probabilities = model.predict_proba(new_data)

# # Create a DataFrame with the predicted probabilities for each crop
# predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)

# # Display the predicted probabilities for each crop
# print(f"Predicted probabilities for each crop:\n{predictions_df}")

# # Get the top 3 most likely crops based on the predicted probabilities
# top_crops = predictions_df.T.sort_values(by=0, ascending=False).head(3)
# print(f"\nTop 3 predicted crops for the given conditions:\n{top_crops}")

# # Optionally, you can display the most probable crop:
# most_probable_crop = predictions_df.idxmax(axis=1)
# print(f"\nThe most probable crop for the given conditions is: {most_probable_crop[0]}")

#=================================================================================================================

# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from dataset import dataset  # Assuming your dataset function is in the "dataset.py" file

# # Load the data using the dataset function
# data = dataset()

# # Prepare feature columns (X) and target column (y)
# X = data[['pH', 'Soil EC', 'Phosphorus', 'Potassium', 'Urea', 'T.S.P', 'M.O.P', 'Moisture', 'Temperature']]
# y = data['Plant Type']

# # Split the data into training and testing sets
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model
# model = RandomForestClassifier(random_state=0)
# model.fit(X_train, y_train)

# # Define the new data for prediction (new soil conditions)
# new_data = pd.DataFrame({
#     'pH': [3.5],  # example pH value
#     'Soil EC': [0.1],  # example soil electrical conductivity
#     'Phosphorus': [5.5],  # example phosphorus content
#     'Potassium': [200],  # example potassium content
#     'Urea': [35],  # example urea value
#     'T.S.P': [28],  # example TSP value
#     'M.O.P': [20],  # example MOP value
#     'Moisture': [75],  # example moisture level
#     'Temperature': [52]  # example temperature
# })

# # Get the predicted probabilities for each crop
# predicted_probabilities = model.predict_proba(new_data)

# # Create a DataFrame with the predicted probabilities for each crop
# predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)

# # Display the predicted probabilities for each crop
# print(f"Predicted probabilities for each crop:\n{predictions_df}")

# # Define how many top crops you want to predict, e.g., top 3, top 4, etc.
# top_n = 3  # Change this to the number of top crops you want (1, 2, 3, 4, 5, etc.)

# # Get the top N most likely crops based on the predicted probabilities
# top_crops = predictions_df.T.sort_values(by=0, ascending=False).head(top_n)
# print(f"\nTop {top_n} predicted crops for the given conditions:\n{top_crops}")

# # Optionally, you can display the most probable crop:
# most_probable_crop = predictions_df.idxmax(axis=1)
# print(f"\nThe most probable crop for the given conditions is: {most_probable_crop[0]}")


#============================================================================================

# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from dataset import dataset

# # Load the dataset
# data = dataset()

# # Prepare feature columns (X) and target column (y)
# X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]  # Update with correct column names
# y = data['label']  # Crop label (target column)

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the RandomForestClassifier model
# model = RandomForestClassifier(random_state=0)
# model.fit(X_train, y_train)

# # Define the new data for prediction (environmental conditions for prediction)
# new_data = pd.DataFrame({
#     'N': [10],
#     'P': [12],
#     'K': [13],
#     'temperature': [15.8],
#     'humidity': [22.0],
#     'ph': [1.5],
#     'rainfall': [150.9]
# })

# # Get predicted probabilities for each crop
# predicted_probabilities = model.predict_proba(new_data)

# # Create a DataFrame with the predicted probabilities for each crop
# predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)

# # Display the predicted probabilities for each crop
# print(f"Predicted probabilities for each crop:\n{predictions_df}\n")

# # Function to get top N crops based on predicted probabilities
# def get_top_crops(predictions_df, top_n=3):
#     # Sort crops based on probability, in descending order
#     top_crops = predictions_df.T.sort_values(by=0, ascending=False).head(top_n)
#     return top_crops

# # Get the top N most likely crops (you can adjust top_n as needed)
# top_n = 5  # Change this number to predict top N crops (e.g., 3, 5, or even 10)
# top_crops = get_top_crops(predictions_df, top_n)

# # Display the top N crops
# print(f"\nTop {top_n} predicted crops for the given conditions:\n{top_crops}")

# # Optionally, display the most probable crop
# most_probable_crop = predictions_df.idxmax(axis=1)
# print(f"\nThe most probable crop for the given conditions is: {most_probable_crop[0]}")

#==============================================================================

# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from dataset import dataset

# # Load the dataset
# data = dataset()

# # Prepare feature columns (X) and target column (y)
# X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]  # Update with correct column names
# y = data['label']  # Crop label (target column)

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the RandomForestClassifier model
# model = RandomForestClassifier(random_state=0)
# model.fit(X_train, y_train)

# # Define the new data for prediction (environmental conditions for prediction)
# new_data = pd.DataFrame({
#     'N': [10],
#     'P': [12],
#     'K': [13],
#     'temperature': [15.8],
#     'humidity': [22.0],
#     'ph': [1.5],
#     'rainfall': [150.9]
# })

# # Get predicted probabilities for each crop
# predicted_probabilities = model.predict_proba(new_data)

# # Create a DataFrame with the predicted probabilities for each crop
# predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)

# # Display the predicted probabilities for each crop
# print(f"Predicted probabilities for each crop:\n{predictions_df}\n")

# # Function to get top crops based on predicted probabilities
# def get_top_crops(predictions_df):
#     # Sort crops based on probability, in descending order
#     top_crops = predictions_df.T.sort_values(by=0, ascending=False)
#     return top_crops

# # Get the top predicted crops
# top_crops = get_top_crops(predictions_df)

# # Display the top predicted crops
# print(f"\nTop predicted crops for the given conditions:\n{top_crops}")

# # Optionally, display the most probable crop
# most_probable_crop = predictions_df.idxmax(axis=1)
# print(f"\nThe most probable crop for the given conditions is: {most_probable_crop[0]}")

#================================================================

# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from dataset import dataset

# # Load the dataset
# data = dataset()

# # Prepare feature columns (X) and target column (y)
# X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]  # Update with correct column names
# y = data['label']  # Crop label (target column)

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the RandomForestClassifier model
# model = RandomForestClassifier(random_state=0)
# model.fit(X_train, y_train)

# # Define the new data for prediction (environmental conditions for prediction)
# new_data = pd.DataFrame({
#     'N': [30],
#     'P': [22],
#     'K': [43],
#     'temperature': [10.8],
#     'humidity': [12.0],
#     'ph': [2.5],
#     'rainfall': [200.9]
# })

# # Get predicted probabilities for each crop
# predicted_probabilities = model.predict_proba(new_data)

# # Create a DataFrame with the predicted probabilities for each crop
# predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)

# # Filter out crops with zero probability
# filtered_predictions = predictions_df.T[predictions_df.T[0] > 0].sort_values(by=0, ascending=False)

# # Display the predicted probabilities for each crop
# print("\nPredicted probabilities for each crop:")
# print(filtered_predictions)

# # Get the most probable crop
# most_probable_crop = filtered_predictions.index[0]
# print(f"\nThe most probable crop for the given conditions is: {most_probable_crop}")

#================================================================================

# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from dataset import dataset

# # Load the dataset
# data = dataset()

# # Prepare feature columns (X) and target column (y)
# X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]  # Update with correct column names
# y = data['label']  # Crop label (target column)

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the RandomForestClassifier model
# model = RandomForestClassifier(random_state=0)
# model.fit(X_train, y_train)

# # Define the new data for prediction (environmental conditions for prediction)
# new_data = pd.DataFrame({
#     'N': [0],
#     'P': [0],
#     'K': [0],
#     'temperature': [0],
#     'humidity': [0],
#     'ph': [0],  # If pH is too low, crops may not be recommended
#     'rainfall': [0]
# })

# # Get predicted probabilities for each crop
# predicted_probabilities = model.predict_proba(new_data)

# # Create a DataFrame with the predicted probabilities for each crop
# predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)

# # Filter out crops with zero probability
# filtered_predictions = predictions_df.T[predictions_df.T[0] > 0].sort_values(by=0, ascending=False)

# # Check if there are any recommended crops
# if filtered_predictions.empty:
#     print("\nNo crop is recommended for the given conditions. The environment may be unsuitable for farming.")
# else:
#     # Display the predicted probabilities for each crop
#     print("\nPredicted probabilities for each crop:")
#     print(filtered_predictions)

#     # Get the most probable crop
#     most_probable_crop = filtered_predictions.index[0]
#     print(f"\nThe most probable crop for the given conditions is: {most_probable_crop}")

#===================================================================================

# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from dataset import dataset

# # Load the dataset
# data = dataset()

# # Prepare feature columns (X) and target column (y)
# X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
# y = data['label']

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the RandomForestClassifier model
# model = RandomForestClassifier(random_state=0)
# model.fit(X_train, y_train)

# # Define new data for prediction
# new_data = pd.DataFrame({
#     'N': [0],
#     'P': [0],
#     'K': [0],
#     'temperature': [0],
#     'humidity': [0],
#     'ph': [2],
#     'rainfall': [0]
# })

# # **Check if input values are too low to support crops**
# if new_data.sum(axis=1).values[0] == 0:  # If all values are zero
#     print("\nNo crop is recommended for the given conditions. The environment is unsuitable for farming.")
# else:
#     # Get predicted probabilities
#     predicted_probabilities = model.predict_proba(new_data)

#     # Create a DataFrame with the predicted probabilities
#     predictions_df = pd.DataFrame(predicted_probabilities, columns=model.classes_)

#     # Filter out crops with zero probability
#     filtered_predictions = predictions_df.T[predictions_df.T[0] > 0].sort_values(by=0, ascending=False)

#     # Check if any crop is recommended
#     if filtered_predictions.empty:
#         print("\nNo crop is recommended for the given conditions. The environment is unsuitable for farming.")
#     else:
#         # Display the predicted probabilities for each crop
#         print("\nPredicted probabilities for each crop:")
#         print(filtered_predictions)

#         # Get the most probable crop
#         most_probable_crop = filtered_predictions.index[0]
#         print(f"\nThe most probable crop for the given conditions is: {most_probable_crop}")

#===============================================================================================


# from openai import OpenAI
# import os
# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from flask import Blueprint, jsonify, request
# import requests
# from Crop_data.dataset import dataset
# from Crop_data.laravel_url_api import Laravel_url_api

# crop_prediction_bp = Blueprint('crop_prediction_bp', __name__)

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

# from dotenv import load_dotenv
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
# load_dotenv()
# os.getenv("GROQ_API_KEY")
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


# @crop_prediction_bp.route('/api/crop_agronomy_advice', methods=['GET'])
# def crop_agronomy_advice():
#     crop_name = request.args.get('crop')

#     if not crop_name:
#         return jsonify({"message": "Missing 'crop' query parameter"}), 400

#     try:
#         advice = get_agronomy_advice(crop_name)
#         return jsonify(advice)
#     except RuntimeError as e:
#         return jsonify({"message": str(e)}), 500
#     except Exception as e:
#         return jsonify({"message": f"Failed to generate agronomy advice: {str(e)}"}), 500


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
