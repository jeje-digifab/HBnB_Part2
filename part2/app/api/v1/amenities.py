from flask import Flask, jsonify, request, abort
from app.models.amenity import Amenity
app = Flask(__name__)

# list to stock Amenities
amenities = []

# Endpoint to get all amenities
@app.route('/api/v1/amenities', methods=['GET'])
def get_amenities():
    return jsonify([amenity.__dict__ for amenity in amenities]), 200

# Endpoint to get amenity by ID
@app.route('/api/v1/amenities/<int:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = next((a for a in amenities if a.id == amenity_id), None)
    if amenity is None:
        abort(404, description="Amenity not found")
    return jsonify(amenity.__dict__), 200

# Endpoint to create amenity
@app.route('/api/v1/amenities', methods=['POST'])
def create_amenity():
    if not request.json or 'name' not in request.json:
        abort(400, description="Name is required")
    name = request.json['name']
    new_amenity = Amenity(name)
    amenities.append(new_amenity)
    return jsonify(new_amenity.__dict__), 201

# Endpoint to update amenity
@app.route('/api/v1/amenities/<int:amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = next((a for a in amenities if a.id == amenity_id), None)
    if amenity is None:
        abort(404, description="Amenity not found")
    if not request.json or 'name' not in request.json:
        abort(400, description="Name is required")
    amenity.name = request.json['name']
    return jsonify(amenity.__dict__), 200

if __name__ == '__main__':
    app.run(debug=True)
