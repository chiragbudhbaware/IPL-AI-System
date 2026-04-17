from flask import Blueprint, request, jsonify

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Dummy response
    return jsonify({
        "message": "API working",
        "data_received": data
    })