# -*- coding: UTF-8 -*-
import json
import copy
import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy import *
from sqlalchemy.orm import *

from utils.cm.utils import *
from utils.cm.system import *
from utils.cm.resreq import get_request_auth
from utils.db.engine.db import DB
from utils.db.auth.server import Server, ServerInfo
from utils.db.crm.options import Options, OptionsSchema, OptionPatitions, OptionPatitionsSchema

app = Blueprint('searchapi', __name__)

@app.route('/search', methods=[ 'POST' ])
def getLists():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        cId = request.json['cId']
        if cId is None or cId <= 0:
            return jsonify({ 'cId': 'incorrect company id'}), 200
        uId = request.json['uId']
        if uId is None or uId <= 0:
            return jsonify({ 'uId': 'incorrect user id'}), 200
        pId = request.json['pId']
        if pId is None or pId <= 0:
            return jsonify({ 'pId': 'incorrect page id'}), 200

        conn = None
        try:
            conn = DB(get_common_db_info())
            conn = Server(conn)
            server = conn.get_server_by_type(cId, 0)
            if server is not None:
                server = ServerInfo(many=False).dump(server)
                conn = DB(get_db_info(server))
                pconn = OptionPatitions(conn)
                pconn = pconn.get_option_patitions(cId, patitions)
                result = OptionPatitionsSchema(many=True).dump(pconn)

                if result:
                    result = result[0]['patitions']
            else:
                result = { 'error': 'Not Server Info!!!'}

        except Exception as ex:
            result = { 'error': str(ex) }
        finally:
            if conn is not None:
                conn.close_session()

    return jsonify(result), 200

@app.route('/colums', methods=[ 'POST' ])
def getColums():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        cId = request.json['cId']
        if cId is None or cId <= 0:
            return jsonify({ 'cId': 'incorrect company id'}), 200
        pId = request.json['pId']
        if pId is None or pId <= 0:
            return jsonify({ 'pId': 'incorrect page id'}), 200
        language = request.json['language']
        if is_empty(language) == True:
            return jsonify({ 'language': 'incorrect language'}), 200

        conn = None
        try:
            conn = DB(get_common_db_info())
            conn = Server(conn)
            server = conn.get_server_by_type(cId, 0)
            if server is not None:
                server = ServerInfo(many=False).dump(server)
                conn = DB(get_db_info(server))
                sconn = PageMenu(conn)
                menu = sconn.get_colums(cId, pId, language)
                menus = PageMenuSchema(many=False).dump(menu)

            else:
                result = { 'error': 'Not Server Info!!!'}

        except Exception as ex:
            result = { 'error': str(ex) }
        finally:
            if conn is not None:
                conn.close_session()

    return jsonify(result), 200