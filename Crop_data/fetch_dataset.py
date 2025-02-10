from flask import Blueprint, jsonify
from Crop_data.dataset import dataset

dataset_bp = Blueprint('dataset_bp', __name__)

@dataset_bp.route('/api/get_dataset', methods=['GET'])
def get_dataset():

    data = dataset()

    return jsonify(data.to_dict(orient="records"))