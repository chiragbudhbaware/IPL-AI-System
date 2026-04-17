# from flask import Flask
# from flask_cors import CORS
# from routes.predict import predict_bp

# app = Flask(__name__)
# CORS(app)

# app.register_blueprint(predict_bp)

# @app.route('/')
# def home():
#     return "Backend Running 🚀"

# @predict_bp.route('/predict', methods=['GET', 'POST'])
# def predict():
#     if request.method == 'GET':
#         return "Predict route is working 🚀"

#     data = request.json
#     return jsonify({"message": "POST working", "data": data})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask
from flask_cors import CORS
from routes.predict import predict_bp

app = Flask(__name__)
CORS(app)

# Register blueprint AFTER routes are defined
app.register_blueprint(predict_bp)

@app.route('/')
def home():
    return "Backend Running 🚀"

if __name__ == '__main__':
    app.run(debug=True)