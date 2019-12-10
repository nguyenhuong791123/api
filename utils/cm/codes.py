# -*- coding: utf-8 -*-
import os
import barcode
from barcode import generate
from barcode.writer import ImageWriter
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import qrcode
import qrcode.image.svg
from PIL import Image

from .utils import is_empty, is_exist, convert_file_to_b64_string
from .files import delete_dir, delete_file, get_filename, get_ext

def create_code(flag, code, value, outpath, filename, options):
    result = {}
    try:
        ismode = is_bar_code(code)
        ext = get_ext(filename)
        if ismode:
            fullpath = None
            if is_empty(ext) == False and ext == 'png':
                bci = barcode.get(code, value, writer=ImageWriter())
                fullpath = bci.save(os.path.join(outpath, filename.split('.')[0]))
            else:
                code = code.upper()
                fullpath = generate(code, value, output=os.path.join(outpath, filename))
            if fullpath is not None:
                filename = get_filename(fullpath)
        else:
            opts = QrCode()
            opts.set_options(options)
            # print(opts.__dict__)
            factory = None
            if is_empty(opts.factory) == False:
                factory = opts.factory
            # print(factory)
            img = None
            qr = None
            if is_empty(opts.box_size) == False and is_empty(opts.border) == False:
                qr = qrcode.QRCode(version=opts.version, error_correction=opts.error_correction, box_size=opts.box_size, border=opts.border)
            elif is_empty(opts.box_size) == False and is_empty(opts.border):
                qr = qrcode.QRCode(version=opts.version, error_correction=opts.error_correction, box_size=opts.box_size)
            elif is_empty(opts.box_size) and is_empty(opts.border) == False:
                qr = qrcode.QRCode(version=opts.version, error_correction=opts.error_correction, border=opts.border)
            else:
                qr = qrcode.QRCode(version=opts.version, error_correction=opts.error_correction)

            if qr is None:
                result['msg'] = 'Not Create QRCode !!!'
                return result

            if factory is not None:
                img = qr.make(value, image_factory=factory)
            else:
                qr.add_data(value)
                qr.make(fit=True)
                if is_empty(opts.fill_color) == False and is_empty(opts.back_color) == False:
                    img = qr.make_image(fill_color=opts.fill_color, back_color=opts.back_color)
                elif is_empty(opts.fill_color) == False and is_empty(opts.back_color):
                    img = qr.make_image(fill_color=opts.fill_color)
                elif is_empty(opts.fill_color) and is_empty(opts.back_color) == False:
                    img = qr.make_image(fill_color=opts.back_color)
                else:
                    img = qr.make_image()

            if qr is None:
                result['msg'] = 'Not Create Image !!!'
                return result

            # img = qr.make_image()
            if is_empty(ext):
                filename = filename + '.png'
            if img is not None:
                img.save(os.path.join(outpath, filename))

        result['filename'] = filename
    except Exception as ex:
        result['msg'] = str(ex)
    except IOError as err:
        result['msg'] = str(err)
    finally:
        result['path'] = outpath
        local = os.path.join(outpath, filename)
        if flag == 'json' and os.path.isfile(local):
            b64 = str(convert_file_to_b64_string(local))
            if b64 is not None:
                result['data'] = b64[2:(len(b64)-1)]

    return result

def get_code(outpath, filename, symbols):
    result = {}
    try:
        fullpath = os.path.join(outpath, filename)
        img = Image.open(fullpath)
        print(os.getcwd())
        if symbols is not None:
            data = decode(img, symbols=[ symbols ])
        else:
            data = decode(img)
        if data is not None and is_empty(data[0][0]) == False:
            result['data'] = data[0][0].decode('utf-8', 'ignore')
    except Exception as ex:
        result['msg'] = str(ex)
    except IOError as err:
        result['msg'] = str(err)
    finally:
        result['filename'] = filename

    return result

def is_bar_code(code):
    if is_empty(code):
        return False
    # CALLABLES = types.FunctionType, types.MethodType
    codes = BarCodes()
    for key, value in codes.__dict__.items():
        # if isinstance(value, CALLABLES) or is_empty(key) or key != code:
        if is_empty(value) or value != code:
            continue
        return True
    return False

def get_zbar_symbol(code):
    bar = is_bar_code(code)
    if bar == False or code != 'qr':
        return None

    if code == 'qr':
       return ZBarSymbol.QRCODE
    else:
        codes = BarCodes()
        if code == codes.code39:
            return ZBarSymbol.CODE39
        elif code == codes.code128:
            return ZBarSymbol.CODE128
        elif code == codes.ean:
            return ZBarSymbol.EAN
        elif code == codes.ean13:
            return ZBarSymbol.EAN13
        elif code == codes.gs1:
            return ZBarSymbol.GS1
        elif code == codes.gtin:
            return ZBarSymbol.GTIN
        elif code == codes.isbn:
            return ZBarSymbol.ISBN
        elif code == codes.isbn10:
            return ZBarSymbol.ISBN10
        elif code == codes.isbn13:
            return ZBarSymbol.ISBN13
        elif code == codes.issn:
            return ZBarSymbol.ISSN
        elif code == codes.jan:
            return ZBarSymbol.JAN
        elif code == codes.pzn:
            return ZBarSymbol.PZN
        elif code == codes.upc:
            return ZBarSymbol.UPC
        elif code == codes.upca:
            return ZBarSymbol.UPCA
        else:
            return None

    return None

class QrCode():
    def __init__(self):
        self.version = 1
        self.error_correction = qrcode.constants.ERROR_CORRECT_L
        self.factory = None
        self.box_size = None
        self.border = None
        self.fill_color = None
        self.back_color = None

    def set_options(self, ops, ec=qrcode.constants.ERROR_CORRECT_L):
        self.error_correction = ec
        if ops is None:
            return
        if is_exist(ops, 'version') and ops['version'] is not None:
            self.version = 1
        if is_exist(ops, 'factory') and is_empty(ops['factory']) == False:
            fac = ops['factory']
            if fac == 'basic':
                self.factory = qrcode.image.svg.SvgImage
            elif fac == 'fragment':
                self.factory = qrcode.image.svg.SvgFragmentImage
            else:
                self.factory = qrcode.image.svg.SvgPathImage
        if is_exist(ops, 'box_size') and ops['box_size'] is not None:
            self.box_size = 10
        if is_exist(ops, 'border') and ops['border'] is not None:
            self.border = 2
        if is_exist(ops, 'fill_color') and is_empty(ops['fill_color']) == False:
            self.fill_color = 'black'
        if is_exist(ops, 'back_color') and is_empty(ops['back_color']) == False:
            self.back_color = 'white'

class BarCodes():
    def __init__(self):
        self.code39 = 'code39'
        self.code128 = 'code128'
        self.ean = 'ean'
        self.ean13 = 'ean13'
        self.ean8 = 'ean8'
        self.gs1 = 'gs1'
        self.gtin = 'gtin'
        self.isbn = 'isbn'
        self.isbn10 = 'isbn10'
        self.isbn13 = 'isbn13'
        self.issn = 'issn'
        self.jan = 'jan'
        self.pzn = 'pzn'
        self.upc = 'upc'
        self.upca = 'upca'