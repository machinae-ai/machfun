import json
from google.cloud import firestore
import asyncio
from get_page_dynamic import get_page_dynamic
import os
from merge_json import merge_json
from page_parser import get_page

client = firestore.Client()

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
    affected_doc = client.collection(collection_path).document(document_path)
    # type = data["value"]["fields"]["type"]["stringValue"]

    get_docs_with_empty_input=client.collection(u'cell').where(u'input', u'==', None).get()
    for doc in get_docs_with_empty_input:
        create_run(doc)





# def get_docs_with_empty_input(col_ref):
#     docs = col_ref.where(u'input', u'==', u'').get()
#     return docs

def create_run(doc_ref):
    print('creating run')
    print(doc_ref.id)
    run_ref = client.collection(u'run').document()
    run_ref.set(merge_json(doc_ref.to_dict(), { u'timeCreated': firestore.SERVER_TIMESTAMP }))
    print('created run')