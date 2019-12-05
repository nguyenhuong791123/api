# -*- coding: utf-8 -*-
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

from ..server import *
from ..cm.utils import is_exist

def transport_scp(auth, files):
    print('Put File Scp Start !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    port = int(auth['port'])
    username = auth['username']
    if is_exist(auth['key']):
        ssh.connect(hostname=host, port=port, username=username, key_filename=auth['key'])
    else:
        ssh.connect(host, port, username, auth['password'])
    scp = scp.SCPClient(ssh.get_transport())

    outpath = make_dir_get_outpath('upload')
    remote = auth['home'] + username
    result = put_files(Mode().scp, scp, ssh, outpath, remote, files, auth['flag'])
    if result is not None:
        delete_dir(outpath)

    print('Put File Scp End !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None))
    return result

def download_scp(auth, files):
    print('Download File Scp Start !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    port = int(auth['port'])
    username = auth['username']
    if is_exist(auth['key']):
        ssh.connect(hostname=host, port=port, username=username, key_filename=auth['key'])
    else:
        ssh.connect(host, port, username, auth['password'])
    scp = scp.SCPClient(ssh.get_transport())

    outpath = make_dir_get_outpath('download')
    list = get_files(Mode().scp, scp, ssh, outpath, files, auth['flag'])
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

    print('Download File Scp End !!!' + endtime + ']')
    return result