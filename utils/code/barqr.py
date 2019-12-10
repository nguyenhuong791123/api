# -*- coding: utf-8 -*-
import os
from ..cm.utils import is_exist, is_empty, convert_b64_string_to_file
from ..cm.codes import is_bar_code, get_zbar_symbol, create_code, get_code
from ..cm.files import get_dir, delete_dir, make_dir_get_outpath, zip_result

def put_codes(auth, codes):
    result = None
    if codes is None or len(codes) <= 0:
        return result

    result = []
    flag = None
    if is_exist(auth, 'flag'):
        flag = auth['flag']
    outpath = make_dir_get_outpath('download')
    code = None
    for c in codes:
        if is_exist(c, 'code'):
            code = c['code']
        else:
            code = auth['code']
        if is_empty(code):
            continue
        if is_exist(c, 'data') == False or is_empty(c['data']):
            continue

        value = c['data']
        filename = value
        if is_exist(c, 'filename') and is_empty(c['filename']) == False:
            filename = c['filename']

        options = None
        if code == 'qr' and is_exist(c, 'options'):
            options = c['options']
        obj = create_code(flag, code, value, outpath, filename, options)
    
        if obj is not None:
            result.append(obj)

    if flag != 'json' and is_exist(auth, 'zip') and is_exist(auth, 'zippw'):
        result = zip_result(result, outpath, auth['zip'], auth['zippw'])

    return result

def get_codes(auth, codes):
    result = None
    if codes is None or len(codes) <= 0:
        return result

    result = []
    outpath = make_dir_get_outpath('download')
    flag = None
    if is_exist(auth, 'flag'):
        flag = auth['flag']
    code = None
    for c in codes:
        if is_exist(c, 'code'):
            code = c['code']
        else:
            code = auth['code']
        if is_empty(code):
            continue

        symbols = get_zbar_symbol(code)
        if flag is not None and flag == 'json':
            filename = get_dir(None) + '.png'
            if is_exist(c, 'filename') and is_empty(c['filename']) == False:
                filename = c['filename']

            symbols = get_zbar_symbol(code)
            local = os.path.join(outpath, filename)
            convert_b64_string_to_file(c['data'], local)
        else:
            filename = c.filename
            c.save(os.path.join(outpath, filename))

        result.append(get_code(outpath, filename, symbols))

    if result is not None and len(result) > 0:
        delete_dir(outpath)

    return result