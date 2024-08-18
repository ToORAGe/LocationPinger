from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store the latest location
latest_location = {"latitude": None, "longitude": None}

@app.route('/location', methods=['POST'])
def update_location():
    global latest_location
    data = request.get_json()
    latest_location = {
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude")
    }
    return jsonify(success=True)

@app.route('/latest-location', methods=['GET'])
def get_latest_location():
    return jsonify(latest_location)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
