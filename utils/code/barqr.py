# -*- coding: utf-8 -*-
from ..cm.utils import is_exist, is_empty
from ..cm.codes import is_bar_code, get_zbar_symbol, create_code, get_code
from ..cm.files import get_dir, delete_dir

def put_codes(auth, codes):
    print(auth)
    print(codes)
    result = None
    if codes is None or len(codes) <= 0 or is_exist(auth, 'flag') == False:
        return result

    result = []
    flag = auth['flag']
    code = None
    outpath = make_dir_get_outpath('download')
    if is_exist(auth, 'code'):
        code = auth['code']
    for c in codes:
        if is_exist(c, 'code'):
            code = c['code']
        if is_empty(code):
            continue
        if is_exist(c, 'value') == False or is_empty(c['value']):
            continue

        value = c['value']
        filename = value
        if is_exist(c, 'filename') and is_empty() == False:
            filename = c['filename']
        if is_exist(c, 'flag'):
            flag = c['flag']
        else:
            flag = auth['flag']

        options = None
        if code == 'qr' and is_exist(c, 'options'):
            options = c['options']
        obj = create_code(flag, code, value, outpath, filename, options)
    
        if obj is not None:
            result.append(obj)

    if result is not None:
        delete_dir(outpath)

    return result

def get_codes(auth, codes):
    print(auth)
    print(codes)
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