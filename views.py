__author__ = 'Tang'

from tools import router, Response, to_data_uri
from template import render
import cgi
import os


def index(env):

    body = render('test.html', content="Hello World!")
    return Response(body=body)


def upload(env):
    if env['REQUEST_METHOD'] != 'POST':
        return None

    form = cgi.FieldStorage(fp=env['wsgi.input'], environ=env, keep_blank_values=True)
    pic = form['fileToUpload']
    #pic_uri = to_data_uri(pic, )




router.route('/', index)
router.route('/upload', upload)
router.p_tree()
