
from firebase_admin import credentials
import firebase_admin
from firebase_admin import db
import base64

cred = credentials.Certificate('fetch/cred.json')
url = 'https://neosalpha-999-default-rtdb.firebaseio.com/'
path = {'databaseURL' : url}


if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, path)


def call(path = 'apigee'):
    refv = db.reference(path)
    name = refv.get()
    return name


def send(path, data = {}):
    refv = db.reference(path)
    refv.set(data)


def encodeit(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def decodeit(base64_message):
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message

    