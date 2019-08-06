from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
app = Blueprint('auth', __name__)

@app.route("/auth", methods=['POST'])
def auth():
    params = request.json
    print(params)
    user_token = create_access_token(identity=params['username'])
    res = { "sucess": "true", "err": "", "token": user_token }
    return jsonify(res)

@app.route("/user", methods=['GET'])
def access_user():
    params = request.args
    print(params)
    is_user = get_jwt_identity()
    return "Hello " + is_user + "from action.py"