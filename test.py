__author__ = 'Tang'

from tools import Router

t = Router()

t.route("/test", None)
t.route("/test/url", None)
t.route("/ls", None)

t.p_tree()