from sqlalchemy.sql import func
from db import db


# Shared attributes
class Base:
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )


# users entity schema
class Users(Base, db.Model):
    __tablename__ = "users"

    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    balance = db.Column(db.Numeric(15, 2), default=0.0)


# transactions_category entity schema
class TransactionCategory(Base, db.Model):
    __tablename__ = "transaction_category"

    category_name = db.Column(db.String(50))
    sub_type = db.Column(db.String(50))
    description = db.Column(db.Text)


# transactions entity schema
class Transactions(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.String(50))
    recepient_sender = db.Column(db.String(100))
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    fee = db.Column(db.Numeric(10, 2), default=0.00)
    new_balance = db.Column(db.Numeric(15, 2))
    date = db.Column(db.DateTime, server_default=func.now())
