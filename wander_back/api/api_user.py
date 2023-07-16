from flask import Blueprint, jsonify, request
from email_validator import EmailNotValidError
import psycopg
from flask_jwt_extended import jwt_required

from ..classes.class_user import User
from ..dal.dal_user import DalUser as Dal
from ..logic.hashing import Hashing as Hash

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/getuser', methods=['GET'])
def get_user():
    """
    Get user information
    ---
    tags:
      - User
    parameters:
      - name: user
        in: header
        type: string
        required: true
        description: User email
    responses:
      200:
        description: Successful response
        schema:
          type: object
          properties:
            email:
              type: string
            name:
              type: string
            picture:
              type: string
        examples:
          application/json:
            email: cristian@upv.com
            name: Cristian
            picture: none
      400:
        description: Invalid request or error occurred
        schema:
          type: object
          properties:
            code:
              type: integer
            title:
              type: string
        examples:
          application/json:
            code: 115
            title: User not found
    """
    user_email = request.headers.get("user")
    user_data = Dal.GetUser(user_email)
    if(user_data is None):
        return jsonify({'error': 115}), 400
    return jsonify(user_data), 200

@user_blueprint.route('/signup', methods=['POST', 'OPTIONS'])
def create_user():
    """
    Create a new user.
    ---
    tags:
      - User
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
            password:
              type: string
    responses:
      201:
        description: User created successfully
      400:
        description: Invalid request or error occurred
    """
    if request.method == 'OPTIONS':
        # Respond to the preflight request
        response = jsonify({'message': 'Preflight request received'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    args = request.json
    try:
        new_user = User(args["name"], args["email"], Hash.hash_password(args["password"]))
        Dal.AddUser(new_user)

        return jsonify({'message': "User created successfully"}), 201
    except EmailNotValidError as error:
        # needs to be updated to python 3.10 to use match-case
        if error.args[0] == "The part after the @-sign is not valid. It should have a period.":
            return jsonify({'error': 105}), 400
        elif error.args[0] == "The email address is not valid. It must have exactly one @-sign.":
            return jsonify({'error': 106}), 400
        else:
            return jsonify({'error': 999}), 400
    except ValueError as error:
        return jsonify({'error': error.args[0]}), 400
    except psycopg.IntegrityError:
        return jsonify({'error': 107}), 400

@user_blueprint.route('/update', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user_id = request.args.get('user_id')
    # Implement the logic to update a user here
    return jsonify({'message': f'User {user_id} updated successfully'}), 200


@user_blueprint.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """
    Delete user
    ---
    tags:
      - User
    parameters:
      - name: user_id
        in: query
        type: string
        required: true
        description: User ID
      - name: user_token
        in: query
        type: string
        required: true
        description: User Token
    responses:
      200:
        description: User deleted successfully
    """
    user_id = request.args.get('user_id')
    # Implement the logic to delete a user here
    return jsonify({'message': f'User {user_id} deleted successfully'}), 200