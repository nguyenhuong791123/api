# -*- coding: UTF-8 -*-
from utils.cm.utils import is_empty 

def check_auth(apikey, username, password):
    if username == 'admin' and password == 'admin':
        return username
    elif apikey == 'apikey':
        return apikey
    else:
        return None