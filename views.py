__author__ = 'Tang'

from tools import router, Response
import cgi
import os


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


def upload(env):
    path = os.path.join('static', 'upload')
    repo_path = os.getenv('OPENSHIFT_REPO_DIR')
    if repo_path:
        path = os.path.normpath(os.path.join(path, repo_path))
    if env['REQUEST_METHOD'] != 'POST':
        return None

    form = cgi.FieldStorage(fp=env['wsgi.input'], environ=env, keep_blank_values=True)
    pic = form['fileToUpload']
    filename = os.path.split(pic.filename)[1]
    temp = open(os.path.join(path, filename), mode='wb')
    temp.write(pic.value)
    temp.close()


router.route('/', index)
router.route('/upload', upload)
router.p_tree()
