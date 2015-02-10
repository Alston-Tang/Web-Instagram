__author__ = 'Tang'

from tools import router, Response, set_session, init_db, get_uploaded_img, upload_photo, commit_photo, get_page, \
    get_photo, decode_data_uri, img_filter, encode_data_uri, img_annotate

from template import render
import cgi, Cookie

def index(env):
    photos = get_page(1)
    body = render('index.html', photos=photos)
    return Response(body=body)


def upload(env):
    if env['REQUEST_METHOD'] != 'POST':
        return None
    img_uri = get_uploaded_img(env)
    session_id = set_session()
    upload_photo(img_uri, session_id)
    photo = get_photo(session_id)
    return Response(body=render('editor.html', photo=photo), cookie=('token', session_id))


def init(env):
    init_db()/upload
    return Response(body='Success')


def filter(env):
    session_id = None
    cookie = Cookie.SimpleCookie()
    if 'HTTP_COOKIE' in env:
        cookie.load(env['HTTP_COOKIE'])
        session_id = cookie['token'].value
    if not session_id:
        pass
    form = cgi.FieldStorage(fp=env['wsgi.input'], environ=env, keep_blank_values=True)
    filter_type = form['filter'].value
    data, img_type = decode_data_uri(get_photo(session_id))
    data, img_type = img_filter(filter_type, data)
    data = encode_data_uri(data, img_type)
    upload_photo(data, session_id)
    photo = get_photo(session_id)
    return Response(body=render('editor.html', photo=photo))


def annotate(env):
    session_id = None
    cookie = Cookie.SimpleCookie()
    if 'HTTP_COOKIE' in env:
        cookie.load(env['HTTP_COOKIE'])
        session_id = cookie['token'].value
    if not session_id:
        pass
    form = cgi.FieldStorage(fp=env['wsgi.input'], environ=env, keep_blank_values=True)
    font_type = form['type'].value
    size = form['size'].value
    content = form['content'].value
    position = form['position'].value

    data, img_type = decode_data_uri(get_photo(session_id))
    data, img_type = img_annotate(font_type, size, position, content, data, img_type)
    data = encode_data_uri(data, img_type)
    upload_photo(data, session_id)
    photo = get_photo(session_id)
    return Response(body=render('editor.html', photo=photo))





def test(env):
    return Response(body=render('editor.html'))

router.route('/', index)
router.route('/upload', upload)
router.route('/init.html', init)
router.route('/filter', filter)
router.route('/annotate', annotate)
router.route('/test', test)
router.p_tree()
