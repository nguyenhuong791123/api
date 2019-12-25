# -*- coding: utf-8 -*-
from ..cm.utils import is_none, is_empty, is_exist

def set_book_data(book):
    if is_none(book) or is_none(book.sheetnames):
        return

    for sn in book.sheetnames:
        sheet = book[sn]
        rIdx = 0
        maxr = len(list(sheet.rows))
        sa = []
        for row in sheet.rows:
            print(row)
            if rIdx >= (maxr - 1):
                # row[1].value = sum(sa)
                row[1].value = sum_array(sa)
                break
            cIdx = 0
            if rIdx > 0:
                maxc = len(row)
                for cell in row:
                    if cIdx >= (maxc - 1):
                        cell.value = sum_row(row, 1, (maxc - 1))
                        # sr = [cell.value for cell in row]
                        # del sr[0]
                        # del sr[-1]
                        # sa.append(sum(sr))
                        # cell.value = sum(sr)
                        break
                    if cIdx > 0:
                        cell.value = cIdx
                    cIdx = cIdx + 1
                rIdx = rIdx + 1
    # return book

def sum_row(row, min, max):
    if is_none(row):
        return 0

    sr = []
    l = len(row)
    idx = 0
    for cell in row:
        if idx < min:
            continue
        elif idx > max:
            sr.append(cell.value)
            break
        else:
            sr.append(cell.value)

    return sum(sr)

def sum_array(arr):
    if is_none(arr) or len(arr) <= 0:
        return 0
    return sum(arr)