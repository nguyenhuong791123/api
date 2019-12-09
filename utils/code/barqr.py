# -*- coding: utf-8 -*-
from ..cm.utils import is_exist, is_empty
from ..cm.codes import is_bar_code, get_zbar_symbol
from ..cm.files import get_dir, delete_dir

def put_codes(codes):
    result = None
    if codes is None or len(codes) <= 0:
        return result

    result = []
    outpath = make_dir_get_outpath('download')
    for c in codes:
        ismode = is_bar_code(c['code'])
        if ismode == False and c['code'] != 'qr':
            continue
        if is_exist(c, 'value') == False or is_empty(c['value']):
            continue

        value = c['value']
        filename = value
        if is_exist(c, 'filename') and is_empty() == False:
            filename = c['filename']

        flag = 'json'
        if is_exist(c, 'flag'):
            flag = c['flag']
        options = None
        if c['code'] == 'qr' and is_exist(c, 'options'):
            options = c['options']
        obj = create_code(flag, ismode, c['code'], value, outpath, filename, options)
    
        if obj is not None:
            result.append(obj)

    if result is not None:
        delete_dir(outpath)

    return result

def get_codes(auth, codes):
    result = None
    if codes is None or len(codes) <= 0 or is_exist(auth, 'flag') == False:
        return result

    result = []
    outpath = make_dir_get_outpath('download')
    flag = auth['flag']
    code = auth['code']
    for c in codes:
        symbols = get_zbar_symbol(code)
        if flag is not None and flag == 'json':
            filename = get_dir(None) + '.png'
            if is_exist(c, 'filename'):
                filename = c['filename']
            if is_exist(c, 'code'):
                code = c['code']
            symbols = get_zbar_symbol(code)
            local = os.path.join(outpath, filename)
            convert_b64_string_to_file(c['data'], local)
        else:
            filename = c.filename
            c.save(os.path.join(outpath, filename))

        obj = {}
        obj['filename'] = filename
        obj['data'] = get_code(outpath, filename, symbols)
        result.append(obj)

    return result