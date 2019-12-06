# -*- coding: UTF-8 -*-
import os
from flask import Flask, request, render_template, redirect
from flask_cors import CORS
from flask_jwt_extended import ( JWTManager )

from utils.cm.language import parse_http_accept_language
from readme.readme import *

from auth import auth
from urls import fileapi

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

app.register_blueprint(auth.app)
app.register_blueprint(fileapi.app)

# @app.before_request
# def before_request():
#     current_user = get_jwt_identity()
#     print(current_user)
#     if current_user is None:
#         return jsonify({"error": "JWT authentication is required !!!"}), 401

@app.route('/', methods=[ 'GET', 'POST' ])
def index():
    auth = request.authorization
    # print(auth)
    return 'SC System !!!'

@app.route('/api', methods=[ 'GET', 'POST' ])
def api():
    auth = request.authorization
    # print(auth)
    return redirect("/api/rd")

@app.route('/api/<name>', methods=[ 'GET', 'POST' ])
def apimodule(name):
    auth = request.authorization
    # print(auth)

    l = parse_http_accept_language(request.headers.get('Accept-Language', ''))
    if l is None:
        l = 'ja'
    rds = read(name + '_' + l)
    return render_template('index.html', rds=rds)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8085)