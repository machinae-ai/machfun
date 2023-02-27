import json
from google.cloud import firestore
import asyncio
from get_page_dynamic import get_page_dynamic
import os
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

    first_row=get_oldest_document(client.collection('execRow'))

    print(f'first_row: {first_row}')

    first_row

    document_url = data["value"]["fields"]["input"]["stringValue"]



    path_parts = context.resource.split('/documents/')[1].split('/')
    parent_collection_path = '/'.join(path_parts[:-1])
    parent_document_path = '/'.join(path_parts[:-2])
    
    collection_path = path_parts[0]
    document_path = '/'.join(path_parts[1:])
    affected_doc = client.collection(collection_path).document(document_path)

    print(f'parent_document_path: {parent_document_path}')
    parent_doc = client.document(parent_document_path)

    print(f'parent_doc: {parent_doc}')
    parent_doc_data = parent_doc.get().to_dict()

    print(f'parent_doc_data: {parent_doc_data}')

    python_code=parent_doc_data['code']

    # # Condition to check if the url is from dynamic webpage
    if (parent_doc_data['type']=='code'):
      exec(python_code)
    elif (parent_doc_data['type']=='fetch'):
      if(parent_doc_data['fetch_type']=='dynamic'):
        pageText = asyncio.run(get_page_dynamic(parent_doc_data['url']))
        affected_doc.update({
          u'response': pageText
        })
      # For static webpage
      else:
        pageText = get_page(parent_doc_data['url'])
        affected_doc.update({
          u'response': pageText
        })
    elif (parent_doc_data['type']=='gpt'):      
      import openai
      openai.api_key = 'sk-somekeygoeshere' 
      # We can keep temperature=0 to remove radomness
      response = openai.Completion.create(
        model="text-davinci-003",
        prompt = parent_doc_data['prompt'],
        temperature=parent_doc_data['temp'],
        max_tokens=parent_doc_data['tokens'], #700
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
      )
      print(f'openai response: {response}')
      affected_doc.update({
        u'response': response
      })


