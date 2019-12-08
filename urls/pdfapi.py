# -*- coding: UTF-8 -*-
from flask import Blueprint, Flask, jsonify, request, make_response
import pdfkit
from utils.cm.utils import is_exist
from utils.cm.files import delete_dir
from utils.pdf.pdfkits import *

app = Blueprint('pdfapi', __name__)

# curl -v -H "Content-type: application/json" -X POST http://192.168.10.126:8084/pdf
# curl -XPOST -F file=@index.html -F file=@index.css -F file=@style.css http://192.168.10.126:8084/pdf > test.pdf
@app.route('/pdf', methods=[ 'GET', 'POST' ])
def pdf():
    obj = {}
    if request.method == 'POST':
        if request.json is not None:
            if is_json(request.json):
                obj = request.json
        else:
            obj = get_forms(request)

    # options = {}
    # options['orientation'] = 'Portrait'
    # obj['options'] = options
    result = get_pdf(obj)
    if result is not None and is_exist(result, 'msg') == False:
        response = make_response()
        filename = result['filename']
        fullpath = result['path'] + '/' + filename
        response.data = open(fullpath, 'rb').read()
        response.headers['Content-Disposition'] = "attachment; filename=" + filename
        response.mimetype = 'application/pdf'

        delete_dir(result['path'])
        return response
    else:
        if result is None:
            result = { 'msg': 'Json Data is error !!!' }
        return jsonify(result), 200
