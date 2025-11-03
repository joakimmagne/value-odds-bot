from flask import Flask, jsonify
import requests
import os
from apscheduler.schedulers.background import BackgroundScheduler
import time

app = Flask(__name__)
API_KEY = os.environ.get('ODDS_API_KEY', 'YOUR_API_KEY')
BASE_URL = 'https://api.the-odds-api.com/v4'

SPORTS = ['soccer_epl', 'americanfootball_nfl']
REGION = 'eu'
MARKETS = 'h2h'

latest_odds = []

def fetch_odds():
    global latest_odds
    all_odds = []
    for sport in SPORTS:
        resp = requests.get(f'{BASE_URL}/sports/{sport}/odds', params={
            'apiKey': API_KEY,
            'regions': REGION,
            'markets': MARKETS
        })
        if resp.status_code == 200:
            data = resp.json()
            for event in data:
                all_odds.append(event)
        else:
            print('Error fetching', sport, resp.status_code)
    latest_odds = all_odds
    print(f'Updated odds at {time.ctime()} - {len(all_odds)} events')

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_odds, 'interval', minutes=15)
scheduler.start()

@app.route('/odds')
def get_odds():
    return jsonify(latest_odds)

if __name__ == '__main__':
    fetch_odds()
    app.run(debug=True)
