__author__ = 'Tang'

from response import Response
import os

def not_found():
    return Response(body="Opp! 404!", status=404)