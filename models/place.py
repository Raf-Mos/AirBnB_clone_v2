#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
import models


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    amenitites = relationship(
            "Amenity", secondary='place_amenity',
            back_populates="place_amenities", viewonly=False)
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", cascade="delete", backref="place")

    @property
    def reviews(self):
        """ Returns list of reviews.id """
        dict_reviews = models.storage.all(models.Review)
        list_reviews = []
        for i in dict_reviews.values():
            if i.place_id == self.id:
                list_reviews.append(i)
            return i

        @property
        def amenities(self):
            """ Returns list of amenity ids """
            list_obj = []
            amen_objs = models.storage.all('Amenity')
            for i in amen_objs.values():
                if amenity.id in amenity_ids:
                    list_obj.append(amenity)
                return list_obj

        @amenities.setter
        def amenities(self, obj=None):
            """ Appends amenity ids to the attribute """
            if isinstance(obj, Amenity):
                if self.id == obj.place_id:
                    self.amenity_ids.append(obj.id)
