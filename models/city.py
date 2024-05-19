#!/usr/bin/python3
"""
Define SubClass of BaseModel called City
"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    Class City
    Public class attributes:
        state_id: (str) state id
        name:     (str) name
    """
    state_id = ""
    name = ""
