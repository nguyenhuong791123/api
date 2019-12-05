# -*- coding: utf-8 -*-
from .cm.utils import *

def default_auth_server(inAuth):
    if is_exist(inAuth, 'mode') == False:
        return None

    auth = {}
    mode = inAuth['mode']
    if mode == 'ftp':
        auth['host'] = 'sc-ftp-01'
        auth['port'] = 21
        auth['tls'] = True
        auth['username'] = 'huongnv'
        auth['password'] = 'Nguyen080!'
    elif mode == 'sftp':
        auth['host'] = 'sc-sftp-01'
        auth['port'] = 22
        auth['username'] = 'huongnv'
        auth['password'] = 'Nguyen080!'
    elif mode == 'scp':
        auth['host'] = 'sc-scp-01'
        auth['port'] = 22
        auth['username'] = 'huongnv'
        auth['password'] = 'Nguyen080!'
    else:
        return None

    for k in inAuth.keys():
        auth[k] = inAuth[k]

    return auth