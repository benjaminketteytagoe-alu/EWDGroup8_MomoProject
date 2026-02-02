from flask import Blueprint, request, jsonify
from functools import wraps

ADMIN_USERNAME ="admin"
ADMIN_PASSWORD ="admin123"

auth_bp = Blueprint('auth', __name__)

def check_auth(username, password):
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD
def authenticate():
    message = {'message': "Authentication required."}
    resp = jsonify(message)
    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
    return resp
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
@auth_bp.route('/protected')
@requires_auth
def protected():
    return jsonify({'message': 'This is a protected endpoint.'})
