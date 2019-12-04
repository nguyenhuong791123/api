# -*- coding: UTF-8 -*-
import os
import zipfile
import pyminizip
import stat
from .utils import convert_file_to_b64_string, convert_b64_string_to_file
from .dates import *

def get_dir(dir):
    pattern = get_pattern(True, True, None, True)
    outdir = get_datetime(pattern, -3)
    if dir is None:
        return outdir
    else:
        return os.path.join(dir, outdir)

def get_ext(filename):
    if filename is None:
        return None
    return filename.split(".")[-1]

def save_files(files, outdir):
    if os.path.isdir(outdir) == False:
        os.mkdir(outdir)

    result = []
    for file in files:
        if file is None:
            continue

        f = {}
        f['filename'] = file.filename
        f['data'] = outdir
        file.save(os.path.join(outdir, file.filename))
        result.append(f)

    return result

def zip_files(ziphome, zipname, zippw, level):
    if ziphome is None:
        ziphome = './'
    if zipname is None:
        zipname = get_dir(None) + '_zip.zip'

    # print(os.getcwd())
    if zippw is None or len(zippw) <= 0:
        with zipfile.ZipFile(zipname,'w', compression=zipfile.ZIP_STORED) as n_zip:
            for file in os.listdir(ziphome):
                n_zip.write(os.path.join(ziphome, file))
    else:
        if level is None:
            level = 4
        src = []
        for file in os.listdir(ziphome):
            src.append(os.path.join(ziphome, file))
        pyminizip.compress_multiple(src, [], zipname, zippw, level)

    return zipname

def get_sftp_files(sftp, transport, outpath, files, flag):
    result = []
    if sftp is None or transport is None:
        return result
    if outpath is None:
        outpath = '.'

    for file in files:
        if file is None:
            continue

        filename = file['filename']
        local = outpath + '/' + filename
        remote = file['path'] + '/' + filename
        obj = {}
        obj['remote'] = remote
        try:
            sftp.get(remote, local)
            obj['filename'] = filename
        except IOError as err:
            obj['msg'] = str(err)
        finally:
            if flag == 'json' and os.path.isfile(local):
                b64 = str(convert_file_to_b64_string(local))
                if b64 is not None:
                    obj['data'] = b64[2:(len(b64)-1)]

        result.append(obj)

    if sftp is not None:
        sftp.close()
    if transport is not None:
        transport.close()
        print('Download File End !!!' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    return result

def put_sftp_files(sftp, transport, lpath, rpath, files, flag):
    result = []
    if sftp is None or transport is None or rpath is None:
        return result
    if lpath is None:
        lpath = '.'

    rpath = os.path.join(rpath, get_dir(None))
    for file in files:
        if file is None:
            continue

        filename = None
        local = None
        if flag == 'json':
            filename = file['filename']
            local = lpath + '/' + filename
            convert_b64_string_to_file(file['data'], local)
        else:
            filename = file.filename
            local = lpath + '/' + filename
            file.save(local)

        if filename is None or local is None:
            continue
        # remote = '/home/' + auth['username'] + '/' + dir

        obj = {}
        mkdir = mkdir_remote(sftp, rpath)
        if mkdir == True:
            try:
                # sftp.chmod(remote, mode=777)
                if os.path.isfile(local):
                    sftp.put(local, filename)
                else:
                    raise IOError('Could not find localFile %s !!' % local)
            except IOError as err:
                obj['msg'] = str(err)
            finally:
                endtime = get_datetime('%Y-%m-%d %H:%M:%S', None)
                obj['remote'] = rpath + '/' + filename
                obj['msg'] =  '「' + endtime + '」転送完了。'
                print('Transport File End !!!' + endtime)
        else:
            obj['msg'] = 'Can not create dir to remote !!!'
        
        result.append(obj)

    if sftp is not None:
        sftp.close()
    if transport is not None:
        transport.close()

    return result

def mkdir_remote(sftp, remote_dir):
    if remote_dir == '/':
        sftp.chdir('/')
        return
    if remote_dir == '':
        return
    try:
        sftp.chdir(remote_dir)
        return True
    except IOError:
        dirname, basename = os.path.split(remote_dir.rstrip('/'))
        mkdir_remote(sftp, dirname)
        sftp.mkdir(basename)
        sftp.chdir(basename)
        return True
