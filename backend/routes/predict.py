
from flask import Blueprint, request, jsonify

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return "Predict route working 🚀"

    data = request.json
    return jsonify({"message": "POST working", "data": data})