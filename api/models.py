# This file defines the database models for the Momo Project using SQLAlchemy ORM.

import os
import json 
from flask_sqlalchemy import SQLAlchemy

# database instance
db = SQLAlchemy()

# Base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the database 
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://group8:eLeKcEaFiN_2026!@localhost:3306/momo_erd'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

#JSON file
JSON_FILE = os.path.join(basedir, 'all_transactions.json')

def load_transactions_from_json():
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
            return data.get('transactions', [])
    except json.JSONDecodeError:
        return []

# Define database models

class User(db.Model):
    __tablename__ = "Users"
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    balance = db.Column(db.Numeric(15,2), default=0.00)


class TransactionCategory(db.Model):
    __tablename__ = "Transaction_Categories"
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), unique=True, nullable=False)
    sub_type = db.Column(db.String(50))
    description = db.Column(db.Text)


class Transaction(db.Model):
    __tablename__ = "Transactions"
    transaction_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("Transaction_Categories.category_id"))
    transaction_type = db.Column(db.String(50))
    recepient_sender = db.Column(db.String(100))
    amount = db.Column(db.Numeric(15,2))
    fee = db.Column(db.Numeric(10,2))
    new_balance = db.Column(db.Numeric(15,2))
    date = db.Column(db.String(50))

    
