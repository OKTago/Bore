from django.db import connection
from django.db import models
from django.core.management.color import no_style

from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from meta.lib.fields import Fields
import mtype
import inspect
from mtype.cmodels import *

class MetaMan:
    __metaClasses = {} #static

    def addModel(self, cls):
        objName = cls._meta.object_name 
        self.__metaClasses[objName] = cls

    def removeModel(self, cls):
        pass

    def getAllClasses(self):
        return self.__metaClasses.values()

    def buildObject(self, typeName):
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

    def getClass(self, typeName):
        """
        Return the type class.
        Usage example:
            t = metaMan.getClass('Type1')
            t.objects.all()
        """
        return self.__metaClasses[typeName]

    # NOTE: For some reason we can't simply do a from meta.models import MetaType
    def buildClasses(self, MetaTypeModel):
        """
        Build defined types classes and put them
        into mtype.models module. It don't ovverride custom defined models
        in mtype.cmodels module but take them instead and manage them building
        needed tables and putting into mtype.models namespace. You can use them
        in the same way as you do with user interface defined types.
        """
        #mtypeObjects = MetaTypeModel.objects.all()
        mtypeObjects = MetaTypeModel.objects.filter(syncready=True)
        for metatype in mtypeObjects:
            try:
                # do not ovverride types defined into mtype app.
                # eval here is probably a bit hackish but for now I don't 
                # have a better solution
                obj = eval(metatype.name)
                self.addModel(obj)
                continue
            except NameError:
                pass
            fields = metatype.field_set.all()

            # __module__ param is required by the django model meta class
            # I put dynamic defined meta types into mtype app namespace
            dct = {
                '__module__': 'mtype.models'
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
           
            if metatype.name_plural != "":
                # define the django model Meta class
                # class MyModel(models.Model):
                #    myfield = models.IntegerField()
                #    class Meta:
                #       verbose_name_plural = "MyModels" 
                #
                # I use a Temp class here that is injected into
                # type definition through the dict
                class Temp:
                    verbose_name_plural = metatype.name_plural
                dct['Meta'] = Temp
            if metatype.extend is None: 
                # define the new type
                obj = type(str(metatype.name), (models.Model,), dct)
            else:
                cls = self.getClass(metatype.extend.name)
                # TODO: cls could not exist here becouse it is not
                #       built still.

                # TODO: check for valid class names. It seems that
                #       extending from objects with spaces into class name
                #       I have problems
                obj = type(str(metatype.name), (cls,), dct)

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
            self.addModel(obj)
       
        # discover and register manual defined models 
        for name in dir(mtype.cmodels):
            obj = getattr(mtype.cmodels, name)
            if inspect.isclass(obj):
                self.addModel(obj)        

        # create tables if not already exists
        self.syncModels()


    def syncModels(self):
        """
        Sync dynamic objects with db creating tables if they doesn't exists
        """
        models = self.getAllClasses()
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
