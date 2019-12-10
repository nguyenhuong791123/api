# -*- coding: UTF-8 -*-
from flask import Blueprint, request, jsonify, make_response
# from flask_jwt_extended import ( JWTManager, jwt_required, create_access_token, get_jwt_identity )

from utils.server import default_server, Mode
from utils.cm.files import delete_dir
from utils.cm.resreq import make_response_zip
from utils.file.sftp import transport_sftp, download_sftp
from utils.file.ftp import transport_ftp, download_ftp
from utils.file.scp import transport_scp, download_scp
from utils.file.s3 import transport_s3, download_s3

app = Blueprint('fileapi', __name__)

@app.route('/putfiles', methods=[ 'POST' ])
def putfiles():
    auth = {}
    auth['flag'] = 'file'
    auth['mode'] = Mode().s3
    print(auth)
    auth = default_server(auth)
    print(auth)

    files = None
    result = []
    if request.method == 'POST':
        files = request.files.getlist('file')
        if request.json is not None and (files is None or len(files) <= 0):
            files = request.json.get('files')
            auth['flag'] = 'json'

        # print(files)
        if files is None or len(files) <= 0:
            obj = {}
            obj['name'] = None
            obj['data'] = 'ファイルデータは必須です。'
            result.append(obj)
            return jsonify(result), 200

    m = Mode()
    mode = auth['mode']
    if mode == m.sftp:
        result = transport_sftp(auth, files)
    elif mode == m.ftp:
        result = transport_ftp(auth, files)
    elif mode == m.scp:
        result = transport_scp(auth, files)
    elif mode == m.s3:
        result = transport_s3(auth, files)

    return jsonify(result), 200

@app.route('/getfiles', methods=[ 'POST' ])
def getfiles():
    auth = {}
    auth['flag'] = 'file'
    auth['mode'] = Mode().sftp
    print(auth)
    auth = default_server(auth)
    print(auth)

    files = None
    if request.method == 'POST':
        if request.json is not None and (files is None or len(files) <= 0):
            auth['flag'] = request.json.get('flag')
            auth['zip'] = request.json.get('zip')
            auth['zippw'] = request.json.get('zippw')
            files = request.json.get('files')
        else:
            if is_none(request.form.get('flag')) == False:
                auth['flag'] = request.form.get('flag')
            auth['zip'] = request.form.get('zip')
            auth['zippw'] = request.form.get('zippw')
            if is_none(request.form.get('filename')) == False and is_none(request.form.get('path')) == False:
                files = [{ 'filename': request.form.get('filename'), 'path': request.form.get('path') }]
            else:
                obj = {}
                obj['name'] = None
                obj['data'] = '「ファイル名又はパス」を指定してください。'
                return jsonify(obj), 200

        if files is None or len(files) <= 0:
            obj = {}
            obj['name'] = None
            obj['data'] = 'ファイルデータは必須です。'
            return jsonify(obj), 200

    m = Mode()
    mode = auth['mode']
    obj = None
    if mode == m.sftp:
        obj = download_sftp(auth, files)
    elif mode == m.ftp:
        obj = download_ftp(auth, files)
    elif mode == m.scp:
        obj = download_scp(auth, files)
    elif mode == m.s3:
        obj = download_s3(auth, files)

    result = {}
    if auth['flag'] == 'file' and obj is not None:
        return make_response_zip(obj, True)
    elif auth['flag'] == 'json' and obj is not None:
        delete_dir(obj['path'])
        return jsonify(obj), 200
    else:
        return jsonify(result), 200
