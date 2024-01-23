# -*- coding: utf-8 -*-
from .cm.utils import *

class Mode():
    sftp = 0
    ftp = 1
    scp = 2
    s3 = 3
    smtp = 4
    pop3 = 5
    imap = 6

def default_server(inAuth):
    if is_exist(inAuth, 'mode') == False:
        return None

    auth = {}
    mode = inAuth['mode']
    m = Mode()
    if mode == m.sftp:
        auth['host'] = 'sc-sftp-01'
        auth['port'] = 22
        auth['username'] = 'huongnv'
        auth['password'] = 'Nguyen080!'
        auth['home'] = '/home/'
    elif mode == m.ftp:
        auth['host'] = 'sc-ftp-01'
        auth['port'] = 21
        auth['tls'] = True
        auth['username'] = 'huongnv'
        auth['password'] = 'Nguyen080!'
        auth['home'] = '/home/ftpusers/'
    elif mode == m.scp:
        auth['host'] = 'sc-scp-01'
        auth['port'] = 22
        auth['username'] = 'huongnv'
        auth['password'] = 'Nguyen080!'
        auth['home'] = '/home/'
    elif mode == m.s3:
        auth['username'] = 'AKIA2K5FFLLCEIPWKVH5'
        auth['password'] = 'DqjbmOoCIrleH/0ggQONuOn+PCeZzcopF9Xd9iYe'
        auth['region'] = 'ap-northeast-1'
        auth['bucket'] = 's3-sc-files'
        auth['home'] = ''
    elif mode == m.smtp:
        auth['host'] = 'smtp.gmail.com'
        auth['port'] = 587
        auth['auth'] = 'starttls'
        auth['username'] = 'nguyenhuong791123@gmail.com'
        auth['password'] = 'huong080'
    elif mode == m.pop3:
        auth['host'] = 'pop.gmail.com'
        auth['port'] = 995
        auth['auth'] = 'ssl'
        auth['username'] = 'nguyenhuong791123@gmail.com'
        auth['password'] = 'huong080'
        auth['method'] = 'user'
        auth['count'] = 5
    elif mode == m.imap:
        auth['host'] = 'imap.gmail.com'
        auth['port'] = 993
        auth['auth'] = 'ssl'
        auth['username'] = 'nguyenhuong791123@gmail.com'
        auth['password'] = 'huong080'
        auth['box'] = 'IMAP4BOX'
        auth['count'] = 5
    else:
        return None

    for k in inAuth.keys():
        auth[k] = inAuth[k]

    return auth
