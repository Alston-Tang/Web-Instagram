__author__ = 'Tang'

from response import Response


def not_found():
    return Response("Not Found", status=404)