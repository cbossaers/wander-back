import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

from .api_authentication import auth_blueprint
from .api_user import user_blueprint
from .api_itinerary import itinerary_blueprint

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")

CORS(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(itinerary_blueprint, url_prefix='/itnr')


SWAGGER_URL = '/api/docs'
API_URL = '/swagger'

# Route for generating Swagger JSON and Swagger UI blueprint
@app.route(API_URL)
def swagger_json():
    swag = swagger(app)
    swag['info']['version'] = "0.1"
    swag['info']['title'] = "Wander API"
    return jsonify(swag)

# Swagger UI blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Wander API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7436)
