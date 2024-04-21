#!/usr/bin/python3
""" Module for New engine DBStorage """
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from os import getenv


class DBStorage:
    """ DBStorage class """
    __engine = None
    __session = None

    def __init__(self):
        """ Initializes DBStorage """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns all instances from specified or default classes
        in a dictionary keyed by class name and ID
        """
        if cls is None:
            results = self.__session.query(State).all()
            results.extend(self.__session.query(City).all())
            results.extend(self.__session.query(User).all())
            results.extend(self.__session.query(Place).all())
            results.extend(self.__session.query(Review).all())
            results.extend(self.__session.query(Amenity).all())
        else:
            if isinstance(cls, str):
                cls = eval(cls)
            results = self.__session.query(cls).all()

        return {
            "{}.{}".format(type(obj).__name__, obj.id): obj
            for obj in results
        }

    def new(self, obj):
        """ Adds the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commits all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes from the current database session """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Creates all tables in the database and creates a new session """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ Close the session """
        self.__session.close()
