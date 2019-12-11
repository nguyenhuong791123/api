# -*- coding: UTF-8 -*-
import os
import pdfkit

from ..cm.utils import *
from ..cm.dates import get_datetime
from ..cm.files import get_dir, make_dir_local, save_files, get_ext

def get_pdf(obj):
    print('Create Pdf Start !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    if is_exist(obj, 'data') == False or is_empty(obj['data']):
        return None

    flag = None
    if is_exist(obj, 'flag') and is_empty(obj['flag']) == False:
        flag = obj['flag']

    data = obj['data']
    outdir = make_dir_local('download/')
    if data is not None and is_type(data, Obj.LIST) == True and is_empty(data[0]['data']) == False and os.path.isdir(data[0]['data']):
        outdir = data[0]['data']
    if os.path.isdir(outdir) == False:
        os.mkdir(outdir)

    filename = None
    if is_exist(obj, 'filename') and is_empty(obj['filename']) == False:
        filename = obj['filename']
    if filename is None:
        filename = get_dir(None) + '_sc.pdf'

    result = {}
    options = default_options(obj)
    try:
        outpath = os.path.join(outdir, filename)
        if flag == 'url':
            # print(os.getcwd())
            pdfkit.from_url(data, outpath, options=options)
        elif flag == 'file':
            html = []
            css = []
            for o in data:
                name = o['filename']
                ext = get_ext(name)
                if ext != 'html' and ext != 'css':
                    continue

                path = os.path.join(o['data'], name)
                if os.path.isfile(path) == False:
                    path = os.path.join(outdir, name)
                    convert_b64_string_to_file(o['data'], path)

                if ext == 'html':
                    html.append(path)
                elif ext == 'css':
                    css.append(path)

            pdfkit.from_file(html, outpath, options=options)
            # if css is None and len(css) <= 0:
            #     pdfkit.from_file(html, outpath, options=options)
            # else:
            #     print(html)
            #     print(css)
            #     pdfkit.from_file(html, outpath, options=options, css=css)
        else:
            pdfkit.from_string(data, outpath, options=options)
    except IOError as e:
        result['msg'] = str(e)
    finally:
        result['path'] = outdir
        result['filename'] = filename

    print('Create Pdf End !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    return result

def default_options(obj):
    created = get_datetime(None, None)
    opts = {
        'header-left': 'SC PDF API v0.1.0'
        # ,'header-center': 'AAA'
        ,'header-right': '[page] / [topage]'
        ,'footer-left': 'Copyright © 2020 SC Systems Inc. All Rights Reserved.'
        # ,'footer-center': 'Wellcome to SC Systems!!!'
        ,'footer-right': created
        ,'header-spacing': 3
        ,'footer-spacing': 3
        ,'password': 'abcd'
        ,'page-size': 'A4'
        ,'dpi': 400
        ,'orientation': 'Landscape' #'Portrait'
        ,'margin-top': '0.4in'
        ,'margin-left': '0.1in'
        ,'margin-right': '0.1in'
        ,'margin-bottom': '0.4in'
        ,'encoding': "utf-8"
        ,'no-outline': None
        ,'disable-smart-shrinking': ''
        ,'user-style-sheet': True
    }
    if is_exist(obj, 'options') == False or is_json(obj['options']) == False:
        return opts

    options = obj['options']
    for key in options.keys():
        if is_empty(options[key]):
            continue
        opts[key] = options[key]

    return opts

def get_forms(req):
    obj = None
    files = req.files.getlist('file')
    if files is not None and len(files)>0:
        outpath = make_dir_local('download/')
        obj = {}
        obj['flag'] = 'file'
        obj['data'] = save_files(files, outpath)

    if obj is None and req.form is not None:
        url = req.form.get('url')
        filename = req.form.get('filename')
        if is_empty(filename) == False:
            filename = get_dir(None) + '_sc.pdf'
        if is_empty(url) == False:
            obj = {}
            obj['flag'] = 'url'
            obj['data'] = url
            obj['filename'] = filename

        html = req.form.get('html')
        if is_empty(html) == False:
            obj = {}
            obj['flag'] = ''
            obj['data'] = html
            obj['filename'] = filename

    return obj
