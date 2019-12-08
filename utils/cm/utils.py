
# -*- coding: UTF-8 -*-
import os
import json
import base64
import re
import datetime
import shutil

def is_none(obj):
    if obj is None:
        return True
    return False

def is_empty(val):
    return (val is None or len(val) <= 0)

def is_mail(val):
    val = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', val)
    return (val is not None)

def is_exist(obj, key):
    try:
        return key in obj.keys()
    except Exception as e:
        print(str(e))
        return False

def is_json(obj):
    try:
        keys = obj.keys()
        if keys is None:
            data = json.load(obj)
            keys = data.keys()
    except Exception as ex:
        print(str(ex))
    except json.JSONDecodeError as e:
        print('JSONDecodeError: ', str(e))
    return (keys is not None and len(keys) > 0)

def is_type(obj, istype):
    if is_empty(obj):
        return None
    val = str(type(obj)).replace("<class '", "").replace("'>", "")
    return (val == istype) # 'str', 'int', 'list', 'bool'

def convert_file_to_b64_string(fullpath):
    with open(fullpath, "rb") as f:
        return base64.b64encode(f.read())

def convert_b64_string_to_file(s, outpath):
    with open(outpath, "wb") as f:
        f.write(base64.b64decode(s))
