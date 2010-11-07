from django.db import models
from django.contrib import admin
"""
In this file you can define a custom model that will be auto imported
from meta manager class. Manger will create the needed tables also.
"""

class BaseType(models.Model):
    class Meta:
        abstract = True
        app_label = "MType"
 

# Sample custom model

#class Doc(BaseType):
#    title = models.CharField(max_length=255)
#    text = models.TextField()
#    
#    def __unicode__(self):
#        return self.title
#admin.site.register(Doc)
