# machfun

Database Structure
==================

* **admin**

* **user**/{uid}/
  User private data. No one else has access to here accept for the user.


**Functions**

**on_run_create function**

on_run_create function gets executed when the master run document is created at:
  project/{id}/run/{runId}
this function looks for all empty input (initial/bootstrap/head) cells and 
creates run documents to kick off their runs in their respective run collections:
  project/{id}/cell/{cellId}/run/{runId}


To deploy on_run_create function:

gcloud functions deploy on_run_create \
  --project avtomat-40a28 \
  --entry-point on_run_create \
  --runtime python37 \
  --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
  --trigger-resource "projects/avtomat-40a28/databases/(default)/documents/project/{id}/run/{runId}" \
  --set-env-vars OPENAI_KEY=TEST_KEY

**on_input_create function**

on_input_create function gets executed when the input run document is created at:
  project/{id}/run/{runId}/input/{inputId}
this function looks for all cells that rely on the input created and
creates run documents to kick off their runs in their respective run collections:
  project/{id}/run/{runId}/run/{cellRunId}

To deploy on_input_create function:

gcloud functions deploy on_input_create \
  --project avtomat-40a28 \
  --entry-point on_input_create \
  --runtime python37 \
  --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
  --trigger-resource "projects/avtomat-40a28/databases/(default)/documents/project/{id}/run/{runId}/input/{inputId}" \
  --set-env-vars OPENAI_KEY=TEST_KEY


**on_cell_run_create function**

on_cell_run_create function gets executed when individual cell run
document gets created at: project/{id}/cell/{cellId}/run/{runId}


Deploy on_cell_run_create function:

gcloud functions deploy on_cell_run_create \
  --project avtomat-40a28 \
  --entry-point on_cell_run_create \
  --runtime python37 \
  --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
  --trigger-resource "projects/avtomat-40a28/databases/(default)/documents/project/{id}/run/{runId}/run/{cellRunId}" \
  --set-env-vars OPENAI_KEY=TEST_KEY


**on_cell_run_update function**

on_cell_run_update function gets executed when individual cell run gets updated at: project/{id}/cell/{cellId}/run/{runId}

it checks if the status is not 'completed' and then will
check if any other cells can start execution based on this
cell's completion (input being available).

Deploy on_cell_run_update function:

gcloud functions deploy on_cell_run_update \
  --project avtomat-40a28 \
  --entry-point on_cell_run_update \
  --runtime python37 \
  --trigger-event "providers/cloud.firestore/eventTypes/document.update" \
  --trigger-resource "projects/avtomat-40a28/databases/(default)/documents/project/{id}/cell/{cellId}/run/{runId}" \
  --set-env-vars OPENAI_KEY=TEST_KEY



Run locally:

pip3 install -r requirements.txt

python3 test.py
