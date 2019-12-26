# -*- coding: UTF-8 -*-
import os
import json
from flask import Blueprint, request, make_response, render_template
import pyexcel as pe
import openpyxl
from openpyxl.chart import BarChart, LineChart, PieChart, ProjectedPieChart, Reference, Series
from openpyxl.chart.series import DataPoint

from utils.cm.agent import parse_http_accept_language
from utils.cm.files import get_dir, delete_dir, make_dir_local
from utils.viewer.excel import sum_row, sum_cols, sum_array
from utils.viewer.func import EXCEL_FUNC, is_variable_exist

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
        sheetnames = book.get_sheet_names()
        sIdx = 0
        for sn in book.sheetnames:
            sheet = book[sn]
            rIdx = 0
            maxr = len(list(sheet.rows))
            maxc = 0
            sa = []
            for row in sheet.rows:
                if rIdx >= (maxr - 1):
                    for r in range(len(row)):
                        if r > 0 and is_variable_exist(EXCEL_FUNC, row[r].value):
                            row[r].value = sum_cols(sheet, r)

                    categories = Reference(sheet, min_col=1, max_col=1, min_row=maxr, max_row=maxr)
                    datas = Reference(sheet, min_col=2, max_col=(maxc - 1), min_row=2, max_row=(maxr - 1))
                    chart = BarChart()
                    chart.title = sheetnames[sIdx]
                    chart.add_data(datas, titles_from_data = True)
                    chart.set_categories(categories)
                    sheet.add_chart(chart, "B" + str((maxr + 2)))

                    line = LineChart()
                    line.title = sheetnames[sIdx]
                    line.add_data(datas, titles_from_data = True)
                    line.set_categories(categories)
                    for ser in range(len(line.series)):
                        s = line.series[ser]
                        # s.smooth = True
                        s.marker.symbol = "triangle"
                        s.marker.graphicalProperties.solidFill = "FF0000"
                        s.marker.graphicalProperties.line.solidFill = "FF0000"
                    sheet.add_chart(line, "K" + str((maxr + 2)))

                    pie = PieChart()
                    pie.title = sheetnames[sIdx]
                    pie.add_data(datas, titles_from_data = True)
                    pie.set_categories(categories)
                    slice = DataPoint(idx=0, explosion=20)
                    pie.series[0].data_points = [slice]
                    sheet.add_chart(pie, "B" + str((maxr*2 + 15)))

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
        # print(book)
        book.save_as(dest, readOnly=False, js_url=js, css_url=css)
    except IOError as e:
        print("IOError:" + str(e))
    except FileNotFoundError as e:
        print("FileNotFoundError:" + str(e))

    html = render_template('excel/viewer.html', excel_viewer=html)
    # delete_dir(tdir)
    return html
