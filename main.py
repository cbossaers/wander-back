from wander_back.classes.class_user import User
from wander_back.classes.class_itinerary import Itinerary
from wander_back.classes.class_day import Day
from wander_back.classes.class_activity import Activity

from wander_back.dal.dal_itinerary import DalItinerary as dalIt
from wander_back.dal.dal_day import DalDay as dalDay
from wander_back.dal.dal_activity import DalActivity as dalAct

import datetime as dt
from typing import List

from pprint import pprint
import json

def create():
    input = {
        "author": "cristian@tfg.com",
        "city": "París",
        "country": "Francia",
        "description": "Viaje en solitario para un fin de semana",
        "period": "summer",
        "currency": "EUR",
        "tags": ["solo", "finde"],
        "pictures": ["pic1", "pic2"],
        "days": {
            0: {
                "description": "Centro de la ciudad",
                "activities": {
                    0: {
                        "title": "Torre Eiffel",
                        "start_time": dt.time(10,15),
                        "end_time": dt.time(11,30),
                        "location": "Champ de Mars, 5 Av. Anatole France, 75007 Paris, France",
                        "cost": 15,
                        "notes": ""
                    },
                    1: {
                        "title": "Musée du Louvre",
                        "start_time": dt.time(11,45),
                        "end_time": dt.time(13,0),
                        "location": "75001 Paris, France",
                        "cost": 35,
                        "notes": ""
                    },
                    2: {
                        "title": "Brasserie Martin",
                        "start_time": dt.time(13,30),
                        "end_time": dt.time(15,30),
                        "location": "24 Rue Saint-Ambroise, 75011 Paris, France",
                        "cost": 77,
                        "notes": "Pedir el menú del día"
                    }
                }
            },
            1: {
                "description": "Día de callejeo",
                "activities": {
                    0: {
                        "title": "Puente muy bonito",
                        "start_time": dt.time(9,15),
                        "end_time": dt.time(11,30),
                        "location": "4 Quai d'Orléans, 75004 Paris, France",
                        "cost": 0,
                        "notes": ""
                    },
                    1: {
                        "title": "Cathédrale Notre-Dame de Paris",
                        "start_time": dt.time(11,45),
                        "end_time": dt.time(13,0),
                        "location": "6 Parvis Notre-Dame - Pl. Jean-Paul II, 75004 Paris, France",
                        "cost": 20,
                        "notes": ""
                    }
                }
            }
        }
        }
    days = []

    for day in input["days"].values():
        acts = []  # Create a new acts list for each Day object
        for activity in day["activities"].values():
            acts.append(Activity(activity["title"], activity["start_time"], activity["end_time"], activity["location"], activity["cost"], activity["notes"]))
        aux_day = Day(day["description"], acts)
        days.append(aux_day)


    it = Itinerary(input["author"], input["city"], input["country"], input["description"], input["period"], input["currency"], input["tags"], input["pictures"], days)

    dalIt.AddItinerary(it)

def retrieve(itinerary_id):

    itinerary_data = dalIt.GetItinerary(itinerary_id)
    days_data = dalDay.GetDays(itinerary_id)

    days = []

    for day in days_data:
        activities = []
        activities_data = (dalAct.GetActivities(day["id"]))
        
        for activity in activities_data:
            activities.append(Activity(activity["title"], activity["start_time"], activity["end_time"], activity["location"], float(activity["cost"]), activity["notes"]))
        
        days.append(Day(day["description"], activities))

    itinerary = Itinerary(itinerary_data["author"], itinerary_data["city"], itinerary_data["country"], itinerary_data["description"], itinerary_data["period"], itinerary_data["currency"], itinerary_data["tags"], itinerary_data["pictures"], days)
    json_data = json.dumps(itinerary, default=lambda o: o.__json__(), indent=None, ensure_ascii=False)
    pprint(json_data)


def getall():
    filters = {
        'cities': ["Tokyo", "Barcelona"],
        'max_duration': 3,
        'periods': ["summer", "winter"],
        'max_budget': 5000,
        'tags': ["tag1"]
    }

    return dalIt.GetItineraries(filters)

from wander_back.dal.dal_user import DalUser as DalUser

# user_data = DalUser.GetUser("fake@upv.es")
# print(user_data)

create()