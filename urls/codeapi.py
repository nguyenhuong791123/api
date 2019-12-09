# -*- coding: UTF-8 -*-
from flask import Blueprint, request, jsonify, make_response

from utils.cm.files import delete_dir
from utils.code.barqr import get_codes

app = Blueprint('codeapi', __name__)

@app.route('/getcodes', methods=[ 'POST' ])
def getcodes():
    codes = None
    result = []
    if request.method == 'POST':
        if request.json is not None:
            codes = request.json.get('codes')

        if codes is None or len(codes) <= 0:
            obj = {}
            obj['name'] = None
            obj['data'] = 'ファイルデータは必須です。'
            result.append(obj)
            return jsonify(result), 200

    result = get_codes(codes)
    return jsonify(result), 200