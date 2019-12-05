# -*- coding: utf-8 -*-
from .cm.utils import *

def default_auth_server(inAuth):
    if is_exist(inAuth, 'mode') == False:
        return None

    auth = {}
    mode = inAuth['mode']
    m = Mode()
    if mode == m.sftp: # 0
        auth['host'] = 'sc-sftp-01'
        auth['port'] = 22
        auth['username'] = 'huongnv'
        auth['password'] = 'Nguyen080!'
        auth['home'] = '/home/'
    elif mode == m.ftp: # 1
        auth['host'] = 'sc-ftp-01'
        auth['port'] = 21
        auth['tls'] = True
        auth['username'] = 'huongnv'
        auth['password'] = 'Nguyen080!'
        auth['home'] = '/home/ftpusers/'
    elif mode == m.scp: # 2
        auth['host'] = 'sc-scp-01'
        auth['port'] = 22
        auth['username'] = 'huongnv'
        auth['password'] = 'Nguyen080!'
        auth['home'] = '/home/'
    elif mode == m.s3: # 3
        auth['username'] = 'AKIA2K5FFLLCEIPWKVH5'
        auth['password'] = 'DqjbmOoCIrleH/0ggQONuOn+PCeZzcopF9Xd9iYe'
        auth['region'] = 'ap-northeast-1'
        auth['bucket'] = 's3-sc-files'
        auth['home'] = ''
    else:
        return None

    for k in inAuth.keys():
        auth[k] = inAuth[k]

    return auth

class Mode():
    sftp = 0
    ftp = 1
    scp = 2
    s3 = 3
