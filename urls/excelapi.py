# -*- coding: UTF-8 -*-
import os
import json
from copy import deepcopy
from flask import Blueprint, request, make_response, render_template
import pyexcel as pe
import openpyxl
from openpyxl.chart import BarChart, BarChart3D, LineChart, LineChart3D, PieChart, PieChart3D, AreaChart, AreaChart3D, Reference
from openpyxl.chart.series import DataPoint

from utils.cm.agent import parse_http_accept_language
from utils.cm.files import get_dir, delete_dir, make_dir_local
from utils.viewer.excel import sum_row, sum_cols, sum_array
from utils.viewer.func import EXCEL_FUNC, is_variable_exist
from utils.viewer.chart import write_chart

app = Blueprint('excelapi', __name__)

@app.route('/viewer', methods=[ 'GET' ])
def excel_viewer():
    path = 'data/viewer/report_00.xlsx'
    dir = get_dir(None)
    html = 'excel/' + dir + '/viewer.handsontable.html'
    tdir = 'templates/excel/' + dir
    tdir = make_dir_local(tdir)
    objs = []

    try:
        book = openpyxl.load_workbook(path)
        sheetnames = book.get_sheet_names()
        sIdx = 0
        for sn in book.sheetnames:
            sheet = book[sn]
            rIdx = 0
            maxr = len(list(sheet.rows))
            maxc = 0
            sa = []
            vertical = []
            horizontal = []
            arrays = []
            for row in sheet.rows:
                if rIdx >= (maxr - 1):
                    for r in range(len(row)):
                        if r > 0 and is_variable_exist(EXCEL_FUNC, row[r].value):
                            row[r].value = sum_cols(sheet, r)

                    print(vertical)
                    print(horizontal)
                    print(arrays)
                    sheetname = sheetnames[sIdx]
                    obj = {}
                    obj['sheet'] = sheetname
                    obj['vertical'] = vertical
                    obj['horizontal'] = horizontal
                    obj['datas'] = arrays
                    objs.append(obj)
                    pos = 1
                    # if True:
                    #     position = str(((maxr+2)*pos + (15*(pos-1))))
                    #     categories = Reference(sheet, min_col=1, min_row=2, max_row=maxr)
                    #     datas = Reference(sheet, min_col=2, min_row=1, max_col=(maxc - 1), max_row=(maxr - 1))
                    #     area = write_chart(AreaChart(), categories, datas, sheetname, 10)
                    #     sheet.add_chart(area, "B" + position)
                    #     area3d = write_chart(AreaChart3D(), categories, datas, sheetname, 10)
                    #     sheet.add_chart(area3d, "K" + position)
                    #     pos = pos + 1

                    if True:
                        position = str(((maxr+2)*pos + (15*(pos-1))))
                        categories =  Reference(sheet, min_col=1, min_row=2, max_row=maxr)
                        datas =  Reference(sheet, min_col=2, max_col=(maxc - 1), min_row=1, max_row=(maxr - 1))
                        line = write_chart(LineChart(), categories, datas, sheetname, 10)
                        sheet.add_chart(line, "B" + position)
                        line3d = write_chart(LineChart3D(), categories, datas, sheetname, 10)
                        sheet.add_chart(line3d, "K" + position)
                        pos = pos + 1

                    # if True:
                    #     position = str(((maxr+2)*pos + (15*(pos-1))))
                    #     categories = Reference(sheet, min_col=1, max_col=1, min_row=maxr, max_row=maxr)
                    #     datas = Reference(sheet, min_col=2, max_col=(maxc - 1), min_row=2, max_row=(maxr - 1))
                    #     chart = write_chart(BarChart(), categories, datas, sheetname, 10)
                    #     sheet.add_chart(chart, "B" + position)
                    #     # chart3d = write_chart(BarChart3D(), categories, datas, sheetname, 10)
                    #     # sheet.add_chart(chart3d, "K" + position)
                    #     pos = pos + 1

                    if True:
                        position = str(((maxr+2)*pos + (15*(pos-1))))
                        categories = Reference(sheet, min_col=1, min_row=2, max_row=maxr)
                        datas = Reference(sheet, min_col=2, max_col=(maxc - 1), min_row=1, max_row=(maxr - 1))
                        pie = write_chart(PieChart(), categories, datas, sheetname, 10)
                        sheet.add_chart(pie, "B" + position)
                        pie3d = write_chart(PieChart3D(), categories, datas, sheetname, 10)
                        sheet.add_chart(pie3d, "K" + position)

                    break

                cIdx = 0
                maxc = len(row)
                array = []
                if rIdx > 0:
                    for cell in row:
                        if cIdx <= 0:
                            vertical.append(cell.value)
                            cIdx = cIdx + 1
                            continue

                        sr = sum_row(row, cell.value)
                        if sr is not None:
                            cell.value = sr
                            sa.append(sr)
                        else:
                            cell.value = (cIdx + rIdx)
                            array.append(cell.value)
                        cIdx = cIdx + 1
                    arrays.append(array)
                else:
                    for cell in row:
                        if cIdx <= 0:
                            cIdx = cIdx + 1
                            continue
                        if cIdx == (maxc - 1):
                            break
                        horizontal.append(cell.value)
                        cIdx = cIdx + 1
                rIdx = rIdx + 1
            sIdx = sIdx + 1

        user_src = tdir + '/report_00.xlsx'
        book.save(user_src)

        dest = tdir + '/viewer.handsontable.html'
        css = 'static/css/handsontable.full.min.css'
        js = 'static/js/handsontable.full.min.js'
        book = pe.get_book(file_name=user_src, skip_hidden_sheets=False)
        # print(book)
        book.save_as(dest, readOnly=False, js_url=js, css_url=css)
    except IOError as e:
        print("IOError:" + str(e))
    except FileNotFoundError as e:
        print("FileNotFoundError:" + str(e))

    # objs = json.dumps({ 'items': objs })
    html = render_template('excel/viewer.html', excel_viewer=html, objs={ 'items': objs })
    delete_dir(tdir)
    return html
    # response = make_response()
    # response.data = open(user_src, 'rb').read()
    # response.headers['Content-Disposition'] = "attachment; filename=report_00.xlsx"
    # response.mimetype = 'application/vnd.ms-excel.sheet.macroEnabled.12'
    # return response

