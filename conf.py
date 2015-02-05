__author__ = 'Tang'

import os


REPO_PATH = os.getenv('OPENSHIFT_REPO_DIR')
if not REPO_PATH:
    print("===================== For Debug ===========================")
    REPO_PATH = os.getcwd()

STATIC_PATH = os.path.join(REPO_PATH, 'static')
UPLOAD_PATH = os.path.join(STATIC_PATH, 'upload')
TEMPLATE_PATH = os.path.join(REPO_PATH, 'template')

ACCEPT_IMG = ['image/jpeg', 'image/png',  'image/gif']

