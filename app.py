from flask_cors import CORS
from flask import Flask
from Crop_data.describe import statistics_bp
from Crop_data.fetch_dataset import dataset_bp

app = Flask(__name__)

CORS(app, origins='*')

app.register_blueprint(statistics_bp)

app.register_blueprint(dataset_bp)


if __name__ == '__main__':
    port = os.environ.get('PORT', 8080)
    app.run(debug=True, host='0.0.0.0', port=port)

