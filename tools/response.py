__author__ = 'Tang'

HTTP_STATUS = {200: '200 OK', 404: '404 Not Found'}

class Response:
    body = None
    header = None
    status = None

    def __init__(self, body=None, header=None, status=200, ctype="text/html", charset='utf-8'):
        self.body = body
        if not self.header:
            self.header = {}
        if header:
            for key in header:
                self.header[key] = header[key]
        self.header['Content-Type'] = ctype
        self.status = HTTP_STATUS[status]


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