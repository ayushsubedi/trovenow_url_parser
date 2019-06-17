from flask import Flask
from os import environ
from dotenv import load_dotenv
from os.path import join, dirname
from flask_cors import CORS

application = Flask(__name__)

# Linux
# dotenv_path = join(dirname(__file__), '..', '.env')

# Windows
dotenv_path = '.env'


# Allow CORS for this app
CORS(application)

load_dotenv(dotenv_path)

# Secret key for form
application.config['SECRET_KEY'] = environ.get('SECRET_KEY')

from trovenow_url_parser import api_routes
from trovenow_url_parser import routes