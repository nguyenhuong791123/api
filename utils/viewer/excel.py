# -*- coding: utf-8 -*-
import openpyxl

from ..cm.utils import is_none, is_empty, is_exist, del_number

def sum_row(row, cell_value):
    if is_none(row):
        return 0

    efs = E_FS()
    # efs.double_headers(3)
    # print(efs.headers)
    ranges = set_range(efs, cell_value)
    if ranges is None or len(ranges) <= 0:
        return None

    sr = []
    for c in range(len(row)):
        if c in ranges:
            sr.append(row[c].value)

    return sum(sr)

def sum_array(arr):
    if is_none(arr) or len(arr) <= 0:
        return 0
    return sum(arr)

class E_FS():
    def __init__(self):
        self.headers = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.sum    = '=SUM('
        self.sumif  = '=SUMIF('
        self.sumifs = '=SUMIFS('
        self.max    = '=MAX('
        self.maxa   = '=MAXA('
        self.maxifs = '=MAXIFS('
        self.min    = '=MIN('
        self.mina   = '=MINA('
        self.minifs = '=MINIFS('

    def double_headers(self, level):
        arr = list(self.headers)
        for l in range(level):
            for a in arr:
                self.headers = self.headers + (arr[l] + a)

def is_variable_exist(cls, fs):
    if is_empty(fs):
        return False

    for key, value in cls.__dict__.items():
        if fs.startswith(value) > -1:
            return True
    return False

def set_range(cls, fs):
    if is_variable_exist(cls, fs) == False or fs.find('(') == -1:
        return None

    ranges = []
    arr = fs[(fs.index('(') + 1):(len(fs) - 1)]
    if arr.index(':') > -1:
        arr = arr.split(':')
        min = cls.headers.index(del_number(arr[0]))
        max = cls.headers.index(del_number(arr[1]))
        for idx in range(min, max + 1):
            ranges.append(idx)

    elif arr.index(',') > -1:
        arr = arr.split(',')
        for a in arr:
            idx = cls.headers.index(del_number(a))
            if idx == -1:
                continue
            ranges.append(idx)

    return ranges

