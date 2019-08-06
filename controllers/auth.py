from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
app = Blueprint('auth', __name__)

@app.route("/auth")
def auth():
    params = request.args
    print(params)
    access_token = create_access_token(identity='huongnv')
    return "Hello " + access_token + "from action.py"