#!/usr/bin/python3

"""
Define SubClass of BaseModel called amenity
"""
from models.base_model import BaseModel


class Amenity(BaseModel):

    """A class that represents a amenity

    Attributes:
        name(str): amenity name

    """
    name = ""
