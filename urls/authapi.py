
# -*- coding: UTF-8 -*-
import base64
import datetime
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from sqlalchemy import *
from sqlalchemy.orm import *

from utils.cm.utils import *
from utils.cm.system import *
from utils.cm.resreq import get_request_auth
from utils.db.engine.db import DB
from utils.db.auth.server import Server, ServerInfo
from utils.db.crm.company import Company, CompanyBasic, CompanyMode
from utils.db.crm.group import Group, GroupSchema
from utils.db.crm.user import User, UserSchema
from utils.db.crm.page import PageMenu, PageMenuSchema

app = Blueprint('authapi', __name__)

@app.route('/basic', methods=[ 'POST' ])
# @cross_origin()
def getBasic():
    auth = request.headers.get('authorization', None)
    result = {}
    if auth is not None and auth[:5] == 'Basic':
        auth = auth.replace('Basic ', '')
        auth = base64.b64decode(auth).decode('utf-8')
        auth = auth.split(':')

        conn = None
        try:
            conn = DB(get_common_db_info())
            cconn = Company(conn)
            basic = cconn.get_basic(auth[0], auth[1])
            result = CompanyBasic(many=False).dump(basic)
        except Exception as ex:
            result = str(ex)
        finally:
            if conn is not None:
                conn.close_session()

    return jsonify(result), 200

@app.route('/mode', methods=[ 'POST' ])
def getMode():
    result = None
    if request.json is not None:
        auth = request.json['uuid']
        if auth is None or len(auth) <= 0:
            return jsonify({ 'uuid': 'incorrect uuid'}), 200

        auth = base64.b64decode(auth).decode('utf-8')
        auth = auth.split(':')

        conn = None
        try:
            conn = DB(get_common_db_info())
            cconn = Company(conn)
            mode = cconn.get_basic(auth[0], auth[1])
            result = CompanyMode(many=False).dump(mode)
        except Exception as ex:
            result = { 'error': str(ex) }
            # result = str(ex)
        finally:
            if conn is not None:
                conn.close_session()

    return jsonify(result), 200

@app.route('/login', methods=[ 'POST' ])
def getLogin():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        u = request.json['username']
        if u is None or len(u) <= 0:
            return jsonify({ 'username': 'incorrect username'}), 200
        p = request.json['password']
        if p is None or len(u) <= 0:
            return jsonify({ 'password': 'incorrect password'}), 200

        conn = None
        try:
            conn = DB(get_common_db_info())
            uconn = User(conn)
            user = uconn.get_login(u, p)
            users = UserSchema(many=False).dump(user)
            result = { 'user': users }
        except Exception as ex:
            result = { 'error': str(ex) }
        finally:
            if conn is not None:
                conn.close_session()

    # print(result)
    return jsonify(result), 200

@app.route('/menus', methods=[ 'GET', 'POST' ])
def getMenus():
    auth = request.headers.get('authorization', None)

    print('Start ' + datetime.datetime.now().isoformat())
    result = None
    if request.json is not None:
        cId = request.json['cId']
        if cId is None or cId <= 0:
            return jsonify({ 'cId': 'incorrect company id'}), 200
        uId = request.json['uId']
        if uId is None or uId <= 0:
            return jsonify({ 'uId': 'incorrect user id'}), 200
        language = request.json['language']
        if is_empty(language) == True:
            return jsonify({ 'language': 'incorrect language'}), 200

        try:
            conn = DB(get_common_db_info())
            uconn = User(conn)
            sconn = Server(conn)
            server = sconn.get_server_by_type(cId, 0)
            if server is not None:
                user = uconn.get(uId)
                user = UserSchema(many=False).dump(user)

                server = ServerInfo(many=False).dump(server)
                sconn = DB(get_db_info(server))
                sconn = PageMenu(sconn)
                menu = sconn.get_menus(cId, language)
                menus = PageMenuSchema(many=True).dump(menu)
                # result = { 'menus': menus }
                result = { 'user': user, 'menus': menus }
            else:
                result = { 'error': 'Not Server Info!!!' }
        except Exception as ex:
            result = { 'error': str(ex) }
            # result = str(ex)
        finally:
            uconn.db.close_session()
            sconn.db.close_session()

    # print(result)
    print('End   ' + datetime.datetime.now().isoformat())
    return jsonify(result), 200
