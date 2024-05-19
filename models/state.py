#!/usr/bin/python3

"""
Define SubClass of a BaseModel called State
"""

from models.base_model import BaseModel


class State(BaseModel):

    """A class State

    Attribute:
        name (str): the name of the state
    """

    name = ""
