__author__ = 'tang'

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from datetime import datetime
from dateutil.relativedelta import relativedelta
from uuid import uuid1

engine = create_engine("mysql://adminUbw65Jz:aMlEyugQkjaa@localhost/myinstagram", echo=True)
db = sessionmaker(engine)()

Base = declarative_base()
class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime)
    last_id = Column(Integer)
    session = Column(String(32))
    data = Column(Text)


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(String(32), primary_key=True)
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
    new_photo = Photo(None, datetime.now(), session.photo.id, session_id, data)
    db.add(new_photo)
    session.photo_id = new_photo.id
    db.commit()


def get_photos(session_id):
    session = db.query(Session).get(session_id)
    return session.photo


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
    db.query(Photo).filter(session == session_id).delete()
    db.delete(session)


def get_page(page):
    total = db.query(func.count(Photo.id))
    if total <= page * 8:
        return None
    else:
        photos = db.query(Photo.data).order(Photo.create_time.desc()).limit(8).offset(page * 8)
        return photos


def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)