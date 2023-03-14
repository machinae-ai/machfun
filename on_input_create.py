import json
from google.cloud import firestore
import os

from inputs import start_runs_for_input

openai_key = os.environ.get('OPENAI_KEY')


db = firestore.Client()

def get_env_var(request):
  return os.environ.get(request, 'Specified environment variable is not set.')

def on_input_create(data, context):
    """ Triggered on creation of input document at project/{id}/run/{runId}/input/{id}
    Args:
        data (dict): The event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    input_doc_id = context.resource.split("/")[-1]
        
    print(input_doc_id)

    # Use the path to get a reference to the affected document
    doc_ref = db.document(context.resource)
    
    # data_dic=data["value"].to_dict()
    
    # print(u'input created: {doc_ref.id}, {data_dic}')
    # data["value"]["fields"]["id"]["stringValue"]
    
    start_runs_for_input(doc_ref.parent.parent, input_doc_id)

    # transaction = db.transaction()
    # city_ref = db.collection(u'cities').document(u'SF')

    # @firestore.transactional
    # def update_in_transaction(transaction, city_ref):
    #     snapshot = city_ref.get(transaction=transaction)
    #     transaction.update(city_ref, {
    #         u'population': snapshot.get(u'population') + 1
    #     })

    # update_in_transaction(transaction, city_ref)

    # if(
    #   data["oldValue"]["fields"]["status"]["stringValue"] != "completed" and
    #   data["value"]["fields"]["status"]["stringValue"] == "completed"):
    #   print(u'cell run {trigger_resource} completed')
    #   return 
    
    # path_parts = context.resource.split('/documents/')[1].split('/')
    # collection_path = path_parts[0]
    # # document_path = '/'.join(path_parts[1:])
    # # cell_run_doc_ref = client.collection(collection_path).document(document_path)

    # print('list all cell runs that did not complete yet')
    # outstanding_cell_runs=client.collection(collection_path).where(u'status', u'==', 'running').get()
    # print(f'found {outstanding_cell_runs} docs with running status')
    
    # for doc in outstanding_cell_runs:
    #   print(f'{doc.id} => {doc.to_dict()}')
