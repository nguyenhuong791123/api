# -*- coding: utf-8 -*-
import os
import shutil
import datetime
import base64
import paramiko
# paramiko.util.log_to_file('/tmp/paramiko.log')

from ..server import *
from ..cm.utils import *
from ..cm.files import *
from ..cm.dates import get_datetime

def transport_sftp(auth, files):
    print('Upload File Sftp Start !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    transport = paramiko.Transport((auth['host'], int(auth['port'])))
    transport.connect(username = auth['username'], password = auth['password'])
    sftp = paramiko.SFTPClient.from_transport(transport)

    outpath = make_dir_get_outpath('upload')
    remote = auth['home'] + auth['username']
    result = put_files(Mode().sftp, sftp, transport, outpath, remote, files, auth['flag'])
    if result is not None:
        delete_dir(outpath)

    print('Upload File Sftp End !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    return result

def download_sftp(auth, files):
    print('Download File Sftp Start !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    transport = paramiko.Transport((auth['host'], int(auth['port'])))
    transport.connect(username = auth['username'], password = auth['password'])
    sftp = paramiko.SFTPClient.from_transport(transport)

    outpath = make_dir_get_outpath('download')
    list = get_files(Mode().sftp, sftp, transport, outpath, files, auth['flag'])

    return zip_result(list, outpath, auth['zip'], auth['zippw'])
    # result = {}
    # if zip is not None and (zip == True or zip.lower() == 'true'):
    #     os.chdir(outpath)
    #     result['filename'] = zip_files(None, None, zippw, None)
    #     result['data'] = None
    #     os.chdir('../../')
    # else:
    #     if len(list) == 1:
    #         result['filename'] = list[0]['filename']
    #         result = list[0]
    #     else:
    #         result['filename'] = zipname
    #         result['data'] = list

    # endtime = get_datetime('%Y-%m-%d %H:%M:%S', None)
    # result['path'] = outpath
    # result['msg'] =  '「' + endtime + '」ダウンロード完了。'

    # print('Download File Sftp End !!!' + endtime + ']')
    # return result
