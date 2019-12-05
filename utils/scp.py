# -*- coding: utf-8 -*-
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

from .cm.utils import is_exist

def transport_scp(auth, files):
    print('Put File Start !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    port = int(auth['port'])
    username = auth['username']
    if is_exist(auth['key']):
        ssh.connect(hostname=host, port=port, username=username, key_filename=auth['key'])
    else:
        ssh.connect(host, port, username, auth['password'])
    scp = scp.SCPClient(ssh.get_transport())

    if sv is None:
        return None

    dir = 'upload'
    make_dir_local(dir)
    outpath = get_dir(dir)
    make_dir_local(outpath)

    remote = '/home/' + username
    result = put_sftp_ftp_scp_files(2, scp, ssh, outpath, remote, files, auth['flag'])

    print('Put File Start !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None))
    return result
