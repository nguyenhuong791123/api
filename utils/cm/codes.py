# -*- coding: utf-8 -*-
from barcode import generate
import qrcode
import qrcode.image.svg

from .utils import is_empty, is_exist, convert_file_to_b64_string
from .files import delete_dir, delete_file


def create_code(flag, ismode, code, value, outpath, filename, options):
    result = {}
    try:
        os.chdir(outpath)
        if ismode:
            code = code.upper()
            filename = generate(code, value, output=filename)
        else:
            opts = QrCode()
            opts.set_options(options)
            qr = qrcode.QRCode(version=opts.version, error_correction=opts.error_correction, box_size=opts.box_size, border=opts.border)
            qr.add_data(value)
            qr.make(fit = True)

            img = None
            filename = filename + '.png'
            factory = opts.factory
            if factory is not None:
                img = qr.make_image(fill_color=opts.fill_color, back_color=opts.back_color, image_factory=factory)
            else:
                img = qr.make_image(fill_color=opts.fill_color, back_color=opts.back_color)

            if img is not None:
                img.save(os.path.join(outpath, filename))

        result['filename'] = filename
    except Exception as ex:
        result['msg'] = str(ex)
    except IOError as err:
        result['msg'] = str(err)
    finally:
        os.chdir('../../')
        result['path'] = outpath
        local = os.path.join(outpath, filename)
        if flag == 'json' and os.path.isfile(local):
            b64 = str(convert_file_to_b64_string(local))
            if b64 is not None:
                result['data'] = b64[2:(len(b64)-1)]
            delete_file(local)

    return result

# def create_bar_code(flag, code, value, outpath, filename):
#     result = {}
#     try:
#         os.chdir(outpath)
#         code = code.upper()
#         filename = generate(code, value, output=filename)
#         result['filename'] = filename
#     except Exception as ex:
#         result['msg'] = str(ex)
#     except IOError as err:
#         result['msg'] = str(err)
#     finally:
#         os.chdir('../../')
#         result['path'] = outpath
#         local = os.path.join(outpath, filename)
#         if flag == 'json' and os.path.isfile(local):
#             b64 = str(convert_file_to_b64_string(local))
#             if b64 is not None:
#                 result['data'] = b64[2:(len(b64)-1)]

#     return result

# def create_qr_code(value, outpath, filename, options):
#     result = {}
#     qrops = QrCode()
#     try:
#         os.chdir(outpath)
#         qrops.set_options(options)
#         qr = qrcode.QRCode(
#             version=qrops.version
#             ,error_correction=qrcode.constants.ERROR_CORRECT_L
#             ,box_size=qrops.box_size
#             ,border=qrops.border)
#         qr.add_data(value)
#         qr.make(fit = True)

#         img = None
#         filename = filename + '.png'
#         factory = qrops.factory
#         if factory is not None:
#             img = qr.make_image(fill_color=qrops.fill_color, back_color=qrops.back_color, image_factory=factory)
#         else:
#             img = qr.make_image(fill_color=qrops.fill_color, back_color=qrops.back_color)

#         if img is not None:
#             img.save(os.path.join(outpath, filename))

#         result['filename'] = filename
#     except Exception as ex:
#         result['msg'] = str(ex)
#     except IOError as err:
#         result['msg'] = str(err)
#     finally:
#         os.chdir('../../')
#         result['path'] = outpath
#         local = os.path.join(outpath, filename)
#         if flag == 'json' and os.path.isfile(local):
#             b64 = str(convert_file_to_b64_string(local))
#             if b64 is not None:
#                 result['data'] = b64[2:(len(b64)-1)]

#     return result

def is_bar_code(mode):
    if is_empty(mode):
        return False
    # CALLABLES = types.FunctionType, types.MethodType
    for key, value in BarCodes().__dict__.items():
        if is_empty(key) or key != mode:
            continue
        return true
        # if not isinstance(value, CALLABLES):
            # print(key)

class QrCode():
    def __init__(self):
        self.version = 1
        self.factory = 'basic'
        self.error_correction = qrcode.constants.ERROR_CORRECT_L
        self.box_size = 10
        self.border = 4
        self.fill_color = 'black'
        self.back_color = 'white'

    def set_options(self, ops, ec=qrcode.constants.ERROR_CORRECT_L):
        self.error_correction = ec
        if is_exist(ops, 'version') and ops['version'] is not None:
            self.version = 1
        if is_exist(ops, 'factory') and is_empty(ops['factory']) == False:
            factory = ops['factory']
            if factory == 'basic':
                self.factory = qrcode.image.svg.SvgImage
            elif factory == 'fragment':
                self.factory = qrcode.image.svg.SvgFragmentImage
            else:
                self.factory = qrcode.image.svg.SvgPathImage
        if is_exist(ops, 'box_size') and ops['box_size'] is not None:
            self.box_size = 10
        if is_exist(ops, 'border') and ops['border'] is not None:
            self.border = 4
        if is_exist(ops, 'fill_color') and is_empty(ops['fill_color']) == False:
            self.fill_color = 'black'
        if is_exist(ops, 'back_color') and is_empty(ops['back_color']) == False:
            self.back_color = 'white'

class BarCodes():
    code39 = 'code39'
    code128 = 'code128'
    ean = 'ean'
    ean13 = 'ean13'
    ean8 = 'ean8'
    gs1 = 'gs1'
    gtin = 'gtin'
    isbn = 'isbn'
    isbn10 = 'isbn10'
    isbn13 = 'isbn13'
    issn = 'issn'
    jan = 'jan'
    pzn = 'pzn'
    upc = 'upc'
    upca = 'upca'