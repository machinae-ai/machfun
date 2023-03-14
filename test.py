import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from inputs import start_runs_for_input

from on_cell_run_create import execute_python

db = firestore.Client.from_service_account_json("avtomat-40a28-firebase-adminsdk-q0zqt-7cd8741333.json")

project_ref=db.collection(u'project').document(u'1')
master_run_ref=db.collection(u'project').document(u'1').collection(u'run').document(u'Kw02PeuPgo7pO20fmGvv')

start_runs_for_input(master_run_ref, 'init')

