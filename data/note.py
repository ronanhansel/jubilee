import psycopg2
import os


DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
c = conn.cursor()
conn.autocommit = True

def create_table(_id):
    c.execute("""CREATE TABLE IF NOT EXISTS {} (
                key TEXT,
                value TEXT
                )""".format(_id))


def insert_note(_id, key, value):
    with conn:
        c.execute("INSERT INTO public.{} VALUES ('{}', '{}');".format(_id, key, value))


def get_note_all(_id):
    c.execute("SELECT * FROM public.{}".format(_id))
    data = c.fetchall()
    return data


def get_note(_id, key):
    c.execute("select key, value from public.{} where key like '{}'".format(_id, key))
    return c.fetchone()


def change_note(_id, key, value):
    with conn:
        c.execute("""UPDATE public.{} SET value = {}
                    WHERE key like {}""".format(_id, value, key),
                  )


def remove_note(_id, key):
    with conn:
        c.execute("DELETE from public.{} WHERE key like '{}'".format(_id, key),)


def check_table(_id, key):
    c.execute("select exists(select key from public.{} where key like '{}')".format(_id, key))
    res = c.fetchone()
    return res


def rollback():
    conn.rollback()
def autocommit(cmd):
    conn.autocommit = cmd