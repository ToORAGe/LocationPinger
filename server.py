from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import atexit

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure the SQLite database
# Use the absolute path for the SQLite database
db_path = os.path.join(os.path.dirname(__file__), 'locations.db')
print("This is DB path", db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Store the latest location
latest_location = {"latitude": None, "longitude": None}

# Define the Location model
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

# Create tables before the first request
with app.app_context():
    db.create_all()

@app.route('/location', methods=['POST'])
def add_location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    if latitude is None or longitude is None:
        return jsonify({'message': 'Invalid data'}), 400

    new_location = Location(latitude=latitude, longitude=longitude)
    db.session.add(new_location)
    db.session.commit()
    return jsonify({'message': 'Location added successfully'}), 201

@app.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return jsonify([{'latitude': loc.latitude, 'longitude': loc.longitude} for loc in locations])

@app.route('/clear', methods=['POST'])
def clear_data():
    db.drop_all()
    db.create_all()
    return jsonify({'message': 'Database cleared'}), 200

def delete_database():
    if os.path.exists('locations.db'):
        os.remove('locations.db')

atexit.register(delete_database)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)