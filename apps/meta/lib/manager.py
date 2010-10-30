from django.db import connection
from django.db import models
from django.core.management.color import no_style

from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from meta.lib.fields import Fields

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

#    def buildClasses(self, mtypeObjects):
    def buildClasses(self, MetaTypeModel):
        """
        Build defined types classes and put them
        into meta.models module
        NOTE: For some reason we can't simply do a from meta.models import MetaType
        """
        mtypeObjects = MetaTypeModel.objects.all()
        # TODO: implement type inheritance
        for mtype in mtypeObjects:
            fields = mtype.field_set.all()

            # __module__ param is required by the django model meta class
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
                    # unpack properties
                    obj = cls(**properties)
                
                dct[field.name] = obj
           
            if mtype.name_plural != "":
                # define the django model Meta class
                # class MyModel(models.Model):
                #    myfield = models.IntegerField()
                #    class Meta:
                #       verbose_name_plural = "MyModels" 
                #
                # I use a Temp class here that is injected into
                # type definition through the dict
                class Temp:
                    verbose_name_plural = mtype.name_plural
                dct['Meta'] = Temp
            
            # define the new type
            obj = type(str(mtype.name), (models.Model,), dct)
            try:
                admin.site.register(obj)
            except AlreadyRegistered:
                pass
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
