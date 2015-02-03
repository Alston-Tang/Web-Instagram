__author__ = 'Tang'

from tools import router, Response


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
    return Response(body=body)

router.route('/', index)
