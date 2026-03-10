from flask import Flask, render_template, request, jsonify
import requests

with open('api_key.txt') as f:
    API_KEY_ID = f.readline().strip()
with open('api_key_secret.txt') as f:
    API_KEY_SECRET = f.readline().strip()

app = Flask(__name__)

API_URL = "https://data.calgary.ca/resource/c2es-76ed.geojson"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    start = request.args.get("start")
    end = request.args.get("end")

    if not start or not end:
        return jsonify({"error": "Start and end date required"}), 400

    query = f"{API_URL}?$where=issueddate >= '{start}T00:00:00' AND issueddate <= '{end}T23:59:59'&$limit=500"

    response = requests.get(query)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), 500

    data = response.json()

    print(data.keys())

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)