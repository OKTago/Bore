from django.db import models

from django.db import connection
from django.db.utils import DatabaseError

from meta.lib.manager import MetaMan
from meta.lib.fields import Fields

metaMan = MetaMan()

class Reload(models.Model):
    """
    This model is intented to store only one tuple and
    is used by middleware to reload source code when
    new types are defined. 
    MetaType model schedule a reload overriding models.Model save
    method. The middleware execute the reload and unschedule it
    """
    is_required = models.BooleanField()

    @staticmethod
    def schedule():
        obj = Reload(id=1, is_required=True)
        obj.save()

    @staticmethod
    def unschedule():
        obj = Reload(id=1, is_required=False)
        obj.save()

    @staticmethod
    def required():
        try:
            obj = Reload.objects.get(pk=1)
        except Exception:
            Reload.unschedule()
            return False
        return obj.is_required

class MetaType(models.Model):
    name = models.CharField(max_length=255)
    name_plural = models.CharField(max_length=255) 
    final = models.BooleanField()
    abstract = models.BooleanField()
    syncready = models.BooleanField()
    # http://docs.djangoproject.com/en/dev/ref/models/fields/
    # search for ForeignKey
    extend = models.ForeignKey('self', null=True, blank=True)

    def save(self, *args, **kwargs):
        super(MetaType, self).save(*args, **kwargs)
        # schedule objects rebuild
        Reload.schedule()
    
    def __unicode__(self):
        return self.name


FIELDS = Fields().get_set() 
class Field(models.Model):
    name = models.CharField(max_length=255)
    metaType = models.ForeignKey(MetaType)
    ftype = models.CharField(max_length=50, choices=FIELDS)

    def __unicode__(self):
        return self.metaType.name + " > " + self.name


PROPERTIES = Fields().get_available_properties()
class Property(models.Model):
    name = models.CharField(max_length=50, choices=PROPERTIES)
    value = models.CharField(max_length=50)
    field = models.ForeignKey(Field)
    
    def __unicode__(self):
        return self.field.metaType.name + " > " + self.field.name + " > " + self.name

    class Meta:
        verbose_name_plural = "Properties"

try:
    metaMan.buildClasses(MetaType)
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
