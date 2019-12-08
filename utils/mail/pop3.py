
# -*- coding: UTF-8 -*-
import json
import base64
import datetime
import email
import poplib
import ssl
from email.header import decode_header, make_header
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

from ..cm.dates import get_datetime

def get_pop3(auth):
    print('Get Mail Pop3 Start !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    host = auth['host']
    nego_combo = (auth['auth'], auth['port']) # ("通信方式", port番号)

    if nego_combo[0] == "no-encrypt":
        popclient = poplib.POP3(host, nego_combo[1], timeout=10)
    elif nego_combo[0] == "starttls":
        context = ssl.create_default_context()
        popclient = poplib.POP3(host, nego_combo[1], timeout=10)
        popclient.stls(context)
    elif nego_combo[0] == "ssl":
        context = ssl.create_default_context()
        popclient = poplib.POP3_SSL(host, nego_combo[1], timeout=10, context=context)
    popclient.set_debuglevel(2)

    username = auth['username']
    password = auth['password']
    auth_method = auth['method']

    if auth_method == "user":
        popclient.user(username)
        popclient.pass_(password)
    elif auth_method == "apop":
        # Gmailはnot supported
        # yahooはnot supported
        popclient.apop(username, password)
    elif auth_method == "rpop":
        # Gmailはできない
        # yahooはできない
        popclient.rpop(username)
        popclient.pass_(password)


    download_num = 10
    msg_list = [] # 取得したMIMEメッセージを格納するリスト
    msg_num = popclient.stat()[0]  # POP3サーバに存在するメールの数を取得
    # msg_num = popclient.list(1)  # POP3サーバに存在するメールの数を取得
    # print(auth)
    if msg_num <= download_num:
        download_num = msg_num
    for i in range(download_num):
        msg_bytes = b""
        for line in popclient.retr(download_num)[1]:
            msg_bytes += line + b"\n"
        # print(email.message_from_bytes(msg_bytes))
        msg_list.append(email.message_from_bytes(msg_bytes))
    popclient.quit()

    result = []
    for msg in msg_list:
        mail = {}

        mail['from'] = get_header(msg, 'From')
        mail['to'] = get_header(msg, 'To')
        mail['date'] = get_header(msg, 'Date')
        cc = get_header(msg, 'Cc')
        if cc is not None:
            mail['cc'] = cc
        bcc = get_header(msg, 'Bcc')
        if bcc is not None:
            mail['bcc'] = bcc
        sub = get_header(msg, 'Subject')
        if sub is not None:
            mail['subject'] = sub

        mail['content'] = get_content(msg)

    result.append(mail)

    print('Get Mail Pop3 End !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    return result

# ヘッダを取得
def get_header(msg, name):
    header = ''
    if msg[name]:
        for tup in decode_header(str(msg[name])):
            if type(tup[0]) is bytes:
                charset = tup[1]
                if charset:
                    header += tup[0].decode(tup[1])
                else:
                    header += tup[0].decode()
            elif type(tup[0]) is str:
                header += tup[0]
    return header

def get_content(msg):
    charset = msg.get_content_charset()
    payload = msg.get_payload(decode=True)
    try:
        if payload:
            if charset:
                return payload.decode(charset)
            else:
                return payload.decode()
        else:
            return ""
    except:
        return payload