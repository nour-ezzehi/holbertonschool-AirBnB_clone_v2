#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import models

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, val in kwargs.items():
                if key in ("created_at", "updated_at"):
                    val = datetime.strptime(kwargs['updated_at'],
                                            '%Y-%m-%dT%H:%M:%S.%f')
                if "__class__" not in key:
                    setattr(self, key, val)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        '''Return dictionary representation of instance.'''
        dictionary = self.__dict__.copy()
        if "created_at" in dictionary and isinstance(
                dictionary["created_at"], datetime):
            dictionary["created_at"] = dictionary["created_at"].isoformat()
        if "updated_at" in dictionary and isinstance(
                dictionary["updated_at"], datetime):
            dictionary["updated_at"] = dictionary["updated_at"].isoformat()
        dictionary["__class__"] = self.__class__.__name__
        if '_sa_instance_state' in dictionary:
            del (dictionary['_sa_instance_state'])
        return dictionary

    def delete(self):
        """Deletes the current instance from the models.storage"""
        models.storage.delete(self)
