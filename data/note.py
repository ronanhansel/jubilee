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
    c.execute("""create table if not exists {} (
                key TEXT,
                value TEXT
                )""".format(_id))


def insert_note(_id, key, value):
    with conn:
        c.execute("insert into public.{} values ('{}', '{}');".format(_id, key, value))


def get_note_all(_id):
    c.execute("select * from public.{}".format(_id))
    data = c.fetchall()
    return data


def get_note(_id, key):
    c.execute("select key, value from public.{} where key like '{}'".format(_id, key))
    return c.fetchone()


def change_note(_id, key, value):
    with conn:
        c.execute("""update public.{} set value='{}'
                    where key like '{}'""".format(_id, value, key),
                  )


def remove_note(_id, key):
    with conn:
        c.execute("delete from public.{} where key like '{}'".format(_id, key),)


def check_table(_id, key):
    c.execute("select exists(select key from public.{} where key like '{}')".format(_id, key))
    res = c.fetchone()
    return res


def rollback():
    conn.rollback()
def autocommit(cmd):
    conn.autocommit = cmd