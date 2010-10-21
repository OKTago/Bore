import django.db.models.fields
from django.db.models.fields import *
from inspect import getmembers, isclass

class Fields:
    # private static
    __fields = {} 
    __fields_set = []
    
    def __init__(self):
        if len(self.__fields) == 0:
            self.__discover()

    def get_all(self):
        return self.__fields

    def get_set(self):
        return self.__fields_set

    def get_class_by_name(self, name):
        return self.__fields[name]
        
    def __discover(self):
        """
        builds a dictionary of all defined fields 
        """
        classes = getmembers(django.db.models.fields, isclass)
        for cls in classes:
            name = cls[0]
            obj = cls[1]
            if issubclass(obj, Field):
                self.__fields[name] = obj
                self.__fields_set.append((name, name))
