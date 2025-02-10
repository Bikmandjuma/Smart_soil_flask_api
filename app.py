from flask_cors import CORS
from flask import Flask
from Crop_data.describe import statistics_bp
from Crop_data.fetch_dataset import dataset_bp

app = Flask(__name__)

CORS(app, origins='*')

app.register_blueprint(statistics_bp)

app.register_blueprint(dataset_bp)


if __name__ == '__main__':
    app.run(debug=True)

