# -*- coding: UTF-8 -*-
import os
import xlrd

def readme_read(sheet):
    result = []
    path = 'readme/readme.xlsx'
    if sheet is None or os.path.isfile(path) == False:
        return result

    wb = xlrd.open_workbook(path)
    if sheet not in wb.sheet_names():
        result.append('Not found document ' + sheet + ' API !!!')
        return result

    sh = wb.sheet_by_name(sheet)
    for col in range(sh.ncols):
        if col > 0:
            continue
        for row in range(sh.nrows):
            result.append(sh.cell(row, col).value)
    
    return result


