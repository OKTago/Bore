from django.db import connection
from django.db.models.loading import AppCache
from django.db import models
from django.core.management.color import no_style

from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from meta.lib.fields import Fields

APP_NAME = 'meta'

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

    def buildClasses(self, mtypeObjects):
        """
        Build defined types classes and put them
        into meta.models module
        """
        for mtype in mtypeObjects:
            fields = mtype.typefield_set.all()
            dct = {
                '__module__': 'meta.models'
            }
            for field in fields:
                cls = Fields().get_class_by_name(field.field)()
                dct[field.name] = cls
            obj = type(str(mtype.name), (models.Model,), dct)
            try:
                admin.site.register(obj)
            except AlreadyRegistered:
                pass
            self.addModel(obj)

        self.syncModels()


    def syncModels(self):
        """
        Sync dynamic objects with db creating tables if they doesn't exists
        """
       # ac = AppCache()
       # models = ac.app_models.get(APP_NAME).values()

        models = self.getAllClasses()
        print models
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
            cursor.execute(sql)
