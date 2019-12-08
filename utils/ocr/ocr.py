# -*- coding: UTF-8 -*-
# tesseract_layoutの説明
# 0 = Orientation and script detection (OSD) only.
# 1 = Automatic page segmentation with OSD.
# 2 = Automatic page segmentation, but no OSD, or OCR
# 3 = Fully automatic page segmentation, but no OSD. (Default)
# 4 = Assume a single column of text of variable sizes.
# 5 = Assume a single uniform block of vertically aligned text.
# 6 = Assume a single uniform block of text.
# 7 = Treat the image as a single text line.
# 8 = Treat the image as a single word.
# 9 = Treat the image as a single word in a circle.
# 10 = Treat the image as a single character.
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from PIL import Image
import pyocr
# import argparse
# import cv2

from ..cm.utils import is_exist
from ..cm.files import make_dir_get_outpath, save_base64s, save_files, delete_dir

def img_to_text(files, language, layout):
    if files is None or len(files) <= 0:
        return None
    sfs = None
    outpath = make_dir_get_outpath('download')
    if is_exist(files[0], 'data'):
        sfs = save_base64s(files, outpath)
    else:
        sfs = save_files(files, outpath)
    if sfs is None or len(sfs) <= 0:
        return None

    result = []
    print(sfs)
    for file in sfs:
        filename = file['filename']
        fullpath = os.path.join(file['data'], filename)
        f = {}
        f['filename'] = filename
        f['data'] = get_text(fullpath, language, layout)
        result.append(f)

    # if os.path.isdir(outpath):
    #     delete_dir(outpath)

    return result

def get_text(stream, language, layout):
    # print(os.getcwd())
    # print(stream)
    if stream is None:
        return ''

    tools = pyocr.get_available_tools()
    assert(len(tools) != 0)
    tool = tools[0]

    if language is None:
        language = 'jpn'

    if layout is None:
        layout = 6

    res = None
    try:
        res = tool.image_to_string(
            Image.open(stream),
            lang=language,
            builder=pyocr.builders.TextBuilder(tesseract_layout=layout))
    except Exception as ex:
        print(str(ex))

    return res