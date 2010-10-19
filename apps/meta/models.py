from django.db import models

from django.db import connection
from django.db.utils import DatabaseError

Person = type('Person', (models.Model,), {
    '__module__': 'meta.models',
    'name': models.CharField(max_length=255),
})

# TODO: cerca un modo per fare il syncdb in automatico
