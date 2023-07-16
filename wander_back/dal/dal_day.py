import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
from typing import List

from ..classes.class_day import Day
from ..dal.dal_activity import DalActivity


class DalDay:
    load_dotenv()

    conndata: str = os.environ.get("CONN_STRING")

    @staticmethod
    def GetDays(itinerary_id):
        with psycopg.connect(DalDay.conndata, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                sql = """
                    SELECT *
                    FROM public.day
                    WHERE itinerary_id = %s
                """

                data = (itinerary_id, )

                try:
                    cur.execute(sql, data)
                    return cur.fetchall()

                except Exception as error:
                    raise error

    @staticmethod
    def AddDays(itinerary: int, days: List[Day]):
        with psycopg.connect(DalDay.conndata, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                sql = "INSERT INTO public.day " \
                      "(itinerary_id, description, budget) " \
                      "VALUES (%s, %s, %s) RETURNING id"

                try:
                    for day in days:
                        data = (itinerary, day.description, day.budget)

                        cur.execute(sql, data)
                        inserted_id = cur.fetchone()["id"]
                        conn.commit()

                        DalActivity.AddActivities(inserted_id, day.activities)


                except Exception as error:
                        raise error
