__author__ = 'tang'

import MySQLdb
from conf import DB_HOST, DB_PASSWORD, DB_USERNAME, DB_PORT
from datetime import datetime
from dateutil.relativedelta import relativedelta
from uuid import uuid1


con = MySQLdb.connect(user=DB_USERNAME, passwd=DB_PASSWORD, host=DB_HOST, port=int(DB_PORT), db="myinstagram")
cur = con.cursor()
cur.connection.autocommit(True)

def drop_all():
    cur.execute("DROP TABLE IF EXISTS photos")
    cur.execute("DROP TABLE IF EXISTS sessions")


def create_all():
    photos = '''
    CREATE TABLE photos
    (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    create_time DATETIME,
    last_id INT,
    session VARCHAR(72),
    data LONGTEXT
    );'''
    sessions = '''
    CREATE TABLE sessions
    (
    id VARCHAR(72) PRIMARY KEY,
    photo_id INTEGER,
    expire_time DATETIME
    );
    '''
    cur.execute(photos)
    cur.execute(sessions)


def init_db():
    drop_all()
    create_all()


def set_session():
    session_id = uuid1()

    command = "INSERT INTO sessions (id, expire_time) VALUES ('%s', '%s');" % (session_id, (datetime.now() + relativedelta(months=+1)).strftime('%Y-%m-%d %H:%M:%S'))
    rv = cur.execute(command)

    return session_id


def verify_session(session_id):
    cur.execute("SELECT * FROM sessions WHERE id='%s'" % session_id)
    session = cur.fetchone()
    if not session:
        session_id = set_session()
    else:
        session_id = session[0]
    return session_id


def reset_session(session_id):
    cur.execute("DELETE FROM photos WHERE session='%s'" % session_id)
    cur.execute("UPDATE sessions SET photo_id=NULL WHERE id='%s'" % session_id)


def upload_photo(data, session_id):
    cur.execute("SELECT photo_id FROM sessions WHERE id='%s'" % session_id)
    last_id = cur.fetchone()[0]
    if last_id is None:
        last_id = 'NULL'
    command = "INSERT INTO photos (create_time, last_id, session, data) VALUES ('%s', %s, '%s', '%s')" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), last_id, session_id, data)
    cur.execute(command)
    photo_id = cur.lastrowid
    cur.execute("UPDATE sessions SET photo_id=%d WHERE id='%s'" % (photo_id, session_id))


def get_photo(session_id):
    cur.execute("SELECT photo_id FROM sessions WHERE id='%s'" % session_id)
    photo_id = cur.fetchone()[0]
    if not photo_id:
        return None
    cur.execute("SELECT data FROM photos WHERE id=%d" % photo_id)
    photo = cur.fetchone()[0]
    return photo


def last_photo(session_id):
    cur.execute("SELECT COUNT(id) FROM photos WHERE session='%s'" % session_id)
    num = cur.fetchone()[0]
    if num == 1:
        return True
    else:
        return False


def pop_photo(session_id):
    cur.execute("SELECT photo_id FROM sessions WHERE id='%s'" % session_id)
    photo_id = cur.fetchone()[0]
    cur.execute("SELECT last_id FROM photos WHERE id=%d" % photo_id)
    last_id = cur.fetchone()[0]
    if last_id is None:
        return False
    cur.execute("DELETE FROM photos WHERE id=%d" % photo_id)
    cur.execute("UPDATE sessions SET photo_id=%d WHERE id='%s'" % (last_id, session_id))
    return True




def commit_photo(session_id):
    cur.execute("SELECT photo_id FROM sessions WHERE id='%s'" % session_id)
    photo_id = cur.fetchone()[0]
    cur.execute("UPDATE photos SET create_time='%s', session=NULL, last_id=NULL WHERE id=%d" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), photo_id))
    cur.execute("DELETE FROM photos WHERE session='%s'" % session_id)


def get_page(page):
    cur.execute("SELECT COUNT(id) FROM photos WHERE session IS NULL")
    num = cur.fetchone()[0]
    start = (page - 1) * 8
    if (page - 1) * 8 >= num:
        return [], num
    rv = []
    cur.execute("SELECT data FROM photos WHERE session IS NULL ORDER BY create_time DESC LIMIT 8 OFFSET %d" % start)
    photos = cur.fetchall()
    for photo in photos:
        rv.append(photo[0])
    return rv, num
