__author__ = 'Tang'

import os
import base64
import cgi
import magic
from response import Response
from conf import REPO_PATH, ACCEPT_IMG, TEMP_PATH, STATIC_PATH
import tempfile
import subprocess
from PIL import Image

MIME_TABLE = {'.txt': 'text/plain',
              '.html': 'text/html',
              '.css': 'text/css',
              '.js': 'application/javascript',
              '.jpg': 'image/jpeg',
              '.jpeg': 'image/jpeg',
              '.png': 'image/png',
              '.gif': 'image/gif'}

IMG_PATH = os.path.join(STATIC_PATH, 'pic')


def get_static(path, env):
    path = os.path.normpath(os.path.join(REPO_PATH, path[1:len(path)]))
    file_type = "application/octet-stream"
    if os.path.exists(path):
        f = open(path, 'rb')
        content = f.read()
        f.close()
        name, ext = os.path.splitext(path)
        if ext in MIME_TABLE:
            file_type = MIME_TABLE[ext]
        return Response(content, ctype=file_type)
    else:
        return None


def get_uploaded_img(env):
    if env['REQUEST_METHOD'] != 'POST':
        return None

    form = cgi.FieldStorage(fp=env['wsgi.input'], environ=env, keep_blank_values=True)
    pic = form['img']
    filename, file_extension = os.path.splitext(pic.filename)
    data = pic.value
    img_type = magic.from_buffer(data, mime=True)
    if img_type not in ACCEPT_IMG:
        return False
    if file_extension not in MIME_TABLE or MIME_TABLE[file_extension] != img_type:
        return False
    img_uri = encode_data_uri(data, img_type)
    return img_uri


def encode_data_uri(data, img_type):
    if img_type not in ACCEPT_IMG:
        return None
    else:
        return 'data:' + img_type + ';base64,' + base64.b64encode(data)


def decode_data_uri(data):
    start = end = 5
    while data[end] != ';':
        end += 1
    img_type = data[start:end]
    while data[end] != ',':
        end += 1
    img = base64.b64decode(data[end+1:])
    return img, img_type


def img_filter(filter_type, data, img_type):
    tmp_file = tempfile.NamedTemporaryFile(delete=False, dir=TEMP_PATH, suffix=ACCEPT_IMG[img_type])
    tmp_name = tmp_file.name
    tmp_file.write(data)
    tmp_file.close()

    if filter_type == 'border':
        subprocess.call(['convert', tmp_name, '-bordercolor', 'black', '-border', '20', tmp_name])
    elif filter_type == 'lomo':
        subprocess.call(['convert', tmp_name, '-channel', 'R', '-level', '33%', '-channel', 'G', '-level', '33%', tmp_name])
    elif filter_type == 'lens-flare':
        tmp_img = Image.open(tmp_name)
        width = tmp_img.size[0]
        height = tmp_img.size[1]
        tmp_img.close()
        require_file = get_flare(width, height)
        subprocess.call(['composite', '-compose',  'screen', '-gravity', 'northwest', require_file, tmp_name, tmp_name])
    elif filter_type == 'black-white':
        tmp_img = Image.open(tmp_name)
        width = tmp_img.size[0]
        height = tmp_img.size[1]
        tmp_img.close()
        require_file = get_bwgrad(width, height)
        subprocess.call(['convert', tmp_name, '-type', 'grayscale', tmp_name])
        subprocess.call(['composite', '-compose', 'softlight', '-gravity', 'center', require_file, tmp_name, tmp_name])
    elif filter_type == 'blur':
        subprocess.call(['convert', tmp_name, '-blur', '0.5x2', tmp_name])

    tmp_file = open(tmp_name, 'rb')
    data = tmp_file.read()
    tmp_file.close()
    os.remove(tmp_name)
    return data, img_type


def img_annotate(font_type, font_size, position, content, data, img_type):
    tmp_file = tempfile.NamedTemporaryFile(delete=False, dir=TEMP_PATH, suffix=ACCEPT_IMG[img_type])
    tmp_name = tmp_file.name
    tmp_file.write(data)
    tmp_file.close()
    if position == 'top':
        subprocess.call(['convert', tmp_name, '-background', 'black', '-fill', '#ffffff', '-pointsize', str(font_size),
                        '-font', font_type, 'label:'+content, '+swap', '-gravity', 'center', '-append', tmp_name])
    elif position == 'bottom':
        subprocess.call(['convert', tmp_name, '-background', 'black', '-fill', '#ffffff', '-pointsize', str(font_size),
                        '-font', font_type, 'label:'+content, '-gravity', 'center', '-append', tmp_name])

    tmp_file = open(tmp_name, 'rb')
    data = tmp_file.read()
    tmp_file.close()
    os.remove(tmp_name)
    return data, img_type


def get_flare(width, height):
    require_file = os.path.join(IMG_PATH, "lensflare_%s_%s.png" % (str(width), str(height)))
    if not os.path.exists(require_file):
        flare = Image.open(os.path.join(IMG_PATH, 'lensflare.png'))
        flare = flare.resize((width, height))
        flare.save(require_file)
    return require_file


def get_bwgrad(width, height):
    require_file = os.path.join(IMG_PATH, "bwgrad_%s_%s.png" % (str(width), str(height)))
    if not os.path.exists(require_file):
        grad = Image.open(os.path.join(IMG_PATH, 'bwgrad.png'))
        grad = grad.resize((width, height))
        grad.save(require_file)
    return require_file