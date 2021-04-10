from zipfile import ZipFile, ZIP_DEFLATED
from sys import argv
import pyrebase

config = {
    'apiKey': "AIzaSyCbclsVrbrr2DKco5e-z3j_m6VUiKdI504",
    'authDomain': "contract-generator-f02ca.firebaseapp.com",
    'databaseURL': "https://contract-generator-f02ca-default-rtdb.firebaseio.com",
    'storageBucket': "contract-generator-f02ca.appspot.com",
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
database = firebase.database()
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(argv[2], argv[3])

with ZipFile('update.zip', 'w', ZIP_DEFLATED) as archive:
    archive.write('dist/main.exe', 'main.exe')
    archive.write('changelog.txt')

storage.child('update.zip').put('update.zip', user['idToken'])
database.child('/').update({'latest_version': argv[1]}, user['idToken'])
