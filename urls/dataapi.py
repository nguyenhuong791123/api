
# -*- coding: UTF-8 -*-
from flask import Blueprint, request, jsonify

from utils.cm.resreq import get_request_auth

app = Blueprint('dataapi', __name__)

@app.route('/select', methods=[ 'GET' ])
def getSelect():
    auth = get_request_auth()
    print(request.__dict__)
    return jsonify(auth), 200

@app.route('/insert', methods=[ 'POST' ])
def getInsert():
    auth = get_request_auth()
    return jsonify({ 'auth': auth }), 200

