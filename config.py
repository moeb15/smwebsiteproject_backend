from dotenv import load_dotenv
import os

load_dotenv()
class Config:
    DEBUG = True

    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_DEBUG = os.environ.get('FLASK_ENV')


    USER = os.environ.get('PG_USER')
    PWD = os.environ.get('PG_PASSWORD')
    DBNAME = os.environ.get('PG_DBNAME')
    SRVR = os.environ.get('PG_SERVER')

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{USER}:{PWD}@{SRVR}/{DBNAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_ERROR_MESSAGE_KEY = os.environ.get('JWT_ERROR_MESSAGE_KEY')
    JWT_BLACKLIST_ENABLED = os.environ.get('JWT_BLACKLIST_ENABLED ')
    JWT_BLACKLIST_TOKEN_CHECKS = os.environ.get('JWT_BLACKLIST_TOKEN_CHECKS ')

    APISPEC_SWAGGER_URL= '/swagger/' 
    APISPEC_SWAGGER_UI_URL= '/docs/'

    CORS_HEADERS = 'Content-Type'
