# -*- coding: UTF-8 -*-
import os
import sys
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.cm.resreq import load_apis
from utils.cm.agent import UserAgent
from utils.cm.dates import get_datetime

app = Flask(__name__)
CORS(app, supports_credentials=True)
load_apis(app)

@app.after_request
def after_request(response):
    print('After Request !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    return response

# lc = []
# curl -XGET -d "apikey={API-KEY}" http://192.168.56.53:7085/
# curl -H "Authorization: token OAUTH-TOKEN" http://192.168.56.53:7085/
@app.before_request
def before_request():
    print('Before Request !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    ag = UserAgent(request)
    print(ag.to_json())
    # global lc
    # lc.append(len(lc) + 1)
    # print(lc)
    if ag.auth_api_key is None and ag.path[:4] != '/api' and ag.path != '/':
        return jsonify({"error": "Auth Info or API Key is Required !!!"}), 401

@app.route('/', methods=[ 'GET' ])
def index():
    ag = UserAgent(request)
    return jsonify(ag.to_json()), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8085)
