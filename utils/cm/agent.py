# -*- coding: UTF-8 -*-
import re
import locale
import json

LANGUAGE_CODES = [ "en", "ja", "vi" ]
def to_locale(language, to_lower=False):
    p = language.find('-')
    if p >= 0:
        if to_lower:
            return language[:p].lower()+'_'+language[p+1:].lower()
        else:
            # Get correct locale for sr-latn
            if len(language[p+1:]) > 2:
                return language[:p].lower()+'_'+language[p+1].upper()+language[p+2:].lower()
            return language[:p].lower()+'_'+language[p+1:].upper()
    else:
        return language.lower()

def parse_accept_lang_header(lang_string):
    # From django.utils.translation.trans_real.parse_accept_lang_header
    accept_language_re = re.compile(r'''
            ([A-Za-z]{1,8}(?:-[A-Za-z]{1,8})*|\*)         # "en", "en-au", "x-y-z", "*"
            (?:\s*;\s*q=(0(?:\.\d{,3})?|1(?:.0{,3})?))?   # Optional "q=1.00", "q=0.8"
            (?:\s*,\s*|$)                                 # Multiple accepts per header.
            ''', re.VERBOSE)

    result = []
    pieces = accept_language_re.split(lang_string)
    if pieces[-1]:
        return []
    for i in range(0, len(pieces) - 1, 3):
        first, lang, priority = pieces[i : i + 3]
        if first:
            return []
        priority = priority and float(priority) or 1.0
        result.append((lang, priority))
    result.sort(key=lambda k: k[1], reverse=True)
    return result

def normalize_language(language):
    return locale.locale_alias.get(to_locale(language, True))

def is_language_supported(language, supported_languages=None):
    if supported_languages is None:
        supported_languages = LANGUAGE_CODES
    if not language:
        return None
    normalized = normalize_language(language)
    if not normalized:
        return None
    # Remove the default encoding from locale_alias.
    normalized = normalized.split('.')[0]
    for lang in (normalized, normalized.split('_')[0]):
        if lang.lower() in supported_languages:
            return lang
    return None

def parse_http_accept_language(accept):
    for accept_lang, unused in parse_accept_lang_header(accept):
        if accept_lang == '*':
            break

        normalized = locale.locale_alias.get(to_locale(accept_lang, True))
        if not normalized:
            continue
        # Remove the default encoding from locale_alias.
        normalized = normalized.split('.')[0]

        for lang_code in (accept_lang, accept_lang.split('-')[0]):
            lang_code = lang_code.lower()
            if lang_code in LANGUAGE_CODES:
                return lang_code
    return None

class UserAgent():
    def __init__(self, req):
        self.host = req.host
        self.path = req.path
        self.method = req.method
        self.remote_addr = req.remote_addr
        self.user_agent = req.user_agent
        self.cookies = req.cookies
        self.accept_languages = req.accept_languages
        self.auth_api_key = None

    def setAuth(self, authkey):
        self.auth_api_key = authkey

    def toJson(self):
        obj = {}
        obj['auth_api_key'] = self.auth_api_key
        obj['host'] = self.host
        obj['path'] = self.path
        obj['method'] = self.method
        obj['remote_addr'] = self.remote_addr
        obj['user_agent'] = str(self.user_agent)
        obj['cookies'] = self.cookies
        obj['accept_languages'] = str(self.accept_languages)
        return obj