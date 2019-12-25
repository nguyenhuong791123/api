# -*- coding: UTF-8 -*-
import json
from flask import Blueprint, request, make_response, render_template
import pyexcel as pe
import openpyxl

from utils.cm.agent import parse_http_accept_language
from utils.cm.files import get_dir, delete_dir, make_dir_local, delete_file
from utils.viewer.excel import sum_row, sum_array

app = Blueprint('excelapi', __name__)

@app.route('/viewer', methods=[ 'GET' ])
def excel_viewer():
    path = 'data/viewer/report_00.xlsx'
    dir = get_dir(None)
    html = 'excel/' + dir + '/viewer.handsontable.html'
    tdir = 'templates/excel/' + dir
    tdir = make_dir_local(tdir)

    try:
        book = openpyxl.load_workbook(path)
        for sn in book.sheetnames:
            sheet = book[sn]
            rIdx = 0
            maxr = len(list(sheet.rows))
            sa = []
            for row in sheet.rows:
                if rIdx >= (maxr - 1):
                    row[1].value = sum_array(sa)
                    break
                cIdx = 0
                if rIdx > 0:
                    maxc = len(row)
                    for cell in row:
                        if cIdx <= 0:
                            cIdx = cIdx + 1
                            continue

                        sr = sum_row(row, cell.value)
                        if sr is not None:
                            cell.value = sr
                            sa.append(sr)
                        else:
                            cell.value = cIdx
                        cIdx = cIdx + 1
                rIdx = rIdx + 1

        user_src = tdir + '/report_00.xlsx'
        book.save(user_src)

        dest = tdir + '/viewer.handsontable.html'
        css = 'static/css/handsontable.full.min.css'
        js = 'static/js/handsontable.full.min.js'
        book = pe.get_book(file_name=user_src, skip_hidden_sheets=False)
        print(book)
        book.save_as(dest, readOnly=False, js_url=js, css_url=css)
    except IOError as e:
        print("IOError:" + str(e))
    except FileNotFoundError as e:
        print("FileNotFoundError:" + str(e))

    html = render_template(html)
    delete_dir(tdir)
    return html
