import firebase_admin
from firebase_admin import credentials, auth
import pyrebase
import os
from dotenv import load_dotenv, dotenv_values 

API_KEY = os.getenv("FIREBASE_API_KEY")

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

config = {
  "apiKey": API_KEY,
  "authDomain": "recycleus-ef1a3.firebaseapp.com",
  "storageBucket": "recycleus-ef1a3.appspot.com",
  "messagingSenderId": "114600752569",
  "appId": "1:114600752569:web:ed4754a14f3f81e0123268",
  "databaseURL": "",
}

firebase = pyrebase.initialize_app(config)
auth_instance = firebase.auth()

def sign_up(email, password):
    try:
        user = auth_instance.create_user_with_email_and_password(email, password)
        return user
    except Exception as e:
        print(f"Firebase signup error: {str(e)}")
        return None

def sign_in(email, password):
	try:
		user = auth_instance.sign_in_with_email_and_password(email, password)
		return user
	except:
		return None

def get_account_info(id_token):
	try:
		user = auth.verify_id_token(id_token)
		return user
	except:
		return None