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
    result = zip_result(list, outpath, auth['zip'], auth['zippw'])
    if result is not None:
        print('Download File S3 End !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')

    return result

def connect(auth):
    key = auth['username']
    secret = auth['password']
    s3 = boto3.resource('s3', aws_access_key_id=key, aws_secret_access_key=secret, region_name=auth['region'])
    return s3.Bucket(auth['bucket'])
