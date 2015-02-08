__author__ = 'tang'

from conf import DB_HOST, DB_PASSWORD, DB_USERNAME, DB_PORT
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime
from dateutil.relativedelta import relativedelta
from uuid import uuid1

engine = create_engine("mysql://%s:%s@%s:%s/myinstagram" % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT),
                       echo=True)
db = sessionmaker(engine)()

Base = declarative_base()


class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime)
    last_id = Column(Integer)
    session = Column(String(72))
    data = Column(LONGTEXT)


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(String(72), primary_key=True)
    photo_id = Column(Integer, ForeignKey('photos.id'))
    expire_time = Column(DateTime)
    photo = relationship("Photo", uselist=False)


def set_session():
    session_id = uuid1()
    session = Session(id=session_id, expire_time=datetime.now() + relativedelta(months=+3))
    db.add(session)
    db.commit()
    return session_id


def upload_photo(data, session_id):
    session = db.query(Session).get(session_id)
    if session.photo:
        new_photo = Photo(id=None, create_time=datetime.now(), last_id=session.photo.id, session=session_id, data=data)
    else:
        new_photo = Photo(id=None, create_time=datetime.now(), last_id=None, session=session_id, data=data)
    db.add(new_photo)
    db.commit()
    session.photo_id = new_photo.id
    db.commit()


def get_photos(session_id):
    if session_id:
        session = db.query(Session).get(session_id)
        return session.photo
    else:
        count = 0
        photos = db.query(Photo).filter(Photo.session == None).order_by(Photo.create_time.desc())
        print photos
        for photo in photos:
            count += 1
        return photos


def pop_photo(session_id):
    session = db.query(Session).get(session_id)
    cur_photo = session.photo
    last_photo = db.query(Session).get(cur_photo.last_id)
    session.photo_id = last_photo.id
    db.delete(cur_photo)
    db.commit()


def commit_photo(session_id):
    session = db.query(Session).get(session_id)
    cur_photo = session.photo
    cur_photo.create_time = datetime.now()
    cur_photo.session = None
    cur_photo.last_id = None
    db.commit()
    db.query(Photo).filter(Photo.session == session_id).delete()
    db.delete(session)


def get_page(page):
    num = db.query(func.count(Photo.id)).scalar()
    rv = []
    #photos = db.query(Photo.data).filter(Photo.session == None).order_by(Photo.create_time.desc())
    #for photo in photos:
    #    rv.append(photo.data)
    #return rv
    return num


def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)