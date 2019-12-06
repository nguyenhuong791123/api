# -*- coding: UTF-8 -*-
from flask import Blueprint, request, jsonify, make_response

from utils.server import default_server
from utils.mail.smtp import send_mail
from utils.mail.pop3 import get_pop3
from utils.mail.imap import get_imap

app = Blueprint('mailapi', __name__)

@app.route('/imap', methods=[ 'POST' ])
def imap():
    auth = None
    if request.method == 'POST':
        if request.json is not None:
            if is_json(request.json):
                auth = request.json.get('auth')

    if auth is None:
        auth = {}
        auth['mode'] = Mode().imap
        auth = default_server(auth)

    # result = {}
    # result['result'] = get_imap(auth)
    return jsonify(get_imap(auth)), 200

@app.route('/pop3', methods=[ 'POST' ])
def pop3():
    auth = Mone
    if request.method == 'POST':
        if request.json is not None:
            if is_json(request.json):
                auth = request.json.get('auth')

    if auth is None:
        auth = {}
        auth['mode'] = Mode().pop3
        auth = default_server(auth)

    # result = {}
    # result['result'] = get_pop3(auth)
    return jsonify(get_pop3(auth)), 200

@app.route('/smtp', methods=[ 'POST' ])
def smtp():
    auth = None
    if request.method == 'POST':
        if request.json is not None:
            if is_json(request.json):
                auth = request.json.get('auth')
                mails = request.json.get('mails')
        if mails is None or str(mails) == '{}':
            data = open('data/mail/data.json', 'r')
            info = json.load(data)
            mails = info['mails']

    if auth is None:
        auth = {}
        auth['mode'] = Mode().smtp
        auth = default_server(auth)

    # result = {}
    # result['result'] = send_mail(auth, mails)
    return jsonify(send_mail(auth, mails)), 200