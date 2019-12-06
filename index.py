# -*- coding: UTF-8 -*-
import os
import json
from flask import Flask, request, render_template, redirect, jsonify
from flask_cors import CORS
# from flask_jwt_extended import ( JWTManager )

from utils.cm.agent import parse_http_accept_language, UserAgent
from utils.cm.dates import get_datetime
from readme.readme import *

from auth import auth
from urls import fileapi

app = Flask(__name__)
CORS(app, supports_credentials=True)
# app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
# jwt = JWTManager(app)

app.register_blueprint(auth.app)
app.register_blueprint(fileapi.app)

@app.after_request
def after_request(response):
    print('After Request !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    return response

# lc = []
@app.before_request
def before_request():
    ag = UserAgent(request)
    print(ag.toJson())
    print(request.headers.__dict__)
    print(request.headers.get('HTTP_AUTHORIZATION', ''))
    # global lc
    # lc.append(len(lc) + 1)
    # print(lc)
    print('Before Request !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    if ag.auth_api_key is None and ag.path[:4] != '/api' and ag.path != '/':
        return jsonify({"error": "Auth Info or API Key is Required !!!"}), 401

@app.route('/', methods=[ 'GET' ])
def index():
    ag = UserAgent(request)
    return jsonify(ag.toJson()), 200

@app.route('/api', methods=[ 'GET' ])
def api():
    return redirect("/api/rd")

@app.route('/api/<name>', methods=[ 'GET' ])
def apis(name):
    l = parse_http_accept_language(request.headers.get('Accept-Language', ''))
    if l is None:
        l = 'ja'
    rds = readme_read(name + '_' + l)
    return render_template('index.html', rds=rds)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8085)
