"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(response_body['family']), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify({
            "id": member["id"],
            "first_name": member["first_name"],
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }), 200
    return jsonify({"msg": "Member not found"}), 404

@app.route('/members', methods=['POST'])
def add_member():
    member_data = request.get_json()
    if not member_data:
        return jsonify({"msg": "Detected empty Jackson family object"}),400
    if "first_name" not in member_data:
        return jsonify({"msg": "Jackson family object needs a first name"}),400
    if "age" not in member_data:
        return jsonify({"msg": "Jackson family object needs an age"}),400
    if "lucky_numbers" not in member_data:
        return jsonify({"msg": "Jackson family object needs a lucky numbers"}),400

    jackson_family.add_member(member_data)
    return jsonify(member_data), 200
    #jackson_family.add_member(member_data)
    #return jsonify({"msg": "New family member added succesfully"}),200

@app.route('/members/<int:id>',methods=['DELETE'])
def delete_member(id):
    member = jackson_family.get_member(id)
    if member:
        jackson_family.delete_member(id)
        return jsonify({"done": True}),200
    return jsonify({"msg": "Not found Jackson family member"}),404


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
