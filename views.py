__author__ = 'Tang'

from tools import router, Response, set_session, init_db, get_uploaded_img, upload_photo, commit_photo, get_page, \
    get_photo, decode_data_uri, img_filter, encode_data_uri, img_annotate, reset_session, verify_session, pop_photo

from template import render
import cgi
import Cookie
from urlparse import parse_qs


def index(env):
    query = parse_qs(env['QUERY_STRING'])
    try:
        page = int(query.get('page', [1])[0])
    except:
        page = 1
    photos, total_count = get_page(page)
    if total_count != 0:
        total_count = (total_count - 1) / 8 + 1
    next_page = "disabled" if page == total_count else ""
    prev_page = "disabled" if page == 1 else ""
    body = render('index.html', photos=photos, page=page, total_page=total_count, next=next_page, prev=prev_page)
    return Response(body=body)


def upload(env):
    if env['REQUEST_METHOD'] != 'POST':
        return None
    session_id = None
    cookie = Cookie.SimpleCookie()
    if 'HTTP_COOKIE' in env:
        cookie.load(env['HTTP_COOKIE'])
        session_id = cookie['token'].value
    if not session_id:
        session_id = set_session()
    else:
        session_id = verify_session(session_id)
        reset_session(session_id)
    img_uri = get_uploaded_img(env)
    upload_photo(img_uri, session_id)
    photo = get_photo(session_id)
    return Response(body=render('editor.html', photo=photo), cookie=('token', session_id))


def init(env):
    init_db()
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


def submit(env):
    session_id = None
    cookie = Cookie.SimpleCookie()
    if 'HTTP_COOKIE' in env:
        cookie.load(env['HTTP_COOKIE'])
        session_id = cookie['token'].value
    if not session_id:
        pass
    commit_photo(session_id)
    return Response(body='Success')


def discard(env):
    session_id = None
    cookie = Cookie.SimpleCookie()
    if 'HTTP_COOKIE' in env:
        cookie.load(env['HTTP_COOKIE'])
        session_id = cookie['token'].value
    if not session_id:
        pass
    reset_session(session_id)
    return Response(body='Success')


def undo(env):
    session_id = None
    cookie = Cookie.SimpleCookie()
    if 'HTTP_COOKIE' in env:
        cookie.load(env['HTTP_COOKIE'])
        session_id = cookie['token'].value
    if not session_id:
        pass
    undo_success = pop_photo(session_id)
    if undo_success:
        photo = get_photo(session_id)
        return Response(body=render('editor.html', photo=photo))


def resume(env):
    session_id = None
    cookie = Cookie.SimpleCookie()
    if 'HTTP_COOKIE' in env:
        cookie.load(env['HTTP_COOKIE'])
        session_id = cookie['token'].value
    if not session_id:
        pass
    photo = get_photo(session_id)
    return Response(body=render('editor.html', photo=photo))


router.route('/', index)
router.route('/upload', upload)
router.route('/init.html', init)
router.route('/filter', filter)
router.route('/annotate', annotate)
router.route('/submit', submit)
router.route('/discard', discard)
router.route('/undo', undo)
router.route('/resume', resume)
router.route('/show', index)
router.p_tree()