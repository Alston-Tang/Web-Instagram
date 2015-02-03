__author__ = 'Tang'

from tools import router


def index(env):
    body = """<!doctype html>
<html lang="en">
<head>
</head>
<body>
    Hello World!
</body>
</html>
"""
    ctype = 'text/html'
    return [ctype, body]

router.route('/', index)
