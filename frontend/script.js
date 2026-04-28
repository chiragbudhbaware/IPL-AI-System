// Frontend script: fetches config from backend, posts prediction requests, and renders a pie chart

let teams = [];
let venues = [];
const fallbackTeams = [
    'Chennai Super Kings','Delhi Capitals','Gujarat Titans','Kolkata Knight Riders','Lucknow Super Giants','Mumbai Indians','Punjab Kings','Rajasthan Royals','Royal Challengers Bangalore','Sunrisers Hyderabad'
];
const fallbackVenues = [
    'Wankhede Stadium','MA Chidambaram Stadium','M Chinnaswamy Stadium','Eden Gardens','Rajiv Gandhi International Stadium','Arun Jaitley Stadium','Sawai Mansingh Stadium','Punjab Cricket Association Stadium, Mohali','Narendra Modi Stadium, Ahmedabad','Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow'
];

let originalTeamOptions = {};
let probChart = null;

function populateDropdowns() {
    const team1Select = document.getElementById('team1');
    const team2Select = document.getElementById('team2');
    const tossWinnerSelect = document.getElementById('toss_winner');
    const venueSelect = document.getElementById('venue');

    // clear any existing options (except placeholder)
    team1Select.innerHTML = '<option value="">Select Team 1</option>';
    team2Select.innerHTML = '<option value="">Select Team 2</option>';
    tossWinnerSelect.innerHTML = '<option value="">Select Toss Winner</option>';
    venueSelect.innerHTML = '<option value="">Select Venue</option>';

    teams.forEach(team => {
        const opt1 = document.createElement('option'); opt1.value = team; opt1.textContent = team; team1Select.appendChild(opt1);
        const opt2 = document.createElement('option'); opt2.value = team; opt2.textContent = team; team2Select.appendChild(opt2);
    });

    originalTeamOptions.team2 = [...teams];

    venues.forEach(v => {
        const o = document.createElement('option'); o.value = v; o.textContent = v; venueSelect.appendChild(o);
    });

    team1Select.addEventListener('change', updateTeam2Options);
    team1Select.addEventListener('change', updateTossWinnerOptions);
    team2Select.addEventListener('change', updateTossWinnerOptions);
}

function updateTeam2Options() {
    const team1Select = document.getElementById('team1');
    const team2Select = document.getElementById('team2');
    const selected = team1Select.value;
    team2Select.innerHTML = '<option value="">Select Team 2</option>';
    originalTeamOptions.team2.forEach(t => { if (t !== selected) { const o = document.createElement('option'); o.value=t; o.textContent=t; team2Select.appendChild(o);} });
}

function updateTossWinnerOptions() {
    const team1Select = document.getElementById('team1');
    const team2Select = document.getElementById('team2');
    const tossWinnerSelect = document.getElementById('toss_winner');
    const a = team1Select.value, b = team2Select.value;

    tossWinnerSelect.innerHTML = '<option value="">Select Toss Winner</option>';
    if (a) { const o = document.createElement('option'); o.value=a; o.textContent=a; tossWinnerSelect.appendChild(o); }
    if (b) { const o = document.createElement('option'); o.value=b; o.textContent=b; tossWinnerSelect.appendChild(o); }
}

async function postPredict(data) {
    const url = 'http://127.0.0.1:5000/predict';
    const res = await fetch(url, {
        method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(data)
    });
    return res;
}

function clearResultArea() {
    document.getElementById('predictionText').textContent = '';
    document.getElementById('probabilities').innerHTML = '';
    const canvas = document.getElementById('probChart');
    if (probChart) { try { probChart.destroy(); } catch(e){} probChart = null; }
}

document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = document.querySelector('.predict-btn');
    submitBtn.disabled = true; submitBtn.textContent = 'Predicting...';
    document.getElementById('error').classList.add('hidden');
    clearResultArea();

    const formData = new FormData(e.target); const data = Object.fromEntries(formData);

    try {
        const response = await postPredict(data);
        const result = await response.json().catch(()=>({}));
        if (!response.ok) {
            document.getElementById('errorText').textContent = result.error || 'Prediction failed';
            document.getElementById('error').classList.remove('hidden');
            return;
        }

        // success
        document.getElementById('predictionText').textContent = result.prediction || '';
        if (result.probabilities && Object.keys(result.probabilities).length) {
            const entries = Object.entries(result.probabilities);
            const labels = entries.map(e=>e[0]);
            const values = entries.map(e=>Number(e[1]));

            // textual list
            const container = document.getElementById('probabilities');
            entries.forEach(([team, p])=>{
                const row = document.createElement('div'); row.className='prob-row'; row.textContent = `${team} — ${Number(p).toFixed(1)}%`; container.appendChild(row);
            });

            // determine max/min indices
            const maxIndex = values.indexOf(Math.max(...values));
            const minIndex = values.indexOf(Math.min(...values));
            const colors = values.map((_,i)=> i===maxIndex? '#10b981' : i===minIndex? '#ef4444' : '#60a5fa');

            // draw pie
            try {
                const ctx = document.getElementById('probChart').getContext('2d');
                if (probChart) { probChart.destroy(); probChart = null; }
                probChart = new Chart(ctx, {
                    type: 'pie',
                    data: { labels: labels, datasets: [{ data: values, backgroundColor: colors, borderColor: '#fff', borderWidth: 2 }]},
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { position: 'bottom', labels: { color: '#0f172a' } }
                        }
                    }
                });
            } catch (err) { console.warn('Chart error', err); }
        }

        document.getElementById('result').classList.remove('hidden');
    } catch (err) {
        console.error(err);
        document.getElementById('errorText').textContent = 'Failed to connect to the server. Make sure the backend is running.';
        document.getElementById('error').classList.remove('hidden');
    } finally {
        submitBtn.disabled = false; submitBtn.textContent = 'Predict Winner';
    }
});

// load config then populate
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const res = await fetch('http://127.0.0.1:5000/config');
        if (res.ok) { const cfg = await res.json(); teams = cfg.teams || fallbackTeams; venues = cfg.venues || fallbackVenues; }
        else { teams = fallbackTeams; venues = fallbackVenues; }
    } catch (e) { teams = fallbackTeams; venues = fallbackVenues; }
    populateDropdowns();
});
