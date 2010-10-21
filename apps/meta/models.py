from django.db import models

from django.db import connection
from django.db.utils import DatabaseError

from django.contrib import admin

from meta.lib.builder import *

class MetaMan:
    __metaClasses = {}

    def addModel(self, cls):
        objName = cls._meta.object_name 
        self.__metaClasses[objName] = cls

    def removeModel(self, cls):
        pass

    def buildObject(self, typeName):
        """
        Return an instance of type name
        Usage example:
            o = metaMan.buildObject('Type1')
            o.name = "test name"
            o.save()
        """
        cls = self.__metaClasses[typeName]
        obj = cls()
        return obj

    def getClass(self, typeName):
        """
        Return the type class.
        Usage example:
            t = metaMan.getClass('Type1')
            t.objects.all()
        """
        return self.__metaClasses[typeName]

metaMan = MetaMan()


class MetaType(models.Model):
    name = models.CharField(max_length=255)
    final = models.BooleanField()
    abstract = models.BooleanField()

    def __unicode__(self):
        return self.name
admin.site.register(MetaType)

class TypeField(models.Model):
    name = models.CharField(max_length=255)
    metaType = models.ForeignKey(MetaType)
    # TODO: manca un riferimento al tipo del campo (CharField, BooleanField etc)
    #       Il tipo di campo va inserito in una tabella a parte e poi fatto un switch case sul risultato
    #       Esempio:
    #           basic_types
    #            ---------------
    #           id    |   name
    #           1     |   String
    #           2     |   Boolean
    #
    #           switch(type):
    #               case String: return models.CharField()
admin.site.register(TypeField)


Object = type('Person', (models.Model,), {
    '__module__': 'meta.models', # deve corrispondere al path di import per questo file 
    'name': models.CharField(max_length=255),
    '__unicode__': lambda self: eval("self."+"name"),
})

admin.site.register(Object)

Tag = type('Tag', (models.Model,), {
    '__module__': 'meta.models', # deve corrispondere al path di import per questo file 
    'name': models.CharField(max_length=255),
    '__unicode__': lambda self: eval("self."+"name"),
})

Document = type('Document', (models.Model,), {
    '__module__': 'meta.models', # deve corrispondere al path di import per questo file 
    'title': models.CharField(max_length=255),
    'tags': models.ManyToManyField(Tag),
    '__unicode__': lambda self: eval("self."+"title"),
})

for i in range(3):
    base = type('Type'+str(i), (models.Model,), {
        '__module__': 'meta.models',
        'name': models.CharField(max_length=255),
        '__unicode__': lambda self: eval("self."+"name"),
    })
    metaMan.addModel(base)
    admin.site.register(base)

# eredita da Type0
obj = type('TypeExt', (metaMan.getClass('Type0'),), {
    '__module__': 'meta.models',
    'nameExt': models.CharField(max_length=255),
    '__unicode__': lambda self: eval("self."+"name"),
})
admin.site.register(obj)

sync_meta_models()


# TODO: verificare se esiste una sorta di elenco di models.Fields
#       in modo che nell'interfaccia di definizione del tipo
#       si possa usare un drop-down con l'elenco
