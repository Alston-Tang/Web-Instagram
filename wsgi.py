#!/usr/bin/python
import os
import cgi
from tools import not_found

if __name__ != '__main__':
    virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
    virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
    try:
        execfile(virtualenv, dict(__file__=virtualenv))
    except IOError:
        pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

from tools import router
import views


def application(environ, start_response):

    url = environ['PATH_INFO']

    handler = router.match(url)
    if handler:
        res = handler(environ)
        if res:
            start_response(res.get_status(), res.get_header())
            return [res.get_body().encode('utf-8')]

    handler = router.permanent_link(url)
    if handler:
        img_path = filter(None, url.split('/'))[1]
        res = handler(img_path, environ)
        if res:
            start_response(res.get_status(), res.get_header())
            return [res.get_body()]

    handler = router.static(url)
    if handler:
        res = handler(url, environ)
        if res:
            start_response(res.get_status(), res.get_header())
            return [res.get_body()]

    res = not_found()
    start_response(res.get_status(), res.get_header())
    return [res.get_body().encode('utf-8')]

#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    # Wait for a single request, serve it and quit.q
    httpd.serve_forever()
