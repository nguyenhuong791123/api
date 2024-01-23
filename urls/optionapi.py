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

app = Blueprint('optionapi', __name__)

@app.route('/options', methods=[ 'POST' ])
def getOptions():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        cId = request.json['cId']
        if cId is None or cId <= 0:
            return jsonify({ 'cId': 'incorrect company id'}), 200
        uId = request.json['uId']
        if uId is None or uId <= 0:
            return jsonify({ 'uId': 'incorrect user id'}), 200
        patitions = None
        if is_exist(request.json, 'patitions') == True:
            patitions = request.json['patitions']
        print(patitions)

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
                
                for p in patitions:
                    if p == 'city_info':
                        cconn = OptionPatitions(conn)
                        cconn = cconn.get_option_citys()
                        citys = OptionPatitionsSchema(many=True).dump(cconn)
                        if citys:
                            citys = { 'option_name': p, 'options': citys[0]['patitions'] }
                            if result:
                                result.append(citys)
                            else:
                                result = [citys]

                    if p == 'company_info':
                        ciconn = OptionPatitions(conn)
                        ciconn = ciconn.get_option_companys()
                        companys = OptionPatitionsSchema(many=True).dump(ciconn)
                        if companys:
                            companys = { 'option_name': p, 'options': companys[0]['patitions'] }
                            if result:
                                result.append(companys)
                            else:
                                result = [companys]

                    if p == 'group_info':
                        giconn = OptionPatitions(conn)
                        giconn = giconn.get_option_groups()
                        groups = OptionPatitionsSchema(many=True).dump(giconn)
                        if groups:
                            groups = { 'option_name': p, 'options': groups[0]['patitions'] }
                            if result:
                                result.append(groups)
                            else:
                                result = [groups]

                    if p == 'users_info':
                        uiconn = OptionPatitions(conn)
                        uiconn = uiconn.get_option_users(None)
                        users = OptionPatitionsSchema(many=True).dump(uiconn)
                        if users:
                            users = { 'option_name': p, 'options': users[0]['patitions'] }
                            if result:
                                result.append(users)
                            else:
                                result = [users]

            else:
                result = { 'error': 'Not Server Info!!!'}

        except Exception as ex:
            result = { 'error': str(ex) }
        finally:
            if conn is not None:
                conn.close_session()

    return jsonify(result), 200

@app.route('/distinctPatitions', methods=[ 'POST' ])
def getDistinctPatitions():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        cId = request.json['cId']
        if cId is None or cId <= 0:
            return jsonify({ 'cId': 'incorrect company id'}), 200
        uId = request.json['uId']
        if uId is None or uId <= 0:
            return jsonify({ 'uId': 'incorrect user id'}), 200

        conn = None
        try:
            conn = DB(get_common_db_info())
            conn = Server(conn)
            server = conn.get_server_by_type(cId, 0)
            if server is not None:
                server = ServerInfo(many=False).dump(server)
                conn = DB(get_db_info(server))
                pconn = OptionPatitions(conn)
                pconn = pconn.get_distinct_patitions(cId)
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

@app.route('/patitions', methods=[ 'POST' ])
def getPatitions():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        cId = request.json['cId']
        if cId is None or cId <= 0:
            return jsonify({ 'cId': 'incorrect company id'}), 200
        uId = request.json['uId']
        if uId is None or uId <= 0:
            return jsonify({ 'uId': 'incorrect user id'}), 200
        language = request.json['language']
        if language is None or len(language) <= 0:
            return jsonify({ 'language': 'incorrect patition'}), 200

        conn = None
        try:
            conn = DB(get_common_db_info())
            conn = Server(conn)
            server = conn.get_server_by_type(cId, 0)
            if server is not None:
                server = ServerInfo(many=False).dump(server)
                conn = DB(get_db_info(server))
                pconn = OptionPatitions(conn)
                pconn = pconn.get_patitions(cId, language)
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

@app.route('/optionPatition', methods=[ 'POST' ])
def getOptionByPatition():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        cId = request.json.get('cId', None)
        if cId is None or cId <= 0:
            return jsonify({ 'cId': 'incorrect company id'}), 200
        uId = request.json.get('uId', None)
        if uId is None or uId <= 0:
            return jsonify({ 'uId': 'incorrect user id'}), 200
        patition = request.json.get('patition', None)
        if patition is None or len(patition) <= 0:
            return jsonify({ 'patition': 'incorrect patition'}), 200
        gIds = request.json.get('gIds', None)

        conn = None
        try:
            conn = DB(get_common_db_info())
            conn = Server(conn)
            server = conn.get_server_by_type(cId, 0)
            if server is not None:
                server = ServerInfo(many=False).dump(server)
                conn = DB(get_db_info(server))
                if patition == 'group_info':
                    giconn = OptionPatitions(conn)
                    giconn = giconn.get_option_groups()
                    result = OptionPatitionsSchema(many=True).dump(giconn)
                    if result:
                        result = result[0]['patitions']
                elif patition == 'users_info':
                    uiconn = OptionPatitions(conn)
                    uiconn = uiconn.get_option_users(gIds)
                    result = OptionPatitionsSchema(many=True).dump(uiconn)
                    if result:
                        result = result[0]['patitions']
                else:
                    pconn = Options(conn)
                    pconn = pconn.get_options_by_patition(cId, patition)
                    result = OptionsSchema(many=True).dump(pconn)

            else:
                result = { 'error': 'Not Server Info!!!'}

        except Exception as ex:
            result = { 'error': str(ex) }
        finally:
            if conn is not None:
                conn.close_session()

    return jsonify(result), 200

@app.route('/optionPatitions', methods=[ 'POST' ])
def getOptionByPatitions():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        cId = request.json['cId']
        if cId is None or cId <= 0:
            return jsonify({ 'cId': 'incorrect company id'}), 200
        uId = request.json['uId']
        if uId is None or uId <= 0:
            return jsonify({ 'uId': 'incorrect user id'}), 200
        patitions = request.json['patitions']
        if patitions is None or len(patitions) <= 0:
            return jsonify({ 'patitions': 'incorrect patition'}), 200

        conn = None
        try:
            conn = DB(get_common_db_info())
            conn = Server(conn)
            server = conn.get_server_by_type(cId, 0)
            if server is not None:
                server = ServerInfo(many=False).dump(server)
                conn = DB(get_db_info(server))
                pconn = Options(conn)
                pconn = pconn.get_options_by_patitions(cId, patitions)
                result = OptionsSchema(many=True).dump(pconn)

            else:
                result = { 'error': 'Not Server Info!!!'}

        except Exception as ex:
            result = { 'error': str(ex) }
        finally:
            if conn is not None:
                conn.close_session()

    return jsonify(result), 200