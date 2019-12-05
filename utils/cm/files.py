# -*- coding: UTF-8 -*-
import os
import shutil
import zipfile
import pyminizip
import stat
from .utils import convert_file_to_b64_string, convert_b64_string_to_file, is_empty
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

def put_sftp_ftp_scp_files(mode, sftp, transport, lpath, rpath, files, flag):
    result = []
    if sftp is None  or rpath is None:
        return result
    if transport is None and mode == 0:
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

        obj = {}
        mkdir = False
        if mode == 0:
            mkdir = mkdir_sftp_remote(sftp, rpath)
        elif mode == 1:
            # mkdir = mkdir_ftp_remote(sftp, rpath)
            mkdir = True
        elif mode == 2:
            # mkdir = mkdir_scp_remote(sftp, rpath)
            mkdir = True
        if mkdir == True:
            try:
                if os.path.isfile(local):
                    if mode != 1:
                        if mode == 0:
                            sftp.put(local, filename)
                        elif mode == 2:
                            sftp.put(local, remote_path=rpath, recursive=True, preserve_times=True)
                    else:
                        # print(os.getcwd())
                        cmd = 'STOR %s' % filename
                        f = open(local, 'rb')
                        sftp.storbinary(cmd, f, 8192)
                        f.close()
                else:
                    raise IOError('Could not find localFile %s !!' % local)
            except IOError as err:
                obj['msg'] = str(err)
            finally:
                obj['remote'] = rpath + '/' + filename
                obj['msg'] =  '「' + get_datetime('%Y-%m-%d %H:%M:%S', None) + '」転送完了。'
        else:
            obj['msg'] = 'Can not create dir to remote !!!'
        
        result.append(obj)

    if sftp is not None:
        if mode != 1:
            sftp.close()
        else:
            sftp.quit()
    if transport is not None and mode == 0:
        transport.close()

    return result

def get_sftp_ftp_scp_files(mode, sftp, transport, outpath, files, flag):
    result = []
    if sftp is None:
        return result
    if transport is None and mode != 1:
        return result
    if outpath is None:
        outpath = '.'

    for file in files:
        if file is None:
            continue

        filename = file['filename']
        remotedir = file['path']
        remote = remotedir + '/' + filename
        obj = {}
        obj['remote'] = remote
        try:
            local = outpath + '/' + filename
            if mode != 1:
                if mode == 0:
                    sftp.get(remote, local)
                elif mode == 2:
                    sftp.get(remote_path=remote, local_path=outpath, recursive=True, preserve_times=True)
            else:
                # if is_empty(remotedir) == False:
                #     sftp.cwd(remotedir)
                with open(local, 'wb') as f:
                    sftp.retrbinary('RETR %s' % filename, f.write)

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
        if mode != 1:
            sftp.close()
        else:
            sftp.quit()
    if transport is not None and mode != 1:
        transport.close()
    
    return result

def mkdir_ftp_remote(ftp, dir):
    if is_empty(dir):
        return False
    if dir == '/':
        sftp.chdir('/')
        return True

    try:
        ftp.cwd(dir)
    except IOError:
        print(dir)
        dirname, basename = os.path.split(dir.rstrip('/'))
        mkdir_ftp_remote(ftp, dirname)
        ftp.mkd(basename)
        ftp.cwd(basename)
    return True

def mkdir_sftp_remote(sftp, dir):
    if is_empty(dir):
        return False
    if dir == '/':
        sftp.chdir('/')
        return True

    try:
        sftp.chdir(dir)
    except IOError:
        dirname, basename = os.path.split(dir.rstrip('/'))
        mkdir_sftp_remote(sftp, dirname)
        sftp.mkdir(basename)
        sftp.chdir(basename)
        return True

def make_dir_local(dir):
    if os.path.isdir(dir) == False:
        os.mkdir(dir)

def delete_dir(path):
    print(path)
    print(os.getcwd())
    if path is not None and os.path.isdir(path):
        shutil.rmtree(path)
