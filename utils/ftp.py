# -*- coding: utf-8 -*-
import datetime
from ftplib import FTP
from .cm.files import *

def transport_ftp(auth, files):
    print('Transport File Start !!!' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    sv = server(auth)
    if sv is None:
        return None

    dir = 'upload'
    make_dir_local(dir)
    outpath = get_dir(dir)
    make_dir_local(outpath)

    # remote = '/home/' + auth['username'] + '/' + dir
    remote = '/home/ftpusers/' + auth['username']
    result = put_ftp_sftp_files(False, sv, None, outpath, remote, files, auth['flag'])
    # if result is not None:
    #     delete_dir(outpath)

    return result

def server(auth):
    port = int(auth['port'])
    host = auth['host']
    if port != 21:
        host += ':' + auth['port']

    sv = FTP(host)
    sv.set_pasv("true")
    sv.login(auth['username'], auth['password'])

    return sv