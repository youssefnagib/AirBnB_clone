#!/usr/bin/python3

from uuid import uuid4
from datetime import datetime
import models

"""
A Base Class of all Classes in this Project
"""


class BaseModel:

    """ BaseModel Definition
    Methods:
        __init__(self, *args, **kwargs)
        __str__(self)
        __save(self)
        __repr__(self)
        to_dict(self)
    """
    def __init__(self, *args, **kwarg):
        """
        Initialize attributes: uuid4, dates when class was created/updated
        """
        DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
        if kwarg:
            for key, value in kwarg.items():
                if key in ("updated_at", "created_at"):
                    setattr(self, key, datetime.strptime(value, DATE_FORMAT))
                elif key[0] == "id":
                    setattr(self, key, str(value))
                elif key == "__class__":
                    pass
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self) -> str:
        """
        Returns string representation of the class
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        updates the public instance attribute:
        updated_at: with the current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all
        keys/values the instance __dict__
        """
        dict = self.__dict__.copy()
        dict["created_at"] = self.created_at.isoformat()
        dict["updated_at"] = self.updated_at.isoformat()
        dict["__class__"] = self.__class__.__name__
        return dict
