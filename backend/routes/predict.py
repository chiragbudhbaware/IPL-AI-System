# # # from flask import Blueprint, request, jsonify
# # # from utils.preprocess import transform_input

# # # predict_bp = Blueprint('predict', __name__)

# # # @predict_bp.route('/predict', methods=['POST'])
# # # def predict():
# # #     data = request.json

# # #     required_fields = ['team1', 'team2', 'toss_winner', 'toss_decision', 'venue']

# # #     for field in required_fields:
# # #         if field not in data:
# # #             return jsonify({"error": f"{field} is missing"}), 400

# # #     processed = transform_input(data)

# # #     return jsonify({
# # #         "message": "Preprocessing ready",
# # #         "processed_data": processed
# # #     })

# # from flask import Blueprint, request, jsonify

# # predict_bp = Blueprint('predict', __name__)

# # @predict_bp.route('/predict', methods=['POST'])
# # def predict():
# #     data = request.json

# #     required_fields = ['team1', 'team2', 'toss_winner', 'toss_decision', 'venue']

# #     # Check missing fields
# #     for field in required_fields:
# #         if field not in data:
# #             return jsonify({"error": f"{field} is missing"}), 400

# #     return jsonify({
# #         "message": "Input validated successfully",
# #         "input": data
# #     })

# from flask import Blueprint, request, jsonify
# from utils.preprocess import transform_input

# predict_bp = Blueprint('predict', __name__)

# @predict_bp.route('/predict', methods=['POST'])
# def predict():
#     data = request.json

#     required_fields = ['team1', 'team2', 'toss_winner', 'toss_decision', 'venue']

#     for field in required_fields:
#         if field not in data:
#             return jsonify({"error": f"{field} is missing"}), 400

#     processed = transform_input(data)

#     return jsonify({
#         "message": "Preprocessing ready",
#         "processed_data": processed
#     })

from flask import Blueprint, request, jsonify

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return "Predict route working 🚀"

    data = request.json
    return jsonify({"message": "POST working", "data": data})