from django.db import connection
from django.db import models
from django.core.management.color import no_style

from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from meta.fields import Fields
import inspect

import meta
from meta.actions import Actions

class MetaMan:
    __metaClasses = {} #static

    __actionsObjects = {}

    def add_model(self, cls):
        objName = cls._meta.object_name 
        self.__metaClasses[objName] = cls
        # build and register an action object
        self.__actionsObjects[str(objName)] = Actions(cls)

    def remove_model(self, cls):
        pass

    def get_all_classes(self):
        return self.__metaClasses.values()

    def build_object(self, typeName):
        """
        Return an instance of type name
        Usage example:
            o = metaMan.buildObject('Type1')
            o.name = "test name"
            o.save()
        """
        cls = self.__metaClasses[typeName]
        obj = cls()
        return obj

    def get_class(self, typeName):
        """
        Return the type class.
        Usage example:
            t = metaMan.getClass('Type1')
            t.objects.all()
        """
        return self.__metaClasses[typeName]

    def build_classes(self):
        """
        Build defined types classes and put them
        into meta.models module.
        """
        # NOTE: trying to import MetaType on the top of the file doesn't work 
        from meta.models import MetaType, BaseType
        #mtypeObjects = MetaTypeModel.objects.all()
        mtypeObjects = MetaType.objects.filter(syncready=True)
        for metatype in mtypeObjects:
            fields = metatype.field_set.all()

            def mod_unicode(self):
                string = ""
                for f in self._meta.local_fields:
                    string += "%s " % getattr(self, f.name)
                return string
            # __module__ param is required by the django model meta class
            dct = {
                '__module__': 'meta.models',
                '__unicode__': mod_unicode 
            }
            for field in fields:
                cls = Fields().get_class_by_name(field.ftype)
                properties =  Fields.get_properties_assoc(field)
                if len(properties) == 0:
                    # TODO: Should never go here. We must always have needed params when build a field. 
                    if issubclass(cls, Fields().get_class_by_name('CharField')): 
                        obj = cls(max_length = 255)
                    elif issubclass(cls, Fields().get_class_by_name('DecimalField')):
                        obj = cls(max_digits = 20, decimal_places = 4)
                    else:
                        obj = cls()
                else:
                    #print properties
                    obj = cls(**properties) # unpack properties
                
                dct[field.name] = obj
           
            if metatype.extend is None: 
                # define the new type
                obj = type(str(metatype.name), (BaseType,), dct)
            else:
                cls = self.get_class(metatype.extend.name)
                # TODO: cls could not exist here becouse it is not
                #       built still.

                # TODO: check for valid class names. It seems that
                #       extending from objects with spaces into class name
                #       I have problems
                obj = type(str(metatype.name), (cls,), dct)

            if metatype.name_plural != "":
                obj._meta.verbose_name_plural = metatype.name_plural
            
            try:
                # build a more confortable admin site here inspecting
                # for fields and adding them to Admin list_display
                lst =[]
                i = 0
                MAX_FIELDS = 5
                father = metatype.extend
                while father:
                    inherited_fields = father.field_set.all()
                    for field in inherited_fields:
                        lst.append(field.name)
                        i += 1
                        if i == MAX_FIELDS: break
                    father = father.extend
                    #all_fields += inherited_fields
                if i < MAX_FIELDS:
                    for field in fields:
                        lst.append(field.name)
                        i += 1
                        if i == MAX_FIELDS: break
                
                class ObjAdmin(admin.ModelAdmin):
                    list_display = lst 
                admin.site.register(obj, ObjAdmin)
            except AlreadyRegistered:
                pass
            self.add_model(obj)
       
        # create tables if not already exists
        self.sync_models()

    def get_model_urls(self):
        from django.conf.urls.defaults import patterns, url, include
        urlpatterns = [] 
        for name in self.__metaClasses.keys():
            cls_url = name.lower()
            actions = self.__actionsObjects[name]
            urlpatterns += patterns('',
                url(r'^%s/' % (cls_url), include(actions.urls))
            )
        return urlpatterns
    urls = property(get_model_urls)


    def sync_models(self):
        """
        Sync dynamic objects with db creating tables if they doesn't exists
        """
        models = self.get_all_classes()
        #print "Meta models: " + str(models)
        style = no_style()    
        cursor = connection.cursor()

        final_output = []
        tables = connection.introspection.table_names()
        known_models = connection.introspection.installed_models(tables)
        pending_references = {}
   
        for model in models:
            # if the table for model already exists continue 
            if model._meta.db_table in tables: continue
            # don't try do create tables for abstract models
            if model._meta.abstract: continue
            output, references = connection.creation.sql_create_model(model, style, known_models)
            final_output.extend(output)
            for refto, refs in references.items():
                pending_references.setdefault(refto, []).extend(refs)
                if refto in known_models:
                    final_output.extend(connection.creation.sql_for_pending_references(refto, style, pending_references))
            final_output.extend(connection.creation.sql_for_pending_references(model, style, pending_references))
            # Keep track of the fact that we've created the table for this model.
            known_models.add(model)

        # Handle references to tables that are from other apps
        # but don't exist physically.
        not_installed_models = set(pending_references.keys())
        if not_installed_models:
            alter_sql = []
            for model in not_installed_models:
                alter_sql.extend(['-- ' + sql for sql in
                    connection.creation.sql_for_pending_references(model, style, pending_references)])
            if alter_sql:
                final_output.append('-- The following references should be added but depend on non-existent tables:')
                final_output.extend(alter_sql)
       
        if len(final_output) > 0: 
            sql =  u'\n'.join(final_output).encode('utf-8')
            #print sql
            cursor.execute(sql)

metaman = MetaMan()
