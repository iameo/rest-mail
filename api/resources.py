import flask
from flask_restful import Resource

from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from bson.objectid import ObjectId
from bson.json_util import dumps

from api import db, mail, api, login_manager
from api.model import User

from flask_mail import Mail, Message

from api.utils import fetch_json, mailer_func



@login_manager.user_loader
def load_user(username):
    '''user_loader as required by flask-login'''
    user_json =  db.find_one({"_id":ObjectId(username)})
    return User(user_json)

class CheckAuth(Resource):
    def get(self):
        if current_user.is_authenticated:
            return flask.jsonify({"message": "logged on"})
        return flask.jsonify({"message": "not logged on"})


class Login(Resource):
    def post(self):
        _json = fetch_json()
        username = _json["username"]
        password = _json["password"]

        if username and password:
            user = db.find_one({"username":username})
            if user:
                password_check = check_password_hash(user["password"], password)
                logged_user = User(user)
                return login_user(logged_user) if password_check else False
            return flask.jsonify({"message": "user does not exist"})
        return flask.jsonify({"message":"you must enter both username and password to authenticate!"})


class Logout(Resource):
    def get(self):
        logout_user()
        return flask.jsonify({"message":"logged out"})


class Register(Resource):
    def post(self):
        _json = fetch_json()
        username = _json["username"]
        password = _json["password"]
        password2 = _json["password2"]
        email = _json["email"]

        if username and password and password2 and email:
            if not db.find_one({"username":username}) and (password == password2):
                '''stored hashed value of password as password'''
                hashed_pwd = generate_password_hash(password)
                id = db.insert_one({"username":username, "password": hashed_pwd, "is_active":True, "email":email})
                return flask.jsonify({"status":201, "message":"user registered successfully", "data": dumps(id)})
            return flask.jsonify({"message": "username might be already registered or check your passwords"})
        return flask.jsonify({"status":400, "message":"missing credentials"})


class Mail(Resource):
    # @login_required
    # def get(self):
    #     _json = fetch_json()
    #     _id = _json["_id"]
    #     if _id:
    #         return flask.jsonify(
    #             {"data": dumps(db.find_one({"_id": ObjectId(str(_id))}))})
    #     return flask.jsonify({"message":"nothing to retrieve"})

    @login_required
    def post(self):
        '''get email from current logged on user'''
        mailer = mailer_func()
        try:
            mailer()
        except Exception as e: #in prod, you'd want to catch specific exceptions
            return flask.jsonify({"status":400, "message":"failed", "error": str(e)})
        return flask.jsonify({"status":200, "message":"message sent successfully"})




api.add_resource(CheckAuth, '/check-auth')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Register, '/register')
api.add_resource(Mail, '/mail')