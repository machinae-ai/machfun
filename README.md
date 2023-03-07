# machfun

Database Structure
==================

* **admin**

* **user**/{uid}/
  User private data. No one else has access to here accept for the user.


**Deploying functions**

Deploy run_cell_exec function:

gcloud functions deploy run_cell_exec \
  --project avtomat-40a28 \
  --entry-point run_cell_exec \
  --runtime python37 \
  --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
  --trigger-resource "projects/avtomat-40a28/databases/(default)/documents/project/{id}/cell/{cellId}/run/{runId}" \
  --set-env-vars OPENAI_KEY=TEST_KEY


Deploy run_machina function:

gcloud functions deploy run_machina \
  --project avtomat-40a28 \
  --entry-point run_machina \
  --runtime python37 \
  --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
  --trigger-resource "projects/avtomat-40a28/databases/(default)/documents/project/{id}/run/{runId}" \
  --set-env-vars OPENAI_KEY=TEST_KEY
