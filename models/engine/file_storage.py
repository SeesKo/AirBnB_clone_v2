#!/usr/bin/python3
""" FileStorage Module """
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """
    Serializes instances to a JSON file and deserializes
    JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """ Returns a dictionary of all objects """
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            class_dict = {}
            for k, v in self.__objects.items():
                if type(v) == cls:
                    class_dict[k] = v

            return class_dict

        return self.__objects

    def new(self, obj):
        """ Sets in __objects the obj with key <obj class name>.id """
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """ Serializes __objects to the JSON file """
        object_data = {obj_key: self.__objects[obj_key].to_dict() for obj_key in self.__objects.keys()}
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(object_data, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                for obj_data in json.load(f).values():
                    class_name = obj_data["__class__"]
                    del obj_data["__class__"]
                    self.new(eval(class_name)(**obj_data))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ Deletes obj from __objects if it's inside """
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """ Calls reload() method to deserialize JSON file to objects """
        self.reload()
