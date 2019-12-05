# -*- coding: utf-8 -*-
import os
import shutil
import datetime
import base64
import paramiko
# paramiko.util.log_to_file('/tmp/paramiko.log')

from .cm.utils import *
from .cm.files import *
from .cm.dates import get_datetime

def transport_sftp(auth, files):
    print('Upload File Start !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    transport = paramiko.Transport((auth['host'], int(auth['port'])))
    transport.connect(username = auth['username'], password = auth['password'])
    sftp = paramiko.SFTPClient.from_transport(transport)

    # dir = 'upload'
    # make_dir_local(dir)
    # outpath = get_dir(dir)
    # make_dir_local(outpath)
    outpath = make_dir_get_outpath('upload')

    remote = '/home/' + auth['username']
    result = put_sftp_ftp_scp_files(0, sftp, transport, outpath, remote, files, auth['flag'])
    if result is not None:
        delete_dir(outpath)

    print('Upload File End !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    return result

def download_sftp(auth, files):
    print('Download File Start !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    transport = paramiko.Transport((auth['host'], int(auth['port'])))
    transport.connect(username = auth['username'], password = auth['password'])
    sftp = paramiko.SFTPClient.from_transport(transport)

    # dir = 'download'
    # make_dir_local(dir)
    # outpath = get_dir(dir)
    # make_dir_local(outpath)
    outpath = make_dir_get_outpath('download')

    list = get_sftp_ftp_scp_files(0, sftp, transport, outpath, files, auth['flag'])
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

    print('Download File End !!!' + endtime + ']')
    return result
