__author__ = 'Tang'

from tools import router, Response, set_session, init_db, get_uploaded_img, upload_photo, commit_photo, get_page, \
    get_photo, decode_data_uri, img_filter, encode_data_uri, img_annotate, reset_session, verify_session, pop_photo, \
    last_photo
from template import render
import cgi
import Cookie
from urlparse import parse_qs


def index(env, error_inf=None):
    session_id = None
    cookie = Cookie.SimpleCookie()
    photo = None
    if 'HTTP_COOKIE' in env:
        cookie.load(env['HTTP_COOKIE'])
        session_id = cookie['token'].value
        session_id = verify_session(session_id)
        photo = get_photo(session_id)
    if not session_id:
        pass

    query = parse_qs(env['QUERY_STRING'])
    try:
        page = int(query.get('page', [1])[0])
    except:
        page = 1
    photos, total_count = get_page(page)
    page = 1 if page > total_count else page
    if total_count != 0:
        total_count = (total_count - 1) / 8 + 1
    next_page = False if page >= total_count else True
    prev_page = False if page == 1 else True
    body = render('index.html', photos=photos, photo=photo, page=page, total_page=total_count, next=next_page, prev=prev_page, error_inf=error_inf)
    return Response(body=body)


def upload(env):
    if env['REQUEST_METHOD'] != 'POST':
        return None
    session_id = None
    cookie = Cookie.SimpleCookie()
    if 'HTTP_COOKIE' in env:
        cookie.load(env['HTTP_COOKIE'])
        session_id = cookie['token'].value
    img_uri = get_uploaded_img(env)
    if img_uri is False:
        return index(env, "Wrong Type")
    if not session_id:
        session_id = set_session()
    else:
        session_id = verify_session(session_id)
        reset_session(session_id)
    upload_photo(img_uri, session_id)
    photo = get_photo(session_id)
    return Response(body=render('editor.html', photo=photo, undo=False), cookie=('token', session_id))


def init(env):
    init_db()
    return Response(body=render('init_success.html'))


def filter(env):
    session_id = None
    cookie = Cookie.SimpleCookie()
    if 'HTTP_COOKIE' in env:
        cookie.load(env['HTTP_COOKIE'])
        session_id = cookie['token'].value
    if not session_id:
        return index(env)
    form = cgi.FieldStorage(fp=env['wsgi.input'], environ=env, keep_blank_values=True)
    filter_type = form['filter'].value
    data, img_type = decode_data_uri(get_photo(session_id))
    data, img_type = img_filter(filter_type, data, img_type)
    data = encode_data_uri(data, img_type)
    upload_photo(data, session_id)
    photo = get_photo(session_id)
    return Response(body=render('editor.html', photo=photo, undo=True))


def annotate(env):
    session_id = None
    cookie = Cookie.SimpleCookie()
    if 'HTTP_COOKIE' in env:
        cookie.load(env['HTTP_COOKIE'])
        session_id = cookie['token'].value
    if not session_id:
        return index(env)
    undo_button = not last_photo(session_id)
    form = cgi.FieldStorage(fp=env['wsgi.input'], environ=env, keep_blank_values=True)
    font_type = form['type'].value
    size = form['size'].value
    try:
        size = int(size)
    except:
        size = 20
    if size > 48 or size < 10:
        photo = get_photo(session_id)
        return Response(body=render('editor.html', photo=photo, error_inf="Invalid Font Size", undo=undo_button))
    content = form['content'].value
    if not content:
        photo = get_photo(session_id)
        return Response(body=render('editor.html', photo=photo, error_inf="Empty Content", undo=undo_button))
    if font_type not in ['Times-Bold', 'Courier', 'Helvetica']:
        photo = get_photo(session_id)
        return Response(body=render('editor.html', photo=photo, error_inf="Invalid Font Type", undo=undo_button))
    position = form['position'].value
    if position != 'top' and position != 'bottom':
        photo = get_photo(session_id)
        return Response(body=render('editor.html', photo=photo, error_inf="Invalid Position", undo=undo_button))

    data, img_type = decode_data_uri(get_photo(session_id))
    data, img_type = img_annotate(font_type, size, position, content, data, img_type)
    data = encode_data_uri(data, img_type)
    upload_photo(data, session_id)
    photo = get_photo(session_id)
    return Response(body=render('editor.html', photo=photo, undo=True))


def submit(env):
    session_id = None
    cookie = Cookie.SimpleCookie()
    if 'HTTP_COOKIE' in env:
        cookie.load(env['HTTP_COOKIE'])
        session_id = cookie['token'].value
    if not session_id:
        return index(env)
    photo = get_photo(session_id)
    commit_photo(session_id)
    reset_session(session_id)
    return Response(render('finish.html', photo=photo))


def discard(env):
    session_id = None
    cookie = Cookie.SimpleCookie()
    if 'HTTP_COOKIE' in env:
        cookie.load(env['HTTP_COOKIE'])
        session_id = cookie['token'].value
    if not session_id:
        return index(env)
    reset_session(session_id)
    return index(env)


def undo(env):
    session_id = None
    cookie = Cookie.SimpleCookie()
    if 'HTTP_COOKIE' in env:
        cookie.load(env['HTTP_COOKIE'])
        session_id = cookie['token'].value
    if not session_id:
        return index(env)
    undo_success = pop_photo(session_id)
    undo_button = not last_photo(session_id)
    if undo_success:
        photo = get_photo(session_id)
        return Response(body=render('editor.html', photo=photo, undo=undo_button))


def resume(env):
    session_id = None
    cookie = Cookie.SimpleCookie()
    if 'HTTP_COOKIE' in env:
        cookie.load(env['HTTP_COOKIE'])
        session_id = cookie['token'].value
    if not session_id:
        return index(env, error_inf="Session Not Set")
    photo = get_photo(session_id)
    undo_button = not last_photo(session_id)
    return Response(body=render('editor.html', photo=photo, undo=undo_button))


def init_page(env):
    return Response(body=render('init.html'))


router.route('/', index)
router.route('/upload', upload)
router.route('/init', init)
router.route('/init.html', init_page)
router.route('/filter', filter)
router.route('/annotate', annotate)
router.route('/submit', submit)
router.route('/discard', discard)
router.route('/undo', undo)
router.route('/resume', resume)
router.route('/show', index)
router.p_tree()