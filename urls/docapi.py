# -*- coding: UTF-8 -*-
from flask import Blueprint, request, redirect, render_template

from readme.readme import readme_read
from utils.cm.agent import parse_http_accept_language

app = Blueprint('docapi', __name__)

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
