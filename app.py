from flask_cors import CORS
from flask import Flask
from Crop_data.describe import statistics_bp
from Crop_data.fetch_dataset import dataset_bp
from Crop_data.crop_prediction import crop_prediction_bp

app = Flask(__name__)

CORS(app, origins='*')

app.register_blueprint(statistics_bp)
app.register_blueprint(dataset_bp)
app.register_blueprint(crop_prediction_bp)

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

