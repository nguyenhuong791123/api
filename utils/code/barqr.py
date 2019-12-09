# -*- coding: utf-8 -*-

from ..cm.utils import is_exist, is_empty
from ..cm.codes import is_bar_code

def get_codes(codes):
    result = []
    if codes is None or len(codes) <= 0:
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
        # obj = None
        # if ismode:
        #     obj = create_bar_code(c['code'], value, outpath, filename)
        # else:
        #     options = None
        #     if is_exist(c, 'options'):
        #         options = c['options']
        #     obj = create_qr_code(value, outpath, filename, options)
    
        if obj is not None:
            result.append(obj)

    return result
