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
    ts = paramiko.Transport((auth['host'], int(auth['port'])))
    ts.connect(username = auth['username'], password = auth['password'])
    sftp = paramiko.SFTPClient.from_transport(ts)
    if ts is None or sftp is None:
        return None

    outpath = make_dir_get_outpath('upload')
    remote = auth['home'] + auth['username']
    result = put_files(Mode().sftp, sftp, ts, outpath, remote, files, auth['flag'])
    if result is not None:
        delete_dir(outpath)
        print('Upload File Sftp End !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')

    return result

def download_sftp(auth, files):
    print('Download File Sftp Start !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    ts = paramiko.Transport((auth['host'], int(auth['port'])))
    ts.connect(username = auth['username'], password = auth['password'])
    sftp = paramiko.SFTPClient.from_transport(ts)
    if ts is None or sftp is None:
        return None

    outpath = make_dir_get_outpath('download')
    list = get_files(Mode().sftp, sftp, ts, outpath, files, auth['flag'])
    result = zip_result(list, outpath, auth['zip'], auth['zippw'])
    if result is not None:
        print('Download File Sftp End !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')

    return result
