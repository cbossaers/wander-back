import os
from dotenv import load_dotenv
import requests
from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token

from ..logic.hashing import Hashing as Hash

load_dotenv()

auth_blueprint = Blueprint('auth', __name__)

# Configuration
auth_blueprint.config = {
    'JWT_SECRET_KEY': os.environ.get("JWT_SECRET_KEY")
}
jwt_auth = JWTManager(auth_blueprint)


@auth_blueprint.route('/signin', methods=['POST', 'OPTIONS'])
def login():
    """
    User Sign-In
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        description: Itinerary object that needs to be created
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Successful response
        schema:
          type: object
          properties:
            access_token:
              type: string
            userdata:
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
            access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
            userdata:
                email: cristian@upv.com
                name: Cristian
                picture: none
                
      400:
        description: Invalid request or missing data
        schema:
          type: object
          properties:
            code:
              type: integer
            title:
              type: string
        examples:
          application/json:
            code: 109
            title: Email or password not provided
      401:
        description: Unauthorized access
        schema:
          type: object
          properties:
            code:
              type: integer
            title:
              type: string
        examples:
          application/json:
            code: 108
            title: User not found
    """
    if request.method == 'OPTIONS':
        # Respond to the preflight request
        response = jsonify({'message': 'Preflight request received'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    email = request.json.get('email')
    password = request.json.get('password')

    # Input validation
    if not email or not password:
        return jsonify({'error': 109}), 400

    verified = Hash.verify_password(email, password)

    if verified:
        access_token = create_access_token(identity=email)
        userdata = request_user(email)
        response_data = {'access_token': access_token, 'userdata': userdata}
        return response_data, 200

    return jsonify({'error': 108}), 401


@auth_blueprint.route('/')
def index():
    # A welcome message to test the authentication server
    return "<h1>Welcome to the authentication server!</h1>"


def request_user(email):
    url = 'http://127.0.0.1:7436/user/getuser'
    headers = {
        'user': email
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        # Handle request exceptions here
        print(f'Request failed: {e}')
        return None
