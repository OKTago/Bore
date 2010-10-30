from meta.models import Field, MetaType, Property, Reload
from django.contrib import admin

class FieldInline(admin.TabularInline):
    model = Field


#def schedule_build(modeladmin, request, queryset):
#    Reload.schedule()
#schedule_build.short_description = "Sync Meta Types"
class MetaTypeAdmin(admin.ModelAdmin):
#    actions = [
#        schedule_build
#    ]
    inlines = [
        FieldInline,
    ]
admin.site.register(MetaType, MetaTypeAdmin)

class PropertyInline(admin.TabularInline):
    model = Property

class FieldAdmin(admin.ModelAdmin):
    inlines = [
        PropertyInline,
    ] 
admin.site.register(Field, FieldAdmin)
