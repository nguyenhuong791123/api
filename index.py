# -*- coding: UTF-8 -*-
import os
import sys
import json
from flask import Flask, session, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import ( JWTManager, get_jwt_identity, jwt_required, verify_jwt_in_request )

from utils.cm.resreq import load_apis
from utils.cm.agent import UserAgent
from utils.cm.dates import get_datetime
from utils.cm.utils import random_N_digits

from utils.db.auth.db import db
# from utils.db.auth.config import Config
# import utils.db.auth.config

app = Flask(__name__)
app.secret_key               = random_N_digits(24, False)
# app.config['JWT_SECRET_KEY'] = random_N_digits(16, False)
jwt = JWTManager(app)

CORS(app, supports_credentials=True)
load_apis(app)
passpaths = [ '/', '/auths', '/token', '/refresh', '/protected']

app.config.from_object('utils.db.auth.config.Config')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.after_request
def after_request(response):
    print('After Request !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    print(response.__dict__)
    return response

# lc = []
# curl -XGET -d "apikey={API-KEY}" http://192.168.56.53:7085/
# curl -H "Authorization: Bearer OAUTH-TOKEN" http://192.168.56.53:7085/
@app.before_request
def before_request():
    print('Before Request !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    ag = UserAgent(request)
    print(ag.to_json())
    # print(request.__dict__)
    # global lc
    # lc.append(len(lc) + 1)
    # print(lc)
    # if ag.api_token is None and ag.api_key is None and ag.path not in passpaths:
    # # if ag.api_token is None and ag.api_key is None and ag.path[:4] != '/api' and ag.path not in passpaths:
    #     return jsonify({"error": "OAUTH-TOKEN or API-KEY is Required !!!"}), 401

@app.route('/', methods=[ 'GET' ])
def index():
    ag = UserAgent(request)
    return jsonify(ag.to_json()), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8085)
