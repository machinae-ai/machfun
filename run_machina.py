import json
from google.cloud import firestore
import asyncio
from get_page_dynamic import get_page_dynamic
import os
from merge_json import merge_json
from page_parser import get_page
# Import the Firebase service
# from firebase_admin import auth


client = firestore.Client()
# default_app = firebase_admin.initialize_app()

# def get_env_var(request):
#   return os.environ.get(request, 'Specified environment variable is not set.')
  
def get_oldest_document(collection):
    docs = collection.order_by(u'timeCreated', direction=firestore.Query.DESCENDING).limit(1).get()
    for doc in docs:
        return doc

def run_machina(data, context):
    """ Triggered by a change to a Firestore document.
    Args:
        data (dict): The event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    trigger_resource = context.resource

    print('Function triggered by change to: %s' % trigger_resource)

    print('\nOld value:')
    print(json.dumps(data["oldValue"]))

    print('\nNew value:')
    print(json.dumps(data["value"]))

    path_parts = context.resource.split('/documents/')[1].split('/')
    collection_path = path_parts[0]
    document_path = '/'.join(path_parts[1:])
    master_run_doc = client.collection(collection_path).document(document_path)
    # FIXIT: make the path relative to the affected document path
    cell_col = client.collection('project/1/cell')
    # type = data["value"]["fields"]["type"]["stringValue"]

    # get_docs_with_empty_input=client.collection(u'cell').where(u'input', u'==', None).get()    
    print(f'cell path: {cell_col}')
    # FIXIT: make 'none' work with null/empty document field instead of string 'none'
    cell_docs_with_empty_input=cell_col.where(u'input', u'==', None).get()
    print(f'found {cell_docs_with_empty_input} docs with empty input')
    for doc in cell_docs_with_empty_input:
        create_run(master_run_doc, doc)

def create_run(master_run_doc, cell_doc):
    print(f'creating run for {cell_doc.id}, {cell_doc.to_dict()}')    
    run_ref = master_run_doc.collection('cell_run').document(cell_doc.id)
    run_ref.set(cell_doc.to_dict())
    run_ref.update({
      u'timeCreated': firestore.SERVER_TIMESTAMP,
      u'status': 'running',
    })    
    print('created run %s' % run_ref.id)