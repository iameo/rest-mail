import flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_restful import Api

from flask_pymongo import PyMongo

import os

from dotenv import load_dotenv
load_dotenv()

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'sloovi-sloovin'
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

login_manager = LoginManager()
login_manager.init_app(app)


#connect app to mongo db
mongo = PyMongo(app)

#collection userz, creates if not created
db = mongo.db.userz

api = Api(app)

#flask-mail config
app.config['MAIL_SERVER']= os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_SUPPRESS_SEND'] = os.getenv('MAIL_SUPPRESS_SEND')
app.config['MAIL_DEBUG'] = os.getenv('MAIL_DEBUG')

mail = Mail(app)

from api import resources