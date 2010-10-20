from django.db import connection
from django.core.management.color import no_style

from django.db.models.loading import AppCache

APP_NAME = 'meta'


def sync_meta_models():

    ac = AppCache()
    models = ac.app_models.get(APP_NAME).values()

    style = no_style()    

    cursor = connection.cursor()

    final_output = []
    tables = connection.introspection.table_names()
    known_models = connection.introspection.installed_models(tables)

    pending_references = {}
   
    for model in models:
        # se la tabella gia' esiste vai avanti
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
