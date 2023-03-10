# machfun

Database Structure
==================

* **admin**

* **user**/{uid}/
  User private data. No one else has access to here accept for the user.


**Functions**

**run_machina function**

run_machina function gets executed when the master run document is created at:
  project/{id}/run/{runId}
this function looks for all empty input (initial/bootstrap/head) cells and 
creates run documents to kick off their runs in their respective run collections:
  project/{id}/cell/{cellId}/run/{runId}


To deploy run_machina function:

gcloud functions deploy run_machina \
  --project avtomat-40a28 \
  --entry-point run_machina \
  --runtime python37 \
  --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
  --trigger-resource "projects/avtomat-40a28/databases/(default)/documents/project/{id}/run/{runId}" \
  --set-env-vars OPENAI_KEY=TEST_KEY


**run_cell_exec function**

run_cell_exec function gets executed when individual cell run
document gets created at: project/{id}/cell/{cellId}/run/{runId}


Deploy run_cell_exec function:

gcloud functions deploy run_cell_exec \
  --project avtomat-40a28 \
  --entry-point run_cell_exec \
  --runtime python37 \
  --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
  --trigger-resource "projects/avtomat-40a28/databases/(default)/documents/project/{id}/cell/{cellId}/run/{runId}" \
  --set-env-vars OPENAI_KEY=TEST_KEY


**on_cell_run_update function**

on_cell_run_update function gets executed when individual cell run gets updated at: project/{id}/cell/{cellId}/run/{runId}

it checks if the status is not 'completed' and then will
check if any other cells can start execution based on this
cell's completion (input being available).

Deploy run_cell_exec function:

gcloud functions deploy on_cell_run_update \
  --project avtomat-40a28 \
  --entry-point on_cell_run_update \
  --runtime python37 \
  --trigger-event "providers/cloud.firestore/eventTypes/document.update" \
  --trigger-resource "projects/avtomat-40a28/databases/(default)/documents/project/{id}/cell/{cellId}/run/{runId}" \
  --set-env-vars OPENAI_KEY=TEST_KEY





Run locally:

pip3 install -r requirements.txt
