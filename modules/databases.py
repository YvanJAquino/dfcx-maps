import os
from google.cloud import firestore

fs = firestore.Client()
collection_id = os.environ.get('SESSIONS_COLLECTION')
if not collection_id:
    collection_id = 'sessions'
sessions = fs.collection(collection_id)