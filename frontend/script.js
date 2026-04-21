// IPL Teams and Venues data
const teams = [
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
];

const venues = [
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
];

// Store original team options
let originalTeamOptions = {};

// Populate dropdowns
function populateDropdowns() {
    const team1Select = document.getElementById('team1');
    const team2Select = document.getElementById('team2');
    const tossWinnerSelect = document.getElementById('toss_winner');
    const venueSelect = document.getElementById('venue');

    // Populate teams for Team 1
    teams.forEach(team => {
        const option1 = document.createElement('option');
        option1.value = team;
        option1.textContent = team;
        team1Select.appendChild(option1);
    });

    // Populate teams for Team 2 (all teams initially)
    teams.forEach(team => {
        const option2 = document.createElement('option');
        option2.value = team;
        option2.textContent = team;
        team2Select.appendChild(option2);
    });

    // Store original Team 2 options (just the teams, not the placeholder)
    originalTeamOptions.team2 = [...teams];

    // Populate venues
    venues.forEach(venue => {
        const option = document.createElement('option');
        option.value = venue;
        option.textContent = venue;
        venueSelect.appendChild(option);
    });

    // Add event listeners
    team1Select.addEventListener('change', updateTeam2Options);
    team1Select.addEventListener('change', updateTossWinnerOptions);
    document.getElementById('team2').addEventListener('change', updateTossWinnerOptions);
}

// Update Team 2 options when Team 1 is selected
function updateTeam2Options() {
    const team1Select = document.getElementById('team1');
    const team2Select = document.getElementById('team2');
    const selectedTeam1 = team1Select.value;

    // Clear all Team 2 options
    team2Select.innerHTML = '<option value="">Select Team 2</option>';

    // Add only teams that are not Team 1
    originalTeamOptions.team2.forEach(team => {
        if (team !== selectedTeam1) {
            const newOption = document.createElement('option');
            newOption.value = team;
            newOption.textContent = team;
            team2Select.appendChild(newOption);
        }
    });

    team2Select.value = ''; // Reset selection
}

// Update Toss Winner options when teams are selected
function updateTossWinnerOptions() {
    const team1Select = document.getElementById('team1');
    const team2Select = document.getElementById('team2');
    const tossWinnerSelect = document.getElementById('toss_winner');
    const selectedTeam1 = team1Select.value;
    const selectedTeam2 = team2Select.value;

    // Clear Toss Winner options except first
    while (tossWinnerSelect.options.length > 1) tossWinnerSelect.remove(1);

    // Add only the two selected teams
    if (selectedTeam1) {
        const option1 = document.createElement('option');
        option1.value = selectedTeam1;
        option1.textContent = selectedTeam1;
        tossWinnerSelect.appendChild(option1);
    }

    if (selectedTeam2) {
        const option2 = document.createElement('option');
        option2.value = selectedTeam2;
        option2.textContent = selectedTeam2;
        tossWinnerSelect.appendChild(option2);
    }

    tossWinnerSelect.value = ''; // Reset selection
}

// Handle form submission
document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const submitBtn = document.querySelector('.predict-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Predicting...';

    // Hide previous results
    document.getElementById('result').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');

    // Get form data
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    try {
        // Send POST request to backend
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            // Handle both old and new response formats
            let displayText = '';
            if (result.prediction) {
                // New format with ML model predictions
                displayText = `<strong>${result.prediction}</strong>`;
                if (result.probabilities) {
                    displayText += '<br><br><strong>Match Probabilities:</strong><br>';
                    for (const [team, prob] of Object.entries(result.probabilities)) {
                        displayText += `${team}: ${prob}%<br>`;
                    }
                }
            } else if (result.message) {
                // Old format
                displayText = result.message;
            }
            
            document.getElementById('predictionText').innerHTML = displayText;
            document.getElementById('result').classList.remove('hidden');
        } else {
            // Show error
            document.getElementById('errorText').textContent = result.error || 'An error occurred';
            document.getElementById('error').classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('errorText').textContent = 'Failed to connect to the server. Make sure the backend is running.';
        document.getElementById('error').classList.remove('hidden');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Predict Winner';
    }
});

// Initialize when page loads
document.addEventListener('DOMContentLoaded', populateDropdowns);