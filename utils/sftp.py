# -*- coding: utf-8 -*-
import os
import shutil
import datetime
import base64
# import zipfile
# import pyminizip
import paramiko
# paramiko.util.log_to_file('/tmp/paramiko.log')

from .common.utils import *
from .common.files import *

def transport_sftp(auth, files):
    print('Transport File Start !!!' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    transport = paramiko.Transport((auth['host'], int(auth['port'])))
    transport.connect(username = auth['username'], password = auth['password'])
    sftp = paramiko.SFTPClient.from_transport(transport)

    dir = 'upload'
    if os.path.isdir(dir) == False:
        os.mkdir(dir)
    outpath = get_dir(dir)
    if os.path.isdir(outpath) == False:
        os.mkdir(outpath)

    # remote = '/home/' + auth['username'] + '/' + dir
    remote = '/home/' + auth['username']
    result = put_sftp_files(sftp, transport, outpath, remote, files, auth['flag'])

    delete_dir(outpath)
    return result

def download_sftp(auth, files):
    print('Download File Start !!!' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    transport = paramiko.Transport((auth['host'], int(auth['port'])))
    transport.connect(username = auth['username'], password = auth['password'])
    sftp = paramiko.SFTPClient.from_transport(transport)

    dir = 'download'
    if os.path.isdir(dir) == False:
        os.mkdir(dir)
    outpath = get_dir(dir)
    if os.path.isdir(outpath) == False:
        os.mkdir(outpath)

    list = get_sftp_files(sftp, transport, outpath, files, auth['flag'])
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

    result['path'] = outpath
    result['msg'] =  '「' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '」ダウンロード完了。'
    return result
