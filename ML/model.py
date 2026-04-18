import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

print("Loading dataset...")

# Load dataset
df = pd.read_csv('../data/matches.csv')

# -------------------------------
# 🧹 DATA CLEANING
# -------------------------------

df = df.dropna(subset=['winner'])
df = df[['team1', 'team2', 'toss_winner', 'toss_decision', 'venue', 'winner']]
df = df[df['team1'] != df['team2']]

# 🔁 Rename old teams
team_replace = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Kings XI Punjab': 'Punjab Kings'
}

for col in ['team1', 'team2', 'toss_winner', 'winner']:
    df[col] = df[col].replace(team_replace)

# ✅ Keep only current teams
valid_teams = [
    'Chennai Super Kings',
    'Delhi Capitals',
    'Gujarat Titans',
    'Kolkata Knight Riders',
    'Lucknow Super Giants',
    'Mumbai Indians',
    'Punjab Kings',
    'Rajasthan Royals',
    'Royal Challengers Bangalore',
    'Sunrisers Hyderabad'
]

df = df[
    df['team1'].isin(valid_teams) &
    df['team2'].isin(valid_teams) &
    df['toss_winner'].isin(valid_teams) &
    df['winner'].isin(valid_teams)
]

# 🏟️ Normalize venue names
df['venue'] = df['venue'].replace({
    'Wankhede Stadium, Mumbai': 'Wankhede Stadium',
    'M Chinnaswamy Stadium, Bengaluru': 'M Chinnaswamy Stadium',
    'Eden Gardens, Kolkata': 'Eden Gardens',
    'MA Chidambaram Stadium, Chepauk': 'MA Chidambaram Stadium',
    'MA Chidambaram Stadium, Chepauk, Chennai': 'MA Chidambaram Stadium',
    'Rajiv Gandhi International Stadium, Uppal': 'Rajiv Gandhi International Stadium',
    'Rajiv Gandhi International Stadium, Uppal, Hyderabad': 'Rajiv Gandhi International Stadium',
    'Arun Jaitley Stadium, Delhi': 'Arun Jaitley Stadium',
    'Sawai Mansingh Stadium, Jaipur': 'Sawai Mansingh Stadium'
})

# 🏟️ Keep only home venues
home_venues = [
    'Wankhede Stadium',
    'MA Chidambaram Stadium',
    'M Chinnaswamy Stadium',
    'Eden Gardens',
    'Rajiv Gandhi International Stadium',
    'Arun Jaitley Stadium',
    'Sawai Mansingh Stadium',
    'Punjab Cricket Association Stadium, Mohali',
    'Narendra Modi Stadium, Ahmedabad',
    'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow'
]

df = df[df['venue'].isin(home_venues)]

# -------------------------------
# 📋 SHOW OPTIONS
# -------------------------------

teams = sorted(df['team1'].unique())
venues = sorted(df['venue'].unique())

print("Encoding data...")

# -------------------------------
# 🔢 ENCODING
# -------------------------------

encoders = {}

for col in df.columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# -------------------------------
# 🤖 MODEL TRAINING
# -------------------------------

X = df.drop('winner', axis=1)
y = df['winner']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training model...")

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,          # 🔥 reduce from 10 → 6
    min_samples_split=10, # 🔥 increase from 5 → 10
    min_samples_leaf=3,   # 🔥 NEW (very important)
    random_state=42
)

model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
print("✅ Final Accuracy:", accuracy_score(y_test, y_pred))

# Save
pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(encoders, open('encoders.pkl', 'wb'))

print("✅ Model and encoders saved!")

# -------------------------------
# 🔥 USER INPUT (SMART)
# -------------------------------

print("\n========== IPL MATCH PREDICTOR ==========")

print("\nAvailable Teams:")
for t in teams:
    print("-", t)

teams_lower = [t.lower() for t in teams]

team1 = input("\nEnter Team 1: ").lower()
team2 = input("Enter Team 2: ").lower()
toss_winner = input("Enter Toss Winner: ").lower()

if team1 not in teams_lower or team2 not in teams_lower or toss_winner not in teams_lower:
    print("\n❌ Invalid team name")
    exit()

team1 = teams[teams_lower.index(team1)]
team2 = teams[teams_lower.index(team2)]
toss_winner = teams[teams_lower.index(toss_winner)]

print("\nToss Decision Options: bat / field")
toss_decision = input("Enter Toss Decision: ")

print("\nAvailable Venues:")
for v in venues:
    print("-", v)

venues_lower = [v.lower() for v in venues]

venue = input("\nEnter Venue: ").lower()

if venue not in venues_lower:
    print("\n❌ Invalid venue")
    exit()

venue = venues[venues_lower.index(venue)]

# -------------------------------
# 🔮 PREDICTION
# -------------------------------

input_data = {
    'team1': team1,
    'team2': team2,
    'toss_winner': toss_winner,
    'toss_decision': toss_decision,
    'venue': venue
}

input_df = pd.DataFrame([input_data])

for col in input_df.columns:
    input_df[col] = encoders[col].transform(input_df[col])

probs = model.predict_proba(input_df)[0]
classes = encoders['winner'].classes_

team_probs = {}

for i, team in enumerate(classes):
    if team == team1 or team == team2:
        team_probs[team] = probs[i]

total = sum(team_probs.values())

print("\n🏏 Match Prediction:")
for team, prob in team_probs.items():
    print(f"{team}: {(prob/total)*100:.2f}%")