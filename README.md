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
  --set-env-vars openai_key= \
  --entry-point run_cell_exec \
  --runtime python37 \
  --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
  --trigger-resource "projects/avtomat-40a28/databases/(default)/documents/execRow/{execRowId}/cell/{cellId}/run/{runId}"

