from flask import Blueprint, jsonify
from Crop_data.dataset import dataset

# Create a Blueprint
statistics_bp = Blueprint('statistics', __name__)

@statistics_bp.route('/api/statistics', methods=['GET'])
def get_statistics():
    data = dataset()
    summary = data.describe().to_dict()
    return jsonify(summary)
