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

    def get_available_properties(self):
        """
        verbose_name=None, name=None, primary_key=False,
                max_length=None, unique=False, blank=False, null=False,
                db_index=False, rel=None, default=NOT_PROVIDED, editable=True,
                serialize=True, unique_for_date=None, unique_for_month=None,
                unique_for_year=None, choices=None, help_text='', db_column=None,
                db_tablespace=None, auto_created=False, validators=[],
                error_messages=None
        """

        ret = [
            ("verbose_name", "verbose_name"),
            ("max_length", "max_length"),
            ("max_digits", "max_digits"),
            ("decimal_places", "decimal_places"),
        ]
        return ret
    
    @staticmethod
    def get_properties_assoc(field):
        ret = {}
        objects = field.property_set.all()
        for obj in objects:
            ret[obj.name] = obj.value
        return ret
        
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
