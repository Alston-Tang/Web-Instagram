__author__ = 'Tang'

import os
import base64
from response import Response
from conf import STATIC_PATH, ACCEPT_IMG

MIME_TABLE = {'.txt': 'text/plain',
              '.html': 'text/html',
              '.css': 'text/css',
              '.js': 'application/javascript',
              '.jpg': 'image/jpeg',
              '.jpeg': 'image/jpeg'}


def get_static(path, env):
    path = os.path.normpath(STATIC_PATH+path[1:len(path)])
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


def to_data_uri(data, img_type):
    if type not in ACCEPT_IMG:
        return None
    else:
        return 'date:' + img_type + ';base64,' + base64.b64encode(data)