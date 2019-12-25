# -*- coding: UTF-8 -*-
import json
from flask import Blueprint, request, make_response, render_template
import pyexcel as pe
import openpyxl
from pyexcel.cookbook import update_rows

from utils.cm.agent import parse_http_accept_language
from utils.cm.files import get_dir, delete_dir, make_dir_local, delete_file
from utils.viewer.excel import set_book_data, sum_row, sum_array

app = Blueprint('excelapi', __name__)

@app.route('/excelviewer', methods=[ 'GET' ])
def excel_viewer():
    src = 'data/viewer/report_00.xlsx'

    html = 'excel/' + get_dir(None) + '.handsontable.html'
    dest = 'templates/' + html
    css = 'static/css/handsontable.full.min.css'
    js = 'static/js/handsontable.full.min.js'

    book = pe.get_book(file_name=src, skip_hidden_sheets=False)
    book.save_as(dest, readOnly=False, js_url=js, css_url=css)
    # pe.save_as(file_name=src, dest_file_name=dest)

    html = render_template(html)
    delete_file(dest)
    return html

@app.route('/viewer', methods=[ 'GET' ])
def viewer():
    src = 'data/viewer/report_00.xlsx'
    dir = get_dir(None)
    html = 'excel/' + dir + '/viewer.handsontable.html'
    tdir = 'templates/excel/' + dir
    tdir = make_dir_local(tdir)

    try:
        book = openpyxl.load_workbook(src)
        # set_book_data(book)
        for sn in book.sheetnames:
            sheet = book[sn]
            rIdx = 0
            maxr = len(list(sheet.rows))
            sa = []
            for row in sheet.rows:
                if rIdx >= (maxr - 1):
                    row[1].value = sum_array(sa)
                    # row[1].value = sum(sa)
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

        user_src = tdir + '/report_00.xlsx'
        book.save(user_src)

        dest = tdir + '/viewer.handsontable.html'
        css = 'static/css/handsontable.full.min.css'
        js = 'static/js/handsontable.full.min.js'
        book = pe.get_book(file_name=user_src, skip_hidden_sheets=False)
        book.save_as(dest, readOnly=False, js_url=js, css_url=css)
    except IOError as e:
        print("IOError:" + str(e))
    except FileNotFoundError as e:
        print("FileNotFoundError:" + str(e))

    html = render_template(html)
    delete_dir(tdir)
    return html
