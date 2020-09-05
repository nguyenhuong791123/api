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
from utils.db.crm.page import PageMenu, PageMenuSchema

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

@app.route('/columns', methods=[ 'POST' ])
def getColumns():
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

@app.route('/datas', methods=[ 'POST' ])
def getDatas():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        cId = request.json['cId']
        if cId is None or cId <= 0:
            return jsonify({ 'cId': 'incorrect company id'}), 200
        uId = request.json['uId']
        if uId is None or uId <= 0:
            return jsonify({ 'uId': 'incorrect user id'}), 200
        page = request.json['page']
        if is_empty(page) == True or is_exist(page, 'page_key') == False:
            return jsonify({ 'page': 'incorrect page info'}), 200
        schema = page['page_key']
        columns = page['columns']
        idSeq = page['page_id_seq']
        if is_empty(columns) == True:
            return jsonify({ 'columns': 'incorrect columns info'}), 200
        reference = None
        if is_exist(page, 'reference') == True:
            reference = page['reference']
        where = None
        if is_exist(page, 'where') == True:
            where = page['where']

        conn = None
        try:
            conn = DB(get_common_db_info())
            conn = Server(conn)
            server = conn.get_server_by_type(cId, 0)
            if server is not None:
                server = ServerInfo(many=False).dump(server)
                conn = DB(get_db_info(server))
                sconn = PageMenu(conn)
                datas = sconn.get_datas(schema, columns, idSeq, where, reference)
                if datas:
                    result = json.dumps([(dict(row.items())) for row in datas])
                    result = json.loads(result)[0]['result']

            else:
                result = { 'error': 'Not Server Info!!!'}

        except Exception as ex:
            result = { 'error': str(ex) }
        finally:
            if conn is not None:
                conn.close_session()

    return jsonify(result), 200