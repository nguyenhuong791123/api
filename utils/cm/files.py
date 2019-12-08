# -*- coding: UTF-8 -*-
import os
import shutil
import zipfile
import pyminizip
import stat

from ..server import *
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
    print(ziphome)
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

def zip_result(list, outpath, zip, zippw):
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
            result['filename'] = None
            result['data'] = list

    endtime = get_datetime('%Y-%m-%d %H:%M:%S', None)
    result['path'] = outpath
    result['msg'] =  '「' + endtime + '」ダウンロード完了。'

    return result

def put_files(mode, sftp, transport, lpath, rpath, files, flag):
    result = []
    m = Mode()
    if sftp is None  or rpath is None:
        return result
    if transport is None and mode in [m.sftp, m.scp]:
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
        try:
            # print(os.getcwd())
            if os.path.isfile(local):
                if mode == m.sftp:
                    mkdir = mkdir_sftp(sftp, rpath)
                    if mkdir:
                        sftp.put(local, filename)
                elif mode == m.ftp:
                    mkdir = mkdir_ftp(sftp, rpath)
                    if mkdir:
                        cmd = 'STOR %s' % filename
                        f = open(local, 'rb')
                        sftp.storbinary(cmd, f, 8192)
                        f.close()
                elif mode == m.scp:
                    mkdir = mkdir_ssh(transport, rpath)
                    if mkdir:
                        sftp.put(local, remote_path=rpath, recursive=True, preserve_times=True)
                elif mode == m.s3:
                    s3path = rpath + '/' + filename
                    sftp.upload_file(local, s3path)

                obj['msg'] =  '「' + get_datetime('%Y-%m-%d %H:%M:%S', None) + '」転送完了。'
            else:
                raise IOError('Could not find localFile %s !!' % local)
        except Exception as ex:
            # print('*** Caught exception: %s: %s' % (ex.__class__, ex))
            obj['msg'] = str(ex)
        except IOError as err:
            obj['msg'] = str(err)
        finally:
            obj['remote'] = rpath + '/' + filename
        
        result.append(obj)

    if sftp is not None:
        if mode in [m.sftp, m.scp]:
            sftp.close()
        elif mode == m.ftp:
            sftp.quit()
    if transport is not None and mode in [m.sftp, m.scp]:
        transport.close()

    print(result)
    return result

def get_files(mode, sftp, transport, outpath, files, flag):
    result = []
    m = Mode()
    if sftp is None:
        return result
    if transport is None and mode in [m.sftp, m.scp]:
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
            if mode == m.sftp:
                    sftp.get(remote, local)
            elif mode == m.ftp:
                if is_empty(remotedir) == False:
                    sftp.cwd(remotedir)
                with open(local, 'wb') as f:
                    sftp.retrbinary('RETR %s' % filename, f.write)
            elif mode == m.scp:
                sftp.get(remote_path=remote, local_path=outpath, recursive=True, preserve_times=True)
            elif mode == m.s3:
                sftp.download_file(remote, local)

            obj['filename'] = filename
        except Exception as ex:
            obj['msg'] = str(ex)
        except IOError as err:
            obj['msg'] = str(err)
        finally:
            if flag == 'json' and os.path.isfile(local):
                b64 = str(convert_file_to_b64_string(local))
                if b64 is not None:
                    obj['data'] = b64[2:(len(b64)-1)]

        result.append(obj)

    if sftp is not None:
        if mode in [m.sftp, m.scp]:
            sftp.close()
        elif mode == m.ftp:
            sftp.quit()
    if transport is not None and mode in [m.sftp, m.scp]:
        transport.close()
    
    return result

def mkdir_ftp(ftp, dir):
    if is_empty(dir):
        return False
    if dir == '/':
        sftp.chdir('/')
        return True

    try:
        ftp.cwd(dir)
        return True
    except IOError:
        print(dir)
        dirname, basename = os.path.split(dir.rstrip('/'))
        mkdir_ftp(ftp, dirname)
        ftp.mkd(basename)
        ftp.cwd(basename)
    return True

def mkdir_sftp(sftp, dir):
    if is_empty(dir):
        return False
    if dir == '/':
        sftp.chdir('/')
        return True

    try:
        sftp.chdir(dir)
        return True
    except IOError:
        dirname, basename = os.path.split(dir.rstrip('/'))
        mkdir_sftp(sftp, dirname)
        sftp.mkdir(basename)
        sftp.chdir(basename)
        return True

def mkdir_ssh(ssh, dir):
    if is_empty(dir):
        return False
    if dir == '/':
        stdin, stdout, stderr = ssh.exec_command('cd /')
        return True

    try:
        stdin, stdout, stderr = ssh.exec_command('cd ' + dir)
        return True
    except IOError:
        print(dir)
        dirname, basename = os.path.split(dir.rstrip('/'))
        mkdir_ssh(ssh, dirname)
        stdin, stdout, stderr = ssh.exec_command('mkdir  ' + basename)
        stdin, stdout, stderr = ssh.exec_command('cd ' + dir)
        return True

def make_dir_local(dir):
    if os.path.isdir(dir) == False:
        os.mkdir(dir)
    return dir

def delete_dir(path):
    print(path)
    print(os.getcwd())
    if path is not None and os.path.isdir(path):
        shutil.rmtree(path)

def make_dir_get_outpath(dir):
    if is_empty(dir):
        return './'

    make_dir_local(dir)
    outpath = get_dir(dir)
    make_dir_local(outpath)
    return outpath
