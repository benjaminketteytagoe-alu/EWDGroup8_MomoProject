from flask import Blueprint, jsonify, request
from models import Transactions, db
from sqlalchemy.sql import func
from auth import auth

transactions_bp = Blueprint("transactions", __name__)


# Read all transactions
@transactions_bp.route("/transactions")
@auth.login_required
def get_transactions():
    transactions = Transactions.query.all()

    if not transactions:
        return jsonify({"error": "Transactions not found"}), 404

    return jsonify([{
        "Txid": t.id,
        "user_id": t.user_id,
        "category_id": t.category_id,
        "recepient_sender": t.recepient_sender,
        "amount": t.amount,
        "fee": t.fee,
        "new_balance": t.new_balance,
        "Tx_date": t.date
    } for t in transactions])


# Read transaction by id
@transactions_bp.route("/transactions/<int:id>")
@auth.login_required
def get_transaction(id):
    transaction = Transactions.query.get_or_404(id)

    return jsonify({
        "Txid": transaction.id,
        "user_id": transaction.user_id,
        "category_id": transaction.category_id,
        "recepient_sender": transaction.recepient_sender,
        "amount": transaction.amount,
        "fee": transaction.fee,
        "new_balance": transaction.new_balance,
        "Tx_date": transaction.date
    })


# Post transaction
@transactions_bp.route("/transactions", methods=["POST"])
@auth.login_required
def create_transaction():
    data = request.get_json()
    required_fields = ["user_id", "category_id", "recepient_sender", "amount"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    try:
        transaction = Transactions(
            user_id=data["user_id"],
            category_id=data["category_id"],
            transaction_type=data.get("transaction_type"),
            recepient_sender=data["recepient_sender"],
            amount=data["amount"],
            fee=data.get("fee", 0.00),
            new_balance=data.get("new_balance"),
            date=func.now()  # ✅ VALID datetime
        )

        db.session.add(transaction)
        db.session.commit()

        return jsonify({
            "message": "Transaction created successfully",
            "transaction_id": transaction.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Update transaction
@transactions_bp.route("/transactions/<int:id>", methods=["PUT"])
@auth.login_required
def update_transaction(id):
    transaction = Transactions.query.get_or_404(id)
    data = request.get_json()

    try:
        # Only update fields that are present in the request
        if "user_id" in data:
            transaction.user_id = data["user_id"]

        if "category_id" in data:
            transaction.category_id = data["category_id"]

        if "transaction_type" in data:
            transaction.transaction_type = data["transaction_type"]

        if "recepient_sender" in data:
            transaction.recepient_sender = data["recepient_sender"]

        if "amount" in data:
            transaction.amount = data["amount"]

        if "fee" in data:
            transaction.fee = data["fee"]

        if "new_balance" in data:
            transaction.new_balance = data["new_balance"]

        if "date" in data:
            transaction.date = data["date"]

        db.session.commit()

        return jsonify({
            "message": "Transaction updated successfully",
            "transaction_id": transaction.id
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Delete a transaction by id
@transactions_bp.route("/transactions/<int:id>", methods=["DELETE"])
@auth.login_required
def rm_transaction(id):
    transaction = Transactions.query.get_or_404(id)

    try:
        db.session.delete(id)
        db.session.commit()

        return jsonify({
            "message": f"Transaction{id} deleted successful"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": str(e)
        }), 400
