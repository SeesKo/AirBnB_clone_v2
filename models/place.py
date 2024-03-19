#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import relationship
from os import getenv


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            back_populates='place_amenities',
            viewonly=False
            )
        reviews = relationship(
            'Review',
            backref='place',
            cascade='all, delete-orphan'
        )
    else:
        """ A place to stay """
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Getter attribute for reviews"""
            from models import storage
            all_reviews = storage.all(Review)
            place_reviews = []
            for review in all_reviews.values():
                if review.place_id == self.id:
                    place_reviews.append(review)
            return place_reviews

        # Getter attribute amenities for FileStorage
        @property
        def amenities(self):
            """Getter attribute for amenities"""
            from models import storage
            amenity_list = []
            for amenity_id in self.amenity_ids:
                amenity = storage.get('Amenity', amenity_id)
                if amenity:
                    amenity_list.append(amenity)
            return amenity_list

        # Setter attribute amenities for FileStorage
        @amenities.setter
        def amenities(self, obj):
            """Setter attribute for amenities"""
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
