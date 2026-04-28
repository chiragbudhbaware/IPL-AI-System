
from flask import Blueprint, request, jsonify
import pickle
import pandas as pd
import os
import json

predict_bp = Blueprint('predict', __name__)

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, '..', '..', 'ML', 'model.pkl')
encoders_path = os.path.join(script_dir, '..', '..', 'ML', 'encoders.pkl')
config_path = os.path.join(script_dir, '..', '..', 'data', 'config.json')

# Load config (teams & venues)
try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    teams = config.get('teams', [])
    venues = config.get('venues', [])
except Exception:
    teams = []
    venues = []
    config = {}

# Load model and encoders
try:
    model = pickle.load(open(model_path, 'rb'))
    encoders = pickle.load(open(encoders_path, 'rb'))
    print("Model and encoders loaded successfully")
except FileNotFoundError:
    model = None
    encoders = None
    print("Model files not found. Please train the model first.")


@predict_bp.route('/config', methods=['GET'])
def get_config():
    return jsonify({"teams": teams, "venues": venues})


@predict_bp.route('/predict', methods=['POST'])
def predict():
    if model is None or encoders is None:
        return jsonify({"error": "Model not trained. Please run ML/model.py first."}), 500

    data = request.json or {}

    required_fields = ['team1', 'team2', 'toss_winner', 'toss_decision', 'venue']

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is missing"}), 400

    # Validate inputs using config lists
    valid_teams = teams
    valid_venues = venues

    if data['team1'] not in valid_teams or data['team2'] not in valid_teams:
        return jsonify({"error": "Invalid team names"}), 400

    if data['toss_winner'] not in valid_teams:
        return jsonify({"error": "Invalid toss winner"}), 400

    if data['toss_decision'] not in ['bat', 'field']:
        return jsonify({"error": "Invalid toss decision"}), 400

    if data['venue'] not in valid_venues:
        return jsonify({"error": "Invalid venue"}), 400

    # Make prediction
    input_data = {
        'team1': data['team1'],
        'team2': data['team2'],
        'toss_winner': data['toss_winner'],
        'toss_decision': data['toss_decision'],
        'venue': data['venue']
    }

    input_df = pd.DataFrame([input_data])

    for col in input_df.columns:
        input_df[col] = encoders[col].transform(input_df[col])

    probs = model.predict_proba(input_df)[0]
    classes = encoders['winner'].classes_

    team_probs = {classes[i]: probs[i] for i in range(len(classes)) if classes[i] in (data['team1'], data['team2'])}

    total = sum(team_probs.values())

    winner = max(team_probs, key=team_probs.get)
    confidence = (team_probs[winner] / total) * 100 if total > 0 else 0

    return jsonify({
        "prediction": f"{winner} is predicted to win with {confidence:.1f}% confidence",
        "winner": winner,
        "confidence": round(confidence, 1),
        "probabilities": {team: round((prob/total)*100, 1) for team, prob in team_probs.items()} if total > 0 else {}
    })
