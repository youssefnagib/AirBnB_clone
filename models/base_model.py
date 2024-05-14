#!/usr/bin/python3

from uuid import uuid4
from datetime import datetime
import models

class BaseModel:

    def __init__(self, *args, **kwarg):
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
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"


    def save(self):
        self.updated_at = datetime.now()
        models.storage.save()
    
    def to_dict(self):
        dict = self.__dict__.copy()
        dict["created_at"] = self.created_at.isoformat()
        dict["updated_at"] = self.updated_at.isoformat()
        dict["__class__"] = self.__class__.__name__
        return dict
    
