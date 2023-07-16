import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

from ..classes.class_itinerary import Itinerary
from ..dal.dal_day import DalDay


class DalItinerary:
    load_dotenv()

    conndata: str = os.environ.get("CONN_STRING")

    @staticmethod
    def GetItinerary(itinerary_id: int):
        with psycopg.connect(DalItinerary.conndata, row_factory=dict_row) as conn:
            with conn.cursor() as cur:

                sql = "SELECT * FROM public.itinerary WHERE id = %s"

                data = (itinerary_id, )

                try:
                    cur.execute(sql, data)
                    itinerary_data = cur.fetchone()
                    return itinerary_data

                except Exception as error:
                    raise error

    @staticmethod
    def GetItineraries(filters):
        with psycopg.connect(DalItinerary.conndata, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                sql = """
                    SELECT id, city, duration
                    FROM public.itinerary
                    WHERE city = ANY(%(cities)s)
                        AND duration <= %(max_duration)s
                        AND period = ANY(%(periods)s)
                        AND budget <= %(max_budget)s
                        AND tags && %(tags)s
                """

                try:
                    cur.execute(sql, filters)
                    return cur.fetchall()

                except Exception as error:
                    raise error

    @staticmethod
    def AddItinerary(itinerary: Itinerary):
        with psycopg.connect(DalItinerary.conndata, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                sql = "INSERT INTO public.itinerary " \
                      "(author, city, country, duration, description, period, budget, currency, tags, pictures)" \
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"

                data = (
                    itinerary.author,
                    itinerary.city,
                    itinerary.country,
                    itinerary.duration,
                    itinerary.description,
                    itinerary.period,
                    itinerary.budget,
                    itinerary.currency,
                    itinerary.tags,
                    itinerary.pictures
                )

                try:
                    cur.execute(sql, data)
                    inserted_id = cur.fetchone()["id"]
                    conn.commit()
                    
                    DalDay.AddDays(inserted_id, itinerary.days)

                    return inserted_id

                except Exception as error:
                    raise error
