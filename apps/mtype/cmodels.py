from django.db import models

"""
In this file you can define a custom model that will be auto imported
from meta manager class. Manger will create the needed tables also.
I put they here and not in models.py to prevent syncdb from build tables.
Nothing is wrong with syncdb but I want MetaMan to have centralized 
control of types
"""

# Create your models here.

class Documento(models.Model):
    titolo = models.CharField(max_length=255)
    testo = models.TextField()

    class Meta:
        verbose_name_plural = "Documenti"
