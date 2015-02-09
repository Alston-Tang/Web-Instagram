__author__ = 'Tang'

HTTP_STATUS = {200: '200 OK', 404: '404 Not Found'}
from dateutil.relativedelta import relativedelta
from datetime import datetime


class Response:
    body = None
    header = None
    status = None

    def __init__(self, body=None, header=None, status=200, ctype="text/html", charset='utf-8', cookie=None):
        self.body = body
        if not self.header:
            self.header = {}
        if header:
            for key in header:
                self.header[key] = header[key]
        self.header['Content-Type'] = ctype
        self.status = HTTP_STATUS[status]
        if cookie:
            expire_time = datetime.now() + relativedelta(months=+3)
            self.header['Set-Cookie'] = '%s=%s; Expires=%s' % \
                                        (cookie[0], cookie[1], expire_time.strftime("%a, %d-%b-%Y %T GMT"))


    def get_header(self):
        rv = []
        for key in self.header:
            rv.append((key, self.header[key]))
        rv.append(('Content-Length', str(len(self.body))))
        return rv

    def get_status(self):
        return self.status

    def get_body(self):
        return self.body