# -*- coding: UTF-8 -*-
import os
import base64
import smtplib
import ssl
import shutil
import zipfile
import pyminizip
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders

from ..cm.utils import *
from ..cm.dates import get_datetime
from ..cm.files import get_dir, make_dir_local, delete_dir
from ..cm.mails import *

def send_mail(auth, objs):
    print('Send Mail Smtp Start !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    results = []
    for obj in objs:
        if is_exist(obj, 'from') == False or is_empty(obj['from']) == True or is_exist(obj, 'to') == False or is_empty(obj['to']) == True:
            continue

        recipients = []
        verifys = obj['to'].split(',')
        for ac in verifys:
            if is_valid(ac) == False:
                continue
            recipients.append(ac)

        msg = getMIMEMultipart(obj)
        if is_exist(obj, 'files') and len(obj['files']) > 0:
            # print(os.getcwd())
            updir = make_dir_local('upload')
            dir = get_dir(None)
            outpath = make_dir_local(os.path.join(updir, dir))
            msg = add_temps(msg, obj, dir, updir, outpath)

        result = {}
        smtpclient = None
        zip = obj['zip']
        zipname = None
        try:
            host = auth['host'] # "smtp.gmail.com"
            nego_combo = (auth['auth'], auth['port']) # ("starttls", 587)
            if nego_combo[0] == "no-encrypt":
                smtpclient = smtplib.SMTP(host, nego_combo[1], timeout=10)
            elif nego_combo[0] == "starttls":
                smtpclient = smtplib.SMTP(host, nego_combo[1], timeout=10)
                smtpclient.ehlo()
                smtpclient.starttls()
                smtpclient.ehlo()
            elif nego_combo[0] == "ssl":
                context = ssl.create_default_context()
                smtpclient = smtplib.SMTP_SSL(host, nego_combo[1], timeout=10, context=context)
            smtpclient.set_debuglevel(2)

            smtpclient.login(auth['username'], auth['password'])
            smtpclient.sendmail(obj['from'], recipients, msg.as_string())
            result['flag'] = True
            result['msg'] = obj['from'] + 'から[' + ','.join(recipients) + ']へメールを送信しました。'
        except Exception as e:
            result['flag'] = False
            result['msg'] = str(e)
        finally:
            if smtpclient is not None:
                smtpclient.quit()
            if outpath is not None and os.path.isdir(outpath):
                shutil.rmtree(outpath)
            if zip is not None and zip == True and os.path.isfile(updir + '/' + dir + '_zip.zip'):
                os.remove(updir + '/' + dir + '_zip.zip')

        results.append(result)

    print('Send Mail Smtp End!!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    return results

def getMIMEMultipart(obj):
    body = obj['body']
    charset = 'utf-8'
    type = 'plain'
    if is_exist(obj, 'charset') and len(obj['charset']) > 0:
        charset = obj['charset']
    if is_exist(obj, 'type') and len(obj['type']) > 0:
        type = obj['type']

    msg = MIMEMultipart()
    if type == 'html':
        msg = MIMEMultipart('alternative')

    plain = None
    html = None
    if charset == "utf-8":
        plain = MIMEText(body, "plain", charset)
        if type == 'html':
            html = MIMEText(body, 'html', charset)
    elif charset == "iso-2022-jp":
        plain = MIMEText(base64.b64encode(body.encode(charset, "ignore")), "plain", charset)
        if type == 'html':
            html = MIMEText(base64.b64encode(body.encode(charset, "ignore")), "html", charset)

    plain.replace_header("Content-Transfer-Encoding", "base64")
    msg.attach(plain)
    if type == 'html' and html is not None:
        html.replace_header("Content-Transfer-Encoding", "base64")
        msg.attach(html)

    msg["Subject"] = obj['subject']
    msg["From"] = obj['from']
    msg["To"] = obj['to']
    msg["Cc"] = obj['cc']
    msg["Bcc"] = obj['bcc']
    msg["Date"] = formatdate(localtime = True)
    return msg

def add_temps(msg, obj, dir, updir, outpath):
    zip = obj['zip']
    zippw = obj['zippw']
    files = obj['files']
    for o in files:
        filename = o['filename']
        outfile = outpath + '/' + filename
        convert_b64_string_to_file(o['data'], outfile)
        if zip is None or zip == False:
            ext = filename.split(".")[-1]
            if os.path.isfile(outfile):
                attach = MIMEApplication(open(outfile, 'rb').read(), _subtype=ext)
                attach.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(attach)

    if zip is not None and (zip == True or str(zip).lower() == 'true'):
        os.chdir(updir)
        zipname = dir + '_zip.zip'
        if zippw is None or len(zippw) <= 0:
            with zipfile.ZipFile(zipname,'w', compression=zipfile.ZIP_STORED)as n_zip:
                for file in os.listdir(dir):
                    n_zip.write(os.path.join(dir, file))
        else:
            src = []
            level = 4
            for file in os.listdir(dir):
                src.append(os.path.join(dir, file))
            pyminizip.compress_multiple(src, [], zipname, zippw, level)

        os.chdir('../')
        zippath = updir + '/' + zipname
        if os.path.isfile(zippath):
            attach = MIMEBase('application', 'zip')
            attach.set_payload(open(zippath, 'rb').read())
            encoders.encode_base64(attach)
            attach.add_header('Content-Disposition', 'attachment', filename=zipname)
            msg.attach(attach)

    return msg