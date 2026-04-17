import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, '../models/model.pkl')
TEAM_ENCODER_PATH = os.path.join(BASE_DIR, '../models/team_encoder.pkl')
VENUE_ENCODER_PATH = os.path.join(BASE_DIR, '../models/venue_encoder.pkl')