#!/usr/bin/python3
""" Module for New engine DBStorage """
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        session = self.__session
        objects = {}
        if cls:
            query = session.query(cls.__table__)
            for obj in query:
                key = "{}.{}".format(cls.__name__, obj.id)
                objects[key] = obj
        else:
            for c in [User, State, City, Amenity, Place, Review]:
                query = session.query(c.__table__)
                for obj in query:
                    key = "{}.{}".format(c.__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Adds the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and creates a new session"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """ Calls remove() method on the private session attribute """
        self.__session.remove()
