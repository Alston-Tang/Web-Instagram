__author__ = 'Tang'

from response import Response
import os

def not_found():
    return Response(os.getcwd(), status=404)