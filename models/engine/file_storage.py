#!/usr/bin/python3
""" FileStorage Module """
import json
from models.base_model import BaseModel


class FileStorage:
    """ Serializes instances to a JSON file and deserializes JSON file to instances """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """ Returns a dictionary of all objects """
        if cls:
            cls_name = cls.__name__
            return {k: v for k, v in self.__objects.items() if type(v) == cls}
        return self.__objects

    def new(self, obj):
        """ Sets in __objects the obj with key <obj class name>.id """
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        """ Serializes __objects to the JSON file """
        with open(self.__file_path, mode='w', encoding='utf-8') as file:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, file)

    def reload(self):
        """ Deserializes the JSON file to __objects """
        try:
            with open(self.__file_path, mode='r', encoding='utf-8') as file:
                self.__objects = {k: BaseModel(**v) for k, v in json.load(file).items()}
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ Deletes obj from __objects if it's inside """
        if obj:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects.pop(key, None)
