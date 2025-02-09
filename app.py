# from flask import Flask, request, jsonify
# import pickle
# import numpy as np

# app = Flask(__name__)

# # Load trained model
# model = pickle.load(open('crop_model.pkl', 'rb'))

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()
    
#     ph = data['ph']
#     temperature = data['temperature']
#     moisture = data['moisture']
#     nutrient = data['nutrient']
    
#     # Convert input data into an array
#     input_data = np.array([[ph, temperature, moisture, nutrient]])

#     # Get prediction from the ML model
#     prediction = model.predict(input_data)
    
#     return jsonify({'crop': prediction[0]})

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, request, jsonify
# import pickle
# import numpy as np

# app = Flask(__name__)

# # Load trained model
# model = pickle.load(open('crop_model.pkl', 'rb'))

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.get_json()

#         # Extract input features
#         ph = data.get('ph')
#         temperature = data.get('temperature')
#         moisture = data.get('moisture')
#         nutrient = data.get('nutrient')

#         # Validate inputs
#         if None in [ph, temperature, moisture, nutrient]:
#             return jsonify({'error': 'Missing input values'}), 400

#         # Convert input data into an array
#         input_data = np.array([[ph, temperature, moisture, nutrient]])

#         # Get prediction from the ML model
#         prediction = model.predict(input_data)

#         # Convert NumPy data type to standard Python type
#         crop_recommendation = int(prediction[0])  

#         return jsonify({'status': 'success', 'crop': crop_recommendation})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load trained model
model = pickle.load(open('crop_model.pkl', 'rb'))

# Define a dictionary to map the crop recommendation number to crop names
crop_names = {
    0: "Wheat",
    1: "Rice",
    2: "Maize",
    3: "Barley",
    # Add more crops based on your model output
}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    ph = data['ph']
    temperature = data['temperature']
    moisture = data['moisture']
    nutrient = data['nutrient']
    
    # Convert input data into an array
    input_data = np.array([[ph, temperature, moisture, nutrient]])

    # Get prediction from the ML model
    prediction = model.predict(input_data)
    
    # Map the prediction to the crop name
    crop_name = crop_names.get(prediction[0], "Unknown Crop")
    
    return jsonify({'status': 'success', 'crop_recommendation': crop_name})

if __name__ == '__main__':
    app.run(debug=True)
