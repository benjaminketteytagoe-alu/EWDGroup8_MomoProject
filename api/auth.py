from dotenv import load_dotenv
from flask_httpauth import HTTPBasicAuth
import os
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
USERNAME = os.getenv("AUTH_USERNAME")
PASSWORD = generate_password_hash(
    os.getenv("AUTH_PASSWORD"), method="pbkdf2:sha256")

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == USERNAME and check_password_hash(PASSWORD, password):
        return username
