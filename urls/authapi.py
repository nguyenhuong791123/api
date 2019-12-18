
# -*- coding: UTF-8 -*-
from flask import Blueprint, request, jsonify
from sqlalchemy import *
from sqlalchemy.orm import *

from utils.db.auth.user import User, UserSchema

app = Blueprint('authapi', __name__)

@app.route('/getauths', methods=[ 'GET' ])
def getUserList():
    result = False
    try:
        users = User.get_user_list()
        result = UserSchema(many=True).dump(users)
    except Exception as ex:
        result = str(ex)

    return jsonify(result), 200

@app.route('/isauth', methods=[ 'POST' ])
def getUserIsExist():
    auth = get_request_auth()
    if auth is None:
        obj = {}
        obj['msg'] = 'ユーザー「メール、パスワード」は必須です。'
        result.append(obj)
        return jsonify(result), 200

    isExist = False
    try:
        isExist = User.is_exist(auth)
    except Exception as ex:
        isExist = str(ex)

    return jsonify({ 'exist': isExist}), 200

@app.route('/putauth', methods=[ 'POST' ])
def registUser():
    auth = get_request_auth()
    if auth is None:
        obj = {}
        obj['msg'] = 'ユーザー「メール、パスワード」は必須です。'
        result.append(obj)
        return jsonify(result), 200

    result = False
    try:
        result = User.regist_user(auth)
    except Exception as ex:
        result = str(ex)

    return jsonify(result), 200

def get_request_auth():
    if request.method == 'POST':
        if request.json is not None:
            auth = request.json.get('auth')
        else:
            auth = {}
            auth['email'] = request.form.get('email')
            auth['password'] = request.form.get('password')

    return auth