import os
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required
import json
import datetime as dt

from ..classes.class_itinerary import Itinerary
from ..classes.class_day import Day
from ..classes.class_activity import Activity
from ..dal.dal_itinerary import DalItinerary as DalIt
from ..dal.dal_day import DalDay as DalDay
from ..dal.dal_activity import DalActivity as DalAct

load_dotenv()

itinerary_blueprint = Blueprint(
    'itinerary', __name__)  # Create a Blueprint object

# Configuration
itinerary_blueprint.config = {
    'JWT_SECRET_KEY': os.environ.get("JWT_SECRET_KEY")
}
jwt_user = JWTManager(itinerary_blueprint)


@itinerary_blueprint.route('/getone', methods=['GET'])
def get_itinerary():
    """
Get Itinerary
---
tags:
  - Itinerary
parameters:
  - name: itinerary_id
    in: query
    type: integer
    required: true
    description: ID of the itinerary
responses:
  200:
    description: Successful response with itinerary data
    schema:
      type: object
      properties:
        id:
          type: integer
        author:
          type: string
        city:
          type: string
        country:
          type: string
        duration:
          type: integer
        description:
          type: string
        period:
          type: string
        budget:
          type: number
          format: float
        currency:
          type: string
        tags:
          type: array
          items:
            type: string
        pictures:
          type: array
          items:
            type: string
        days:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              description:
                type: string
              budget:
                type: number
                format: float
              activities:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    title:
                      type: string
                    start_time:
                      type: string
                    end_time:
                      type: string
                    location:
                      type: string
                    cost:
                      type: number
                      format: float
                    notes:
                      type: string
    examples:
      application/json:
        id: 16
        author: Pepe
        city: Barcelona
        country: Catalunya
        duration: 2
        description: Cosascosascosas
        period: summer
        budget: 2264.0
        currency: EUR
        tags:
          - tag1
          - tag2
          - tag3
        pictures:
          - pic1
          - pic2
        days:
          - id: 0
            description: mascosas
            budget: 2092.0
            activities:
              - id: 0
                title: Puente muy bonito
                start_time: 10:15
                end_time: 11:30
                location: Calle de la Paz, 3
                cost: 15.0
                notes: ''
              - id: 0
                title: Casa muy bonita
                start_time: 11:45
                end_time: 13:00
                location: Calle de la Paz, 4
                cost: 2000.0
                notes: ''
              - id: 0
                title: Restaurante muy bueno
                start_time: 13:15
                end_time: 15:30
                location: Calle de la Paz, 5
                cost: 77.0
                notes: 'Pedir el menú del día'
          - id: 0
            description: mascosas
            budget: 172.0
            activities:
              - id: 0
                title: Puente muy bonito2
                start_time: 10:15
                end_time: 11:30
                location: Calle de la Paz, 32
                cost: 152.0
                notes: ''
              - id: 0
                title: Casa muy bonita2
                start_time: 11:45
                end_time: 13:00
                location: Calle de la Paz, 42
                cost: 20.0
                notes: ''
  400:
    description: Invalid request or error occurred
    schema:
      oneOf:
        - type: object
          properties:
            error:
              type: integer
              example: 111
            description:
              type: string
              example: Fatal error when scanning itineraries for the specified id
        - type: object
          properties:
            error:
              type: integer
              example: 112
            description:
              type: string
              example: Specified tinerary does not exist
"""

    try:
        itinerary_id = int(request.args.get("itinerary_id"))

        itinerary_data = DalIt.GetItinerary(itinerary_id)
        if itinerary_data is None:
            return {"error": 112, "message": "Specified itinerary does not exist"}, 400

        days_data = DalDay.GetDays(itinerary_id)

        days = []

        for day in days_data:
            activities = []
            activities_data = (DalAct.GetActivities(day["id"]))

            for activity in activities_data:
                activities.append(Activity(activity["title"], activity["start_time"], activity["end_time"], activity["location"], float(
                    activity["cost"]), activity["notes"]))

            days.append(Day(day["description"], activities))

        itinerary = Itinerary(itinerary_data["author"], itinerary_data["city"], itinerary_data["country"], itinerary_data["description"],
                              itinerary_data["period"], itinerary_data["currency"], itinerary_data["tags"], itinerary_data["pictures"], days)
        itinerary.id = itinerary_id
        json_data = json.dumps(
            itinerary, default=lambda o: o.__json__(), indent=4, ensure_ascii=False)

        return json_data, 200

    except Exception as e:
        print(e)
        return {"error": 111}, 400


@itinerary_blueprint.route('/getall', methods=['GET'])
def get_itineraries():
    """
Get All Itineraries
---
tags:
  - Itinerary
parameters:
  - name: cities
    in: query
    type: array
    collectionFormat: multi
    items:
      type: string
    description: List of cities
  - name: max_duration
    in: query
    type: integer
    description: Maximum duration in days
  - name: periods
    in: query
    type: array
    collectionFormat: multi
    items:
      type: string
    description: List of periods
  - name: max_budget
    in: query
    type: number
    format: float
    description: Maximum budget
  - name: tags
    in: query
    type: array
    collectionFormat: multi
    items:
      type: string
    description: List of tags
responses:
  200:
    description: Successful response
    schema:
      type: array
      items:
        type: object
        properties:
          city:
            type: string
          duration:
            type: integer
          id:
            type: integer
    examples:
      application/json:
        [
          {"city": "Barcelona", "duration": 2, "id": 16},
          {"city": "Paris", "duration": 5, "id": 85}
        ]
  400:
    description: Invalid request or error occurred
"""
    filters = {
        'cities': request.args.getlist('cities'),
        'max_duration': request.args.get('max_duration'),
        'periods': request.args.getlist('periods'),
        'max_budget': request.args.get('max_budget'),
        'tags': request.args.getlist('tags')
    }
    try:
        result = DalIt.GetItineraries(filters)
        return jsonify(result), 200

    except Exception:
        return {"error": 113}, 400


@itinerary_blueprint.route('/create', methods=['POST', 'OPTIONS'])
def create_itinerary():
    """
Create Itinerary
---
tags:
  - Itinerary
parameters:
  - in: body
    name: body
    description: Itinerary object that needs to be created
    required: true
    schema:
      type: object
      properties:
        author:
          type: string
        city:
          type: string
        country:
          type: string
        description:
          type: string
        period:
          type: string
        currency:
          type: string
        tags:
          type: array
          items:
            type: string
        pictures:
          type: array
          items:
            type: string
        days:
          type: object
          additionalProperties:
            type: object
            properties:
              description:
                type: string
              activities:
                type: object
                additionalProperties:
                  type: object
                  properties:
                    title:
                      type: string
                    start_time:
                      type: string
                    end_time:
                      type: string
                    location:
                      type: string
                    cost:
                      type: number
                      format: float
                    notes:
                      type: string

responses:
  201:
    description: Itinerary created successfully
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

    try:
        input_data = request.json

        days = []

        for day_key, day_value in input_data["days"].items():
            activities = []

            for activity_key, activity_value in day_value["activities"].items():
                activity = activity_value
                start_time = dt.datetime.strptime(activity["start_time"], "%H:%M").time()
                end_time = dt.datetime.strptime(activity["end_time"], "%H:%M").time()
                activities.append(Activity(activity["title"], start_time, end_time, activity["location"], activity["cost"], activity["notes"]))

            day = Day(day_value["description"], activities)
            days.append(day)

        itinerary = Itinerary(input_data["author"], input_data["city"], input_data["country"], input_data["description"], input_data["period"], input_data["currency"], input_data["tags"], input_data["pictures"], days)

        x = DalIt.AddItinerary(itinerary)

        return jsonify({'message': f"Itinerary {x} created successfully"}), 201
    except Exception as e:
        print(e)
        return jsonify({'error': 110}), 400



@itinerary_blueprint.route('/update', methods=['PUT'])
@jwt_required()
def update_itinerary(itinerary_id):
    # Implement the logic to update an itinerary here
    return jsonify({'message': f'User {itinerary_id} updated successfully'}), 200


@itinerary_blueprint.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_itinerary(itinerary_id):
    """
Delete Itinerary
---
tags:
  - Itinerary
parameters:
  - name: itinerary_id
    in: path
    type: integer
    required: true
    description: ID of the itinerary to delete
responses:
  200:
    description: Itinerary deleted successfully
    schema:
      type: object
      properties:
        message:
          type: string
    examples:
      application/json:
        {
          "message": "Itinerary {itinerary_id} deleted successfully"
        }
  401:
    description: Unauthorized - Invalid or missing authentication token
  404:
    description: Itinerary not found
  500:
    description: Internal server error occurred
"""

    # Implement the logic to delete a user here
    return jsonify({'message': f'Itinerary {itinerary_id} deleted successfully'}), 200
