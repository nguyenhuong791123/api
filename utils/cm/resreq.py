
# -*- coding: UTF-8 -*-
import os
from importlib import import_module
from flask import make_response
from .utils import is_empty
from .files import delete_dir

def make_response_zip(obj, delete):
    print(obj)
    res = make_response()
    filename = obj['filename']
    fullpath = obj['path'] + '/' + filename
    res.data = open(fullpath, 'rb').read()
    res.headers['Content-Disposition'] = "attachment; filename=" + filename
    res.mimetype = 'application/zip'

    if delete:
        delete_dir(obj['path'])
    return res

def load_apis(app):
    path = 'urls'
    for file in os.listdir(path):
        if os.path.isfile(path + '/' + file) == False:
            continue
        name = file.split('.')[0]
        if is_empty(name):
            continue
        i = import_module(path + '.' + name)
        if i is None:
            continue
        app.register_blueprint(i.app)
