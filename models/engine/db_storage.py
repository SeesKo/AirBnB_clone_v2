#!/usr/bin/python3
""" Module for New engine DBStorage """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """Handles storage for SQLAlchemy ORM"""
    __engine = None
    __session = None

    def __init__(self):
        """Create engine and link to MySQL database"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, pwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects of a particular class"""
        classes = [User, State, City, Place, Review, Amenity]

        obj_dict = {}
        session = self.__session()

        if cls:
            objs = session.query(cls).all()
        else:
            objs = []
            for c in classes:
                objs += session.query(c).all()

        for obj in objs:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            obj_dict[key] = obj

        session.close()
        return obj_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def delete(self, obj=None):
        """Delete the object from the database session"""
        if obj:
            self.__session.delete(obj)

    def save(self):
        """Commit all changes to the database"""
        self.__session.commit()

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                 expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """Close the session"""
        self.__session.remove()
