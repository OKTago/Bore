from django.db import models

from django.db import connection
from django.db.utils import DatabaseError

from django.contrib import admin

from meta.lib.manager import MetaMan
from meta.lib.fields import Fields


metaMan = MetaMan()

class MetaType(models.Model):
    name = models.CharField(max_length=255)
    final = models.BooleanField()
    abstract = models.BooleanField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "meta_METATYPE"

FIELDS = Fields().get_set() 

class TypeField(models.Model):
    name = models.CharField(max_length=255)
    metaType = models.ForeignKey(MetaType)
    field = models.CharField(max_length=50, choices=FIELDS)

    class Meta:
        db_table = "meta_TYPEFIELD"

class FieldProperty(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    typeField = models.ForeignKey(TypeField)
    class Meta:
        db_table = "meta_FIELDPROPERTY"

class TypeFieldInline(admin.TabularInline):
    model = TypeField

class MetaTypeAdmin(admin.ModelAdmin):
    inlines = [
        TypeFieldInline,
    ]
admin.site.register(MetaType, MetaTypeAdmin)


try:
    metaTypes = MetaType.objects.all()
    metaMan.buildClasses(metaTypes)
except DatabaseError:
    # this should only happen on first syncdb
    # when MetaMan table doesn't still exists
    pass

"""
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

"""

#sync_meta_models()

