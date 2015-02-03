__author__ = 'Tang'

import os

MIME_TABLE = {'.txt': 'text/plain',
              '.html': 'text/html',
              '.css': 'text/css',
              '.js': 'application/javascript'}


def get_static(path):
    file_type = "application/octet-stream"
    if os.path.exists(path):
        f = open(path, 'rb')
        content = f.read()
        f.close()
        name, ext = os.path.splitext(path)
        if ext in MIME_TABLE:
            file_ype = MIME_TABLE[ext]
        return [file_type, content]
    else:
        return False

print get_static('static.py')