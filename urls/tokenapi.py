
# -*- coding: UTF-8 -*-
import json
from flask import Blueprint, session, request, jsonify
# from flask_cors import cross_origin
from flask_jwt_extended import (
    JWTManager
    ,create_access_token
    ,jwt_refresh_token_required
    ,get_jwt_identity
    ,jwt_required
)

from utils.cm.agent import UserAgent
from utils.cm.utils import is_empty
from utils.cm.dates import token_expires
from utils.db.auth.auth import check_auth
from utils.db.sql import sql_sel

app = Blueprint('tokenapi', __name__)

@app.route('/token', methods=[ 'GET', 'POST' ])
# @cross_origin()
def token():
    print(request.__dict__)
    ag = UserAgent(request)
    print(ag.__dict__)
    if is_empty(ag.api_token) == False:
        return jsonify({ "access_token": ag.api_token }), 200
    password = None
    if request.method == 'POST':
        if request.json is not None:
            password = request.json.get('password')
        else:
            password = request.form.get('password')

    key = check_auth(ag.api_key, ag.username, password)
    if is_empty(key):
        return jsonify({ "msg": "Bad username or password" }), 401

    access_token = create_access_token(identity=key, expires_delta=token_expires())
    ag.set_api_token(access_token)
    # session['SessionUser'] = ag.set_session_user()
    # print(session.get('SessionUser'))

    # Set the JWT cookies in the response
    print(access_token)
    return jsonify({ 'access_token': access_token }), 200

@app.route('/refresh', methods=[ 'POST' ])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    return jsonify({ 'refresh': create_access_token(identity=current_user, expires_delta=token_expires()) }), 200

@app.route('/protected', methods=[ 'GET' ])
@jwt_required
def protected():
    return jsonify({ 'protected': 'from {}'.format(get_jwt_identity()) }), 200
