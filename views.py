__author__ = 'Tang'

from tools import router


def index():
    return """<!doctype html>
<html lang="en">
<head>
</head>
<body>
    Hello World!
</body>
</html>
"""

router.route('/', index)
