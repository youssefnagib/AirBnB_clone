#!/usr/bin/python3

"""
Contains the FileStorage Class
"""
import json


class FileStorage:
    """serializes instances to a JSON file"""
    """and deserializes JSON file to instances"""

    # string - path to the JSON file
    __file_path = "file.json"

    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""

        return (self.__objects)

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file"""
        ser_obj = {}
        for key, value in self.__objects.items():
            ser_obj[key] = value.to_dict()
        with open(self.__file_path, "w") as D:
            json.dump(ser_obj, D)

    def reload(self):
        """Deserializes the JSON file to __objects if the file exist"""
        try:
            with open(self.__file_path, 'r') as D:
                deser_obj = json.load(D)
                for key, value in deser_obj.items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass
