from django.db import models
from django.contrib import admin

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

"""
In this file you can define a custom model that will be auto imported
from meta manager class. Manager will create the needed tables also.
"""

class Relation(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
admin.site.register(Relation)

class BaseType(models.Model):
#    relations = models.ManyToManyField(Relation)  
    class Meta:
        abstract = True
        app_label = "Objects"
 

# Sample custom model

#class Doc(BaseType):
#    title = models.CharField(max_length=255)
#    text = models.TextField()
#    
#    def __unicode__(self):
#        return self.title
#admin.site.register(Doc)
