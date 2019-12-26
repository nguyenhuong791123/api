# -*- coding: utf-8 -*-
from ..cm.utils import is_none, is_empty

def write_chart(chart, categories, datas, title, height):
    if is_none(chart) or is_none(categories) or is_none(datas):
        return

    if is_none(height) == False:
        chart.height = height
    if is_empty(title) == False:
        chart.title = title

    chart.add_data(datas, titles_from_data = True)
    chart.set_categories(categories)
    return chart