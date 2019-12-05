# -*- coding: utf-8 -*-
import boto3

from ..server import *
from ..cm.files import *
from ..cm.utils import is_exist
from ..cm.dates import get_datetime

def transport_s3(auth, files):
    print('Put File S3 Start !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None))
    s3 = connect(auth)
    if s3 is None:
        return None

    outpath = make_dir_get_outpath('upload')
    remote = auth['home'] + auth['username']
    result = put_files(Mode().s3, s3, None, outpath, remote, files, auth['flag'])
    if result is not None:
        delete_dir(outpath)

    print('Put File S3 End !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None))
    return result

def download_s3(auth, files):
    print('Download File S3 Start !!!' + get_datetime('%Y-%m-%d %H:%M:%S', None))
    s3 = connect(auth)
    if s3 is None:
        return None

    outpath = make_dir_get_outpath('download')
    list = get_files(Mode().s3, s3, None, outpath, files, auth['flag'])
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

    print('Download File S3 End !!!' + endtime)
    return result

def connect(auth):
    key = auth['username']
    secret = auth['password']
    s3 = boto3.resource('s3', aws_access_key_id=key, aws_secret_access_key=secret, region_name=auth['region'])
    return s3.Bucket(auth['bucket'])
