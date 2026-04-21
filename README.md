# IPL AI System Frontend

A modern web interface for predicting IPL match winners using machine learning.

## Features

- Clean, responsive design
- Form validation
- Real-time prediction results
- Error handling

## Usage

1. Ensure the backend is running on `http://localhost:5000`
2. Open `index.html` in a web browser
3. Fill in the match details and click "Predict Winner"

## Files

- `index.html` - Main HTML page
- `styles.css` - CSS styling
- `script.js` - JavaScript functionality

## API Endpoint

The frontend sends POST requests to `/predict` with JSON data containing:
- team1
- team2
- toss_winner
- toss_decision
- venue