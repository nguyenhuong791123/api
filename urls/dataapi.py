
# -*- coding: UTF-8 -*-
from flask import Blueprint, request, jsonify

from utils.cm.resreq import get_request_auth
from service.data import *
from utils.cm.utils import *

app = Blueprint('dataapi', __name__)

@app.route('/saveData', methods=[ 'POST' ])
def saveData():
    auth = get_request_auth()
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

        result = getServiceSaveData(page, cId, uId)
    return jsonify(result), 200

@app.route('/updateData', methods=[ 'POST' ])
def updateData():
    auth = get_request_auth()
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

        result = getServiceUpdateData(page, cId, uId)
    return jsonify(result), 200