__author__ = 'Tang'

from router import Router
from response import Response
from errors import not_found
from static import get_static, encode_data_uri, decode_data_uri, get_uploaded_img, img_filter, img_annotate
from database import *
router = Router()