import json
from google.cloud import firestore
import asyncio
import os
openai_key = os.environ.get('OPENAI_KEY')

client = firestore.Client()

def get_env_var(request):
  return os.environ.get(request, 'Specified environment variable is not set.')

def on_cell_run_update(data, context):
    """ Triggered on a change to a cell run document at project/{id}/cell/{cellId}/run/{runId}
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

    if(data["oldValue"] is None):
      return

    if(data["value"] is None):
      return
    
    if(data["value"]["fields"]["status"] is None):
      return

    if(data["oldValue"]["fields"]["status"] is None):
      return

    if(
      data["oldValue"]["fields"]["status"]["stringValue"] != "completed" and
      data["value"]["fields"]["status"]["stringValue"] == "completed"):
      print(u'cell run {trigger_resource} completed')
      return 
    
    path_parts = context.resource.split('/documents/')[1].split('/')
    collection_path = path_parts[0]
    # document_path = '/'.join(path_parts[1:])
    # cell_run_doc_ref = client.collection(collection_path).document(document_path)

    print('list all cell runs that did not complete yet')
    outstanding_cell_runs=client.collection(collection_path).where(u'status', u'==', 'running').get()
    print(f'found {outstanding_cell_runs} docs with running status')
    for doc in outstanding_cell_runs:
      print(f'{doc.id} => {doc.to_dict()}')
