# -*- coding: utf-8 -*-
import datetime
from ftplib import FTP, FTP_TLS

from ..server import *
from ..cm.files import *
from ..cm.dates import get_datetime

def transport_ftp(auth, files):
    print('Put File Ftp Start !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None))
    ftp = connect(auth)
    if ftp is None:
        return None

    outpath = make_dir_get_outpath('upload')
    remote = auth['home'] + auth['username']
    result = put_files(Mode().ftp, ftp, None, outpath, remote, files, auth['flag'])
    if result is not None:
        delete_dir(outpath)

    print('Put File Ftp End !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None))
    return result

def download_ftp(auth, files):
    print('Download File Ftp Start !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    ftp = connect(auth)
    if ftp is None:
        return None

    outpath = make_dir_get_outpath('download')
    list = get_files(Mode().ftp, ftp, None, outpath, files, auth['flag'])
    result = zip_result(list, outpath, auth['zip'], auth['zippw'])
    if result is not None:
        print('Download File Ftp End !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')

    return result

def connect(auth):
    host = auth['host']
    port = int(auth['port'])
    if port != 21:
        host += ':' + auth['port']

    ftp = None
    try:
        tls = auth['tls']
        if tls:
            ftp = FTP(host)
        else:
            ftp = FTP_TLS(host)
            ftp.prot_p()

        ftp.set_pasv("true")
        ftp.login(auth['username'], auth['password'])
    except ftplib.all_errors as e:
        print('FTP error = %s' % e)
    finally:
        print(ftp.getwelcome())

    return ftp
