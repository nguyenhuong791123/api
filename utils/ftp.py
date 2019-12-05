# -*- coding: utf-8 -*-
import datetime
from ftplib import FTP, FTP_TLS
from .cm.files import *
from .cm.dates import get_datetime

def transport_ftp(auth, files):
    print('Put File Start !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None))
    sv = connect(auth)
    if sv is None:
        return None

    # dir = 'upload'
    # make_dir_local(dir)
    # outpath = get_dir(dir)
    # make_dir_local(outpath)
    outpath = make_dir_get_outpath('upload')

    remote = '/home/ftpusers/' + auth['username']
    result = put_sftp_ftp_scp_files(1, sv, None, outpath, remote, files, auth['flag'])

    print('Put File Start !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None))
    return result

def download_ftp(auth, files):
    print('Download File Start !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None))
    sv = connect(auth)
    if sv is None:
        return None

    # dir = 'download'
    # make_dir_local(dir)
    # outpath = get_dir(dir)
    # make_dir_local(outpath)
    outpath = make_dir_get_outpath('download')

    list = get_sftp_ftp_scp_files(1, sv, None, outpath, files, auth['flag'])
    zip = auth['zip']
    zippw = auth['zippw']
    result = {}
    if zip is not None and (zip == True or zip.lower() == 'true'):
        os.chdir(outpath)
        result['filename'] = zip_files(None, None, zippw, None)
        result['data'] = None
        os.chdir('../../')
    else:
        if len(list) == 1:
            result['filename'] = list[0]['filename']
            result = list[0]
        else:
            result['filename'] = zipname
            result['data'] = list

    endtime = get_datetime('%Y-%m-%d %H:%M:%S', None)
    result['path'] = outpath
    result['msg'] =  '「' + endtime + '」ダウンロード完了。'

    print('Download File End !!!' + endtime)
    return result

def connect(auth):
    host = auth['host']
    port = int(auth['port'])
    if port != 21:
        host += ':' + auth['port']

    sv = None
    try:
        tls = auth['tls']
        if tls:
            sv = FTP(host)
        else:
            sv = FTP_TLS(host)
            sv.prot_p()

        sv.set_pasv("true")
        sv.login(auth['username'], auth['password'])
    except ftplib.all_errors as e:
        print('FTP error = %s' % e)
    finally:
        print(sv.getwelcome())

    return sv
