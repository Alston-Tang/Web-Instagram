__author__ = 'Tang'

import os


REPO_PATH = os.getenv('OPENSHIFT_REPO_DIR')
if not REPO_PATH:
    print("===================== For Debug ===========================")
    REPO_PATH = os.getcwd()

STATIC_PATH = os.path.join(REPO_PATH, 'static')
UPLOAD_PATH = os.path.join(STATIC_PATH, 'upload')
TEMPLATE_PATH = os.path.join(REPO_PATH, 'template')

DB_HOST = os.getenv('OPENSHIFT_MYSQL_DB_HOST')
DB_PORT = os.getenv('OPENSHIFT_MYSQL_DB_PORT')
DB_USERNAME = os.getenv('OPENSHIFT_MYSQL_DB_USERNAME')
DB_PASSWORD = os.getenv('OPENSHIFT_MYSQL_DB_PASSWORD')

if not DB_HOST or not DB_PORT or not DB_USERNAME or not DB_PASSWORD:
    DB_HOST = 'localhost'
    DB_PORT = '3306'
    DB_USERNAME = 'adminUbw65Jz'
    DB_PASSWORD = 'aMlEyugQkjaa'

ACCEPT_IMG = ['image/jpeg', 'image/png',  'image/gif']

