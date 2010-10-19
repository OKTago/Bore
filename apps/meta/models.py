from django.db import models

from django.db import connection
from django.db.utils import DatabaseError

from django.contrib import admin

def person_unicode(self): return self.name
Person = type('Person', (models.Model,), {
    '__module__': 'meta.models', # deve corrispondere al path di import per questo file 
    'name': models.CharField(max_length=255),
    '__unicode__': person_unicode,
})

admin.site.register(Person)

# TODO: cerca un modo per fare il syncdb in automatico
#       Vedi django/core/management/commands/syncdb.py
