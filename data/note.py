import _sqlite3

conn = _sqlite3.connect('data/note.db')

c = conn.cursor()

def create_table(_id):
    c.execute("""CREATE TABLE IF NOT EXISTS {} (
                key blob,
                value blob
                )""".format(_id))


def insert_note(_id, key, value):
    with conn:
        c.execute("INSERT INTO {} VALUES (?, ?)".format(_id), (key, value))


def get_note_all(_id):
    return c.execute("SELECT * FROM {}".format(_id))


def get_note(_id, key):
    c.execute("SELECT * FROM {} WHERE key=?".format(_id), (key,))
    return c.fetchall()


def change_note(_id, key, value):
    with conn:
        c.execute("""UPDATE {} SET value = :value
                    WHERE key = :key""".format(_id),
                  {'key': key, 'value': value})


def remove_note(_id, key):
    with conn:
        c.execute("DELETE from {} WHERE key = :key".format(_id),
                  {'key': key})


def check_table(_id, key):
    return c.execute("SELECT EXISTS(SELECT * FROM {} WHERE key=?)".format(_id), (key,)).fetchone()