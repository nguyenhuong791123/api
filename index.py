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
    # print('After Request !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    return response

lc = []
@app.before_request
def before_request():
    auth = request.authorization
    # print(auth)
    key = request.form.get('apikey', None)
    # print(key)
    if key is None:
        key = request.cookies.get('apikey', None)
        # print('cookies:' + str(key))

    global lc
    lc.append(len(lc) + 1)
    # print(lc)
    # print('Before Request !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    # if auth is None and key is None:
    #     return jsonify({"error": "Auth or API key is required !!!"}), 401

@app.route('/', methods=[ 'GET', 'POST' ])
def index():
    auth = request.authorization
    # print(auth)

    ag = UserAgent(request)
    return jsonify(ag.toJson()), 200

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

# ab -n 10000 -c 5 http://192.168.10.29:8085/api/rd
# オプション	意味
# -n 数値	テストで発行するリクエストの回数を数値で指定
# -c 数値	テストで同時に発行するリクエストの数を数値で指定
# -t 数値	サーバからのレスポンスの待ち時間（秒）を数値で指定
# -p ファイル名	サーバへ送信するファイルがある場合に指定
# -T コンテンツタイプ	サーバへ送信するコンテンツヘッダを指定
# -v 数値	指定した数値に応じた動作情報を表示
# -w	結果をHTMLで出力（出力をファイルに保存すればWebブラウザで表組みされたものが見られる）
# -x 属性	HTML出力のtableタグに属性を追加（BORDERなど）
# -y 属性	HTML出力のtrタグに属性を追加
# -z 属性	HTML出力のtdまたはthタグに属性を追加
# -C 'Cookie名称=値'	Cookie値を渡してテストする
# -A ユーザー名:パスワード	ベーシック認証が必要なコンテンツにテストする
# -P ユーザー名:パスワード	認証の必要なプロキシを通じてテストする
# -X プロキシサーバ名:ポート番号	プロキシ経由でリクエストする場合に指定
# -V	abのバージョン番号を表示
# -k	HTTP/1.1のKeepAliveを有効にしてテストする
# -h	abのヘルプを表示