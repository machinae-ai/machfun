import json
from google.cloud import firestore
import asyncio
from get_page_dynamic import get_page_dynamic
import os
from page_parser import get_page
import openai
openai_key = os.environ.get('OPENAI_KEY')

client = firestore.Client()

def get_env_var(request):
  return os.environ.get(request, 'Specified environment variable is not set.')

def on_cell_run_create(data, context):
    """ Triggered by a creation of a cell run document
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
    cell_doc_ref = client.collection(collection_path).document(document_path)


    type = data["value"]["fields"]["type"]["stringValue"]

    if(type=='python'):
      execute_python(data["value"]["fields"]["code"]["stringValue"],
                     data["value"]["fields"]["output"]["stringValue"], cell_doc_ref)
    elif(type=='eval'):
      evaluate_python(data["value"]["fields"]["code"]["stringValue"],
                     data["value"]["fields"]["output"]["stringValue"], 
                      cell_doc_ref)
    elif(type=='gpt_text'):
      gpt_text_request(data, cell_doc_ref)
    elif(type=='gpt_code'):
      gpt_code_request(data, cell_doc_ref)
    elif(type=='get_page'):
      fetch_webpage(data, cell_doc_ref)
    else:
      raise Exception('unknown exec type: ' + type)

def fetch_webpage(data, run_doc_ref):
    url = data["value"]["fields"]["url"]["stringValue"]
    print('getting page: ' + url)
    output = get_page_dynamic(url)
    print('done getting page')
    print(output)
    
    run_doc_ref.update({
        u'timeCompleted': firestore.SERVER_TIMESTAMP,
        u'status': 'completed',
        u'result': output
      })
    run_doc_ref.parent.parent.collection('input').document(data["value"]["fields"]["output"]["stringValue"]).set({
      u'timeCreated': firestore.SERVER_TIMESTAMP,
      u'value': output
    })


def gpt_text_request(data, run_doc_ref):
    prompt = data["value"]["fields"]["prompt"]["stringValue"]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
        api_key=openai_key
      )
    print(response.choices[0].text)
    output=response['choices'][0]['text']
    run_doc_ref.update({
        u'timeCompleted': firestore.SERVER_TIMESTAMP,
        u'status': 'completed',
        u'result': output
      })
    run_doc_ref.parent.parent.collection('input').document(data["value"]["fields"]["output"]["stringValue"]).set({
      u'timeCreated': firestore.SERVER_TIMESTAMP,
      u'value': output
    })

def gpt_code_request(data, run_doc_ref):
    prompt = data["value"]["fields"]["prompt"]["stringValue"]
    try:
      response = openai.Completion.create(
          engine="code-davinci-002",
          prompt=f"\"\"\"\n{prompt}\n\"\"\"",
          max_tokens=50,
          n=1,
          stop=None,
          temperature=0,
          api_key=openai_key
        )
      print(response.choices[0].text)
      output=response['choices'][0]['text']
    except Exception as e:        
      error_message = str(e)      
      run_doc_ref.update({
        u'timeCompleted': firestore.SERVER_TIMESTAMP,
        u'status': 'completed',
          u'result': 'Error: ' + error_message
        })
    # Remove '+' sign and '\n' from the beginning of the generated code
    # if generated_code.startswith('+'):
    #     generated_code = generated_code[1:].lstrip('\n')
    # generated_code = generated_code.replace('+', '')
    run_doc_ref.update({
        u'timeCompleted': firestore.SERVER_TIMESTAMP,
        u'status': 'completed',
        u'result': output 
      })
    run_doc_ref.parent.parent.collection('input').document(data["value"]["fields"]["output"]["stringValue"]).set({
      u'timeCreated': firestore.SERVER_TIMESTAMP,
      u'value': output
    })


def evaluate_python(code, output, run_doc_ref):
    print('evaluate python:')
    print(code)
    code_string=code
    try:
      result=eval(code_string)
      run_doc_ref.update({
          u'result': result
        })
    except Exception as e:        
      error_message = str(e)      
      run_doc_ref.update({
        u'timeCompleted': firestore.SERVER_TIMESTAMP,
        u'status': 'completed',
          u'result': 'Error: ' + error_message
        })
    run_doc_ref.parent.parent.collection('input').document(output).set({
      u'timeCreated': firestore.SERVER_TIMESTAMP,
      u'value': result
    })
    run_doc_ref.update({
      u'timeCompleted': firestore.SERVER_TIMESTAMP,
      u'status': 'completed',
      u'result': 'Error: ' + error_message
    })
    print('done evaluating code')

def execute_python(code, output, run_doc_ref):
    print('executing code:')
    print(code)
    code_string=code
    result=None
    try:
      global_vars = {}
      inputs=collect_inputs(data["value"]["fields"]["inputs"]["stringValue"], run_doc_ref)
      local_vars = {inputs}
      exec(code_string, global_vars, local_vars)            
      result=local_vars['output'] if 'output' in local_vars else None
      print(result, local_vars)
    except Exception as e:        
      error_message = str(e)      
      run_doc_ref.update({ 
        u'timeCompleted': firestore.SERVER_TIMESTAMP,
        u'status': 'completed',
          u'result': 'Error: ' + error_message
        })
    run_doc_ref.update({
      u'timeCompleted': firestore.SERVER_TIMESTAMP,
      u'status': 'completed',
      u'result': result
    })
    run_doc_ref.parent.parent.collection('input').document(output).set({
      u'timeCreated': firestore.SERVER_TIMESTAMP,
      u'value': result
    })
    print('done executing code')


def collect_inputs(inputs_array, run_doc_ref):
  res_array=[]
  for input in inputs_array:
    res_array.append(run_doc_ref.collection('input').document(input).get())
  return res_array
    
    
  
