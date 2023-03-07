import json
from google.cloud import firestore
import asyncio
from get_page_dynamic import get_page_dynamic
import os
from page_parser import get_page
import openai
import os
openai_key = os.environ.get('OPENAI_KEY')

client = firestore.Client()

def get_env_var(request):
  return os.environ.get(request, 'Specified environment variable is not set.')

def run_cell_exec(data, context):
    """ Triggered by a creation of a Firestore document!
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


    type = data["value"]["fields"]["type"]["stringValue"]

    if(type=='python'):
      print('executing code:')
      print(data["value"]["fields"]["code"]["stringValue"])
      code_string=data["value"]["fields"]["code"]["stringValue"]
      try:
        exec(code_string)
      except Exception as e:        
        error_message = str(e)      
        affected_doc.update({
        u'timeCompleted': firestore.SERVER_TIMESTAMP,
        u'status': 'completed',
          u'output': 'Error: ' + error_message
        })
      print('done executing code')
    elif(type=='eval'):
      print('evaluate python:')
      print(data["value"]["fields"]["code"]["stringValue"])
      code_string=data["value"]["fields"]["code"]["stringValue"]
      try:
        output=eval(code_string)
        affected_doc.update({
          u'output': output
        })
      except Exception as e:        
        error_message = str(e)      
        affected_doc.update({
        u'timeCompleted': firestore.SERVER_TIMESTAMP,
        u'status': 'completed',
          u'output': 'Error: ' + error_message
        })
      print('done evaluating code')
    elif(type=='gpt'):
      prompt = data["value"]["fields"]["prompt"]["stringValue"]
      response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
      )
      print(response.choices[0].text)
      generated_code=response['choices'][0]['text']
      # Remove '+' sign and '\n' from the beginning of the generated code
      if generated_code.startswith('+'):
          generated_code = generated_code[1:].lstrip('\n')
      generated_code = generated_code.replace('+', '')
      affected_doc.update({
        u'timeCompleted': firestore.SERVER_TIMESTAMP,
        u'status': 'completed',
        u'output': generated_code #response.choices[0].text
      })
    elif(type=='get_page'):
      url = data["value"]["fields"]["url"]["stringValue"]
      print('getting page: ' + url)
      page = get_page_dynamic(url)
      print('done getting page')
      print(page)
      affected_doc.update({
        u'timeCompleted': firestore.SERVER_TIMESTAMP,
        u'status': 'completed',
        u'output': page
      })


