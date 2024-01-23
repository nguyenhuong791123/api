# -*- coding: utf-8 -*-
import openpyxl

from .func import EXCEL_FUNC, is_variable_exist, set_range
from ..cm.utils import is_none

def sum_row(row, cell_value):
    if is_none(row):
        return 0

    efs = EXCEL_FUNC()
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

def sum_cols(sheet, idx):
    if is_none(sheet):
        return 0

    sr = []
    for row in sheet.rows:
        for c in range(len(row)):
            value = row[c].value
            if c == idx and str(value).isdigit():
                sr.append(value)

    return sum(sr)

def sum_array(arr):
    if is_none(arr) or len(arr) <= 0:
        return 0
    return sum(arr)
