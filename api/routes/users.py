from flask import Blueprint, jsonify, request
from models import Users, db
from auth import auth

user_bp = Blueprint("users", __name__)


# READ ALL USERS

@user_bp.route("/users")
@auth.login_required
def get_users():
    users = Users.query.all()

    return jsonify([
        {
            "id": u.id,
            "full_name": u.full_name,
            "phone_number": u.phone_number,
            "balance": u.balance,
            "created_at": u.created_at,
            "updated_at": u.updated_at
        }
        for u in users
    ])


# GET USER BY ID

@user_bp.route("/users/<int:id>")
@auth.login_required
def get_user(id):
    user = Users.query.get_or_404(id)

    return jsonify({
        "id": user.id,
        "full_name": user.full_name,
        "phone_number": user.phone_number,
        "balance": user.balance,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }), 200

# CREATE NEW USER


@user_bp.route("/users", methods=["POST"])
@auth.login_required
def create_user():
    data = request.get_json()

    if not data or not data.get('full_name'):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        new_user = Users(
            full_name=data.get('full_name'),
            phone_number=data.get('phone_number'),
            balance=data.get('balance', 0.0)
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User created successfully",
            "user_id": new_user.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# UPDATE EXISTING USER

@user_bp.route("/users/<int:id>", methods=["PUT"])
@auth.login_required
def update_user(id):
    user = Users.query.get_or_404(id)
    data = request.get_json()

    try:
        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        if 'balance' in data:
            user.balance = data['balance']

        db.session.commit()

        return jsonify({"message": "User updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# DELETE EXISTING USER

@user_bp.route("/users/<int:id>", methods=["DELETE"])
@auth.login_required
def rm_user(id):
    user = Users.query.get_or_404(id)

    try:
        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": f"User {id} deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
