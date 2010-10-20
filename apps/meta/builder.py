from django.db import connection
from django.core.management.color import no_style


def sync_meta_model(models):

    # nei modelli ci deve gia' essere Document_tag che non c'e' 
    # verificare perche'
    style = no_style()    

    cursor = connection.cursor()

    final_output = []
    tables = connection.introspection.table_names()
    known_models = set([model for model in connection.introspection.installed_models(tables) if model not in models])
    #print known_models

    pending_references = {}
   
    for model in models:
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
    
    print u'\n'.join(final_output).encode('utf-8')

def test():
    from meta.models import *
    models = [Tag, Document, Object]
    sync_meta_model(models)
