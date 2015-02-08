__author__ = 'Tang'

from tools import router, Response, set_session, init_db, get_uploaded_img, upload_photo, get_page, commit_photo

from template import render


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
    commit_photo(session_id)




    pass

    #pic_uri = to_data_uri(pic, )


def init(env):
    init_db()
    return Response(body='Success')


def test(env):
    return Response(body=render('editor.html'))

router.route('/', index)
router.route('/upload', upload)
router.route('/init.html', init)
router.route('/test', test)
router.p_tree()
