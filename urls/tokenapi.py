
# -*- coding: UTF-8 -*-
from flask import Blueprint, request, jsonify
from flask_jwt_extended import ( JWTManager, create_access_token, jwt_refresh_token_required, create_refresh_token, get_jwt_identity, jwt_required )

from utils.cm.agent import UserAgent
from utils.cm.utils import is_empty

app = Blueprint('tokenapi', __name__)

@app.route('/auth', methods=['POST'])
def auth():
    ag = UserAgent(request)
    if is_empty(ag.set_api_token) == False:
        return jsonify({ "access_token": ag.set_api_token }), 200

    key = None
    if is_empty(ag.auth) == False:
        # auth = ag.auth
        key = ag.auth
        # username = auth.username
        # password = auth.password
    else:
        key = ag.api_key
    if is_empty(ag.auth):
        return jsonify({ "msg": "Bad username or password" }), 401

    ret = {
        'access_token': create_access_token(identity=key),
        'refresh_token': create_refresh_token(identity=key)
    }
    return jsonify(ret), 200

@app.route('/refresh', methods=[ 'POST' ])
@jwt_refresh_token_required
def refresh():
    return jsonify({ 'access_token': create_access_token(identity=get_jwt_identity()) }), 200


@app.route('/protected', methods=[ 'GET' ])
@jwt_required
def protected():
    return jsonify(logged_in_as=get_jwt_identity()), 200
