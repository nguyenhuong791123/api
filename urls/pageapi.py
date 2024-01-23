# -*- coding: UTF-8 -*-
import json
import copy
import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy import *
from sqlalchemy.orm import *

from service.page import *
from utils.cm.utils import *

app = Blueprint('pageapi', __name__)

@app.route('/setPage', methods=[ 'POST' ])
def setPage():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        page = request.json['page']
        if page is None:
            return jsonify({ 'error': 'incorrect page info'}), 200
        cId = request.json['cId']
        if is_integer(cId) == False:
            return jsonify({ 'error': 'incorrect company id'}), 200
        uId = request.json['uId']
        if is_integer(uId) == False:
            return jsonify({ 'error': 'incorrect user id'}), 200

        result = setServicePage(page, cId, uId)

    return jsonify(result), 200

@app.route('/getPage', methods=[ 'POST' ])
def getPage():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        cId = request.json['cId']
        if is_integer(cId) == False:
            return jsonify({ 'error': 'incorrect company id'}), 200
        pId = request.json['pId']
        if is_integer(pId) == False:
            return jsonify({ 'error': 'incorrect page id'}), 200
        language = request.json['language']
        if is_empty(language) == True:
            return jsonify({ 'error': 'incorrect language'}), 200

        result = getServicePage(cId, pId, language, False)
    return jsonify(result), 200

@app.route('/getEditCustomizePage', methods=[ 'POST' ])
def getEditCustomizePage():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        cId = request.json['cId']
        if is_integer(cId) == False:
            return jsonify({ 'error': 'incorrect company id'}), 200
        pId = request.json['pId']
        if is_integer(pId) == False:
            return jsonify({ 'error': 'incorrect page id'}), 200
        language = request.json['language']
        if is_empty(language) == True:
            return jsonify({ 'error': 'incorrect language'}), 200

        result = getServicePage(cId, pId, language, True)
    return jsonify(result), 200

@app.route('/setGroupPage', methods=[ 'POST' ])
def setGroupPage():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        page = request.json['page']
        if page is None:
            return jsonify({ 'error': 'incorrect page info'}), 200
        cId = request.json['cId']
        if is_integer(cId) == False:
            return jsonify({ 'error': 'incorrect company id'}), 200
        uId = request.json['uId']
        if is_integer(uId) == False:
            return jsonify({ 'error': 'incorrect user id'}), 200

        result = setServiceGroupPage(page, cId, uId)
    return jsonify(result), 200

@app.route('/updatePage', methods=[ 'POST' ])
def updatePage():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        page = request.json['page']
        if page is None:
            return jsonify({ 'error': 'incorrect page info'}), 200
        cId = request.json['cId']
        if is_integer(cId) == False:
            return jsonify({ 'error': 'incorrect company id'}), 200
        uId = request.json['uId']
        if is_integer(uId) == False:
            return jsonify({ 'error': 'incorrect user id'}), 200

        result = updateServicePage(page, cId)
    return jsonify(result), 200

@app.route('/updatePages', methods=[ 'POST' ])
def updatePages():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        pages = request.json['pages']
        if pages is None:
            return jsonify({ 'error': 'incorrect pages info'}), 200
        cId = request.json['cId']
        if is_integer(cId) == False:
            return jsonify({ 'error': 'incorrect company id'}), 200
        uId = request.json['uId']
        if is_integer(uId) == False:
            return jsonify({ 'error': 'incorrect user id'}), 200

        result = updateServicePages(pages, cId)
    return jsonify(result), 200

@app.route('/deletePage', methods=[ 'POST' ])
def deletePage():
    auth = request.headers.get('authorization', None)

    result = None
    if request.json is not None:
        page = request.json['page']
        if page is None:
            return jsonify({ 'error': 'incorrect page info'}), 200
        cId = request.json['cId']
        if is_integer(cId) == False:
            return jsonify({ 'error': 'incorrect company id'}), 200
        uId = request.json['uId']
        if is_integer(uId) == False:
            return jsonify({ 'error': 'incorrect user id'}), 200

        result = deleteServicePage(page, cId)
    return jsonify(result), 200

# @app.route('/savePage', methods=[ 'POST' ])
# def savePage():
#     auth = request.headers.get('authorization', None)

#     result = None
#     if request.json is not None:
#         page = request.json['page']
#         if page is None:
#             return jsonify({ 'error': 'incorrect page info'}), 200
#         cId = request.json['cId']
#         if is_integer(cId) == False:
#             return jsonify({ 'error': 'incorrect company id'}), 200
#         uId = request.json['uId']
#         if is_integer(uId) == False:
#             return jsonify({ 'error': 'incorrect user id'}), 200

#         result = saveServicePage(page, cId, uId)
#     return jsonify(result), 200