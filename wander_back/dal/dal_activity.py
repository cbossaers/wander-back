import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
from typing import List

from ..classes.class_activity import Activity


class DalActivity:
    load_dotenv()

    conndata: str = os.environ.get("CONN_STRING")

    @staticmethod
    def GetActivities(day_id):
        with psycopg.connect(DalActivity.conndata, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                sql = """
                    SELECT *
                    FROM public.activity
                    WHERE day_id = %s
                """

                data = (day_id, )

                try:
                    cur.execute(sql, data)
                    return cur.fetchall()

                except Exception as error:
                    raise error

    @staticmethod
    def AddActivities(day: int, activities: List[Activity]):
        with psycopg.connect(DalActivity.conndata, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                sql = "INSERT INTO public.activity " \
                      "(day_id, title, start_time, end_time, location, cost, notes) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s)"

                try:
                    for activity in activities:
                        data = (day, activity.title, activity.start_time, activity.end_time, activity.location, activity.cost, activity.notes)

                        cur.execute(sql, data)
                        conn.commit()

                except Exception as error:
                        raise error
