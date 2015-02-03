__author__ = 'Tang'

import os
from response import Response

MIME_TABLE = {'.txt': 'text/plain',
              '.html': 'text/html',
              '.css': 'text/css',
              '.js': 'application/javascript',
              '.jpg': 'image/jpeg',
              '.jpeg': 'image/jpeg'}


def get_static(path, env):
    path = path[1:len(path)]
    file_type = "application/octet-stream"
    if os.path.exists(path):
        f = open(path, 'rb')
        content = f.read()
        f.close()
        name, ext = os.path.splitext(path)
        if ext in MIME_TABLE:
            file_ype = MIME_TABLE[ext]
        return Response(content, ctype=file_type)
    else:
        return None