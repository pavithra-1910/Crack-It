import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('firebase-admin.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-database-url.firebaseio.com/'
})
def get_username(user_id):
    ref = db.reference(f'users/{user_id}/username')
    return ref.get()
