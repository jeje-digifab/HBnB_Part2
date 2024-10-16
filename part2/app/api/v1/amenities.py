from flask import Flask, jsonify, request, abort
from models.amenity import Amenity
# import a storage (SQL) in the future

app = Flask(__name__)

# GET : get all amenities
@app.route('/api/v1/amenities', methods=['GET'])
def get_amenities():
    all_amenities = storage.all(Amenity)  # Récupère toutes les amenities
    amenities_list = [amenity.to_dict() for amenity in all_amenities.values()]
    return jsonify(amenities_list)

# GET : get amenity by his id
@app.route('/api/v1/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)  # if amenity does not exist
    return jsonify(amenity.to_dict())

# POST : Create amenity
@app.route('/api/v1/amenities', methods=['POST'])
def create_amenity():
    if not request.json or 'name' not in request.json:
        abort(400, description="Missing name")
    new_amenity = Amenity(name=request.json['name'])
    storage.save(new_amenity)  # Sauvegarde dans la base de données
    return jsonify(new_amenity.to_dict()), 201

# PUT : Update amenity
@app.route('/api/v1/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' in request.json:
        amenity.name = request.json['name']
    storage.save(amenity)
    return jsonify(amenity.to_dict())

# DELETE : delete amenity
@app.route('/api/v1/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    return jsonify({}), 200

if __name__ == "__main__":
    app.run(debug=True)
