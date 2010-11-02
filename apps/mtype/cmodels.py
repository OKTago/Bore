from django.db import models

"""
In this file you can define a custom model that will be auto imported
from meta manager class. Manger will create the needed tables also.
I put they here and not in models.py to prevent syncdb from build tables.
Nothing is wrong with syncdb but I want MetaMan to have centralized 
control of types
"""

# Sample model
#
#class Post(models.Model):
#    title = models.CharField(max_length=255)
#    text = models.TextField()
