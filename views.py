__author__ = 'Tang'

from tools import router, Response, to_data_uri, set_session, init_db
from template import render
import cgi
import os


def index(env):

    body = render('index.html')
    return Response(body=body)


def upload(env):
    if env['REQUEST_METHOD'] != 'POST':
        return None

    form = cgi.FieldStorage(fp=env['wsgi.input'], environ=env, keep_blank_values=True)
    pic = form['img']
    session = set_session()

    #pic_uri = to_data_uri(pic, )


def init(env):
    init_db()
    return index(env)





router.route('/', index)
router.route('/upload', upload)
router.route('/init.html', init)
router.p_tree()
