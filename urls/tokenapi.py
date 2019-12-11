
# -*- coding: UTF-8 -*-
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    JWTManager
    ,create_access_token
    ,create_refresh_token
    ,set_access_cookies
    ,set_refresh_cookies
    ,unset_jwt_cookies
    ,jwt_refresh_token_required
    ,get_jwt_identity
    ,jwt_required
)

from utils.cm.agent import UserAgent
from utils.cm.utils import is_empty
from utils.cm.dates import token_expires

app = Blueprint('tokenapi', __name__)

@app.route('/token', methods=['POST'])
def token():
    ag = UserAgent(request)
    if is_empty(ag.api_token) == False:
        return jsonify({ "access_token": ag.api_token }), 200

    key = None
    if is_empty(ag.auth) == False:
        key = ag.auth.username
    else:
        key = ag.api_key
    if is_empty(ag.auth):
        return jsonify({ "msg": "Bad username or password" }), 401

    access_token = create_access_token(identity=key, expires_delta=token_expires())
    refresh_token = create_refresh_token(identity=key, expires_delta=token_expires())
    ag.set_api_token(access_token)

    # Set the JWT cookies in the response
    resp = jsonify({ 'token': True })
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 200

@app.route('/refresh', methods=[ 'POST' ])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user, expires_delta=token_expires())
    resp = jsonify({ 'refresh': True })
    set_access_cookies(resp, access_token)
    return resp, 200

@app.route('/remove', methods=['POST'])
def logout():
    resp = jsonify({ 'token': True })
    unset_jwt_cookies(resp)
    return resp, 200

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({ 'protected': 'from {}'.format(get_jwt_identity()) }), 200
