from flask import Flask
from flask_cors import CORS
from routes.predict import predict_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(predict_bp)

@app.route('/')
def home():
    return "Backend Running 🚀"

if __name__ == '__main__':
    app.run(debug=True)