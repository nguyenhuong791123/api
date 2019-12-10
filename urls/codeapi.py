# -*- coding: UTF-8 -*-
from flask import Blueprint, request, jsonify, make_response

from utils.cm.utils import is_exist
from utils.cm.resreq import make_response_zip
from utils.code.barqr import put_codes, get_codes

app = Blueprint('codeapi', __name__)

@app.route('/putcodes', methods=[ 'POST' ])
def putcodes():
    auth = {}
    codes = None
    result = []
    if request.method == 'POST':
        if request.json is not None:
            auth = request.json.get('auth')
            codes = request.json.get('codes')
        else:
            auth['code'] = request.form.get('code')
            auth['flag'] = request.form.get('flag')
            code = {}
            code['value'] = request.form.get('value')
            code['filename'] = request.form.get('filename')
            codes = []
            codes.append(code)

        if codes is None or len(codes) <= 0:
            obj = {}
            obj['name'] = None
            obj['data'] = 'ファイルデータは必須です。'
            result.append(obj)
            return jsonify(result), 200

    result = put_codes(auth, codes)
    if (is_exist(auth, 'flag') == False or auth['flag'] != 'json') and result is not None:
        return make_response_zip(result, True)
    else:
        if result is None:
            result = { 'msg': 'Json Data is error !!!' }
        return jsonify(result), 200

@app.route('/getcodes', methods=[ 'POST' ])
def getcodes():
    auth = {}
    codes = None
    result = []
    if request.method == 'POST':
        files = request.files.getlist('file')
        if request.json is not None:
            auth = request.json.get('auth')
            auth['flag'] = 'json'
            files = request.json.get('files')
        else:
            auth['code'] = request.form.get('code')

        if files is None or len(files) <= 0:
            obj = {}
            obj['name'] = None
            obj['data'] = 'ファイルデータは必須です。'
            result.append(obj)
            return jsonify(result), 200

    result = get_codes(auth, files)
    return jsonify(result), 200