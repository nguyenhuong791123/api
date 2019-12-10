
# -*- coding: UTF-8 -*-
from flask import make_response
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
