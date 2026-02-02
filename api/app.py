# This is the main application file for the Momo Project API

from flask import Flask, request, jsonify, abort
import base64
from urllib.parse import unquote
from models import db, Config, User, Transaction, TransactionCategory, load_transactions_from_json

# Initialize Flask app and configure database
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app) 

# Basic Auth
USERNAME = 'admin'
PASSWORD = 'password123'

def check_auth 