# -*- coding: UTF-8 -*-
import base64
from imap_tools import MailBox, Q
from ..cm.utils import is_empty, is_exist
from ..cm.dates import get_datetime

def get_imap(auth):
    print('Get Mail Imap Start !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    mbox = get_mbox(auth)
    result = []
    for m in mbox.fetch():
        obj = {}
        obj['id'] = m.uid
        obj['subject'] = m.subject
        obj['from'] = m.from_
        obj['to'] = m.to
        obj['cc'] = m.cc
        obj['bcc'] = m.bcc
        obj['date'] = m.date
        obj['text'] = m.text
        obj['html'] = m.html
        obj['flags'] = m.flags
        obj['headers'] = m.headers
        att = m.attachments
        if att is not None and len(att) > 0:
            atts = []
            for at in att:
                atts.append({ 'filename': at[0], 'data': str(at[1]) })
            if len(atts) > 0:
                obj['attachments'] = atts

        result.append(obj)

    print('Get Mail Imap End !!![' + get_datetime('%Y-%m-%d %H:%M:%S', None) + ']')
    return result

def get_mbox(auth):
    mbox = MailBox(auth['host'], auth['port'])
    if (is_exist(auth, 'box') and is_empty(auth['box']) == False):
        box = auth['box']
    mbox.login(auth['username'], auth['password'], initial_folder=box)
    return mbox
