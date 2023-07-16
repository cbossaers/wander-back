import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

from ..classes.class_user import User


class DalUser:
    load_dotenv()

    conndata: str = os.environ.get("CONN_STRING")

    @staticmethod
    def GetUser(email: str):
        with psycopg.connect(DalUser.conndata, row_factory=dict_row) as conn:
            with conn.cursor() as cur:

                sql = "SELECT name, email, picture FROM public.user WHERE email = %s"

                data = (email,)

                try:
                    cur.execute(sql, data)
                    user_data = cur.fetchone()
                    return user_data

                except Exception as error:
                    raise error

    @staticmethod
    def GetPassword(email: str):
        with psycopg.connect(DalUser.conndata, row_factory=dict_row) as conn:
            with conn.cursor() as cur:

                sql = "SELECT password FROM public.user WHERE email = %s"

                data = (email,)

                try:
                    cur.execute(sql, data)

                    return cur.fetchone()

                except Exception as error:
                    raise error

    @staticmethod
    def AddUser(user: User):
        with psycopg.connect(DalUser.conndata, row_factory=dict_row) as conn:
            with conn.cursor() as cur:

                sql = "INSERT INTO public.user " \
                      "(name, email, password, picture)" \
                      "VALUES (%s,%s,%s,%s)"

                data = (user.name, user.email, user.password, user.picture)

                try:
                    cur.execute(sql, data)
                    conn.commit()

                except Exception as error:
                    raise error
