__author__ = 'Tang'

import os
import base64
import cgi
import magic
from response import Response
from conf import REPO_PATH, ACCEPT_IMG

MIME_TABLE = {'.txt': 'text/plain',
              '.html': 'text/html',
              '.css': 'text/css',
              '.js': 'application/javascript',
              '.jpg': 'image/jpeg',
              '.jpeg': 'image/jpeg'}


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

    if file_extension not in MIME_TABLE or MIME_TABLE[file_extension] != img_type:
        return None
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
    img_type = data[start:end-start]
    while data[end] != ',':
        end += 1
    img = base64.b64decode(img_type[end+1:])
    return img, img_type