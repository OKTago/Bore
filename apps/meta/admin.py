from meta.models import Field, MetaType, Property, Reload
from django.contrib import admin

from meta.models import Relation
from django.contrib.contenttypes import generic

admin.site.register(Relation)

class FieldInline(admin.TabularInline):
    model = Field

class MetaTypeAdmin(admin.ModelAdmin):
    inlines = [
        FieldInline,
    ]
    list_display = ('name', 'syncready')
    list_filter = ('syncready',)
admin.site.register(MetaType, MetaTypeAdmin)

class PropertyInline(admin.TabularInline):
    model = Property

class FieldAdmin(admin.ModelAdmin):
    inlines = [
        PropertyInline,
    ] 
    list_display = ('name', 'ftype', 'metaType')
    list_filter = ('metaType',)
admin.site.register(Field, FieldAdmin)
