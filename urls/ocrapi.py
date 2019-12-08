# -*- coding: UTF-8 -*-
from flask import Blueprint, Flask, request, render_template, jsonify, make_response

from utils.ocr.ocr import img_to_text

app = Blueprint('ocrapi', __name__)

@app.route('/ocr', methods=[ 'GET', 'POST'])
def ocr():
    result = {}
    if request.method == 'POST':
        files = request.files.getlist('file')
        if request.json is not None and (files is None or len(files) <= 0):
            files = request.json.get('files')

        if files is not None and len(files) > 0:
            result = img_to_text(files, None, None)

    return jsonify(result), 200