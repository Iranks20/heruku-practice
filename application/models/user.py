from abc import abstractstaticmethod
from lib2to3.pgen2 import token
from tokenize import Token
from venv import create
from flask import Response, request, jsonify
import application
from helpers.db_helper import Database as db
from flaskext.mysql import MySQL
import uuid
#from werkzeug.security import generate_password_hash, check_password_hash
import phonenumbers
#imports for jwt
import jwt
from datetime import datetime, timedelta
from functools import wraps
#from application.libs.modal import Modal as md
from application.models.auth import token_required
from application import application
from application.models.user_wallet import UserWallet
 

application.config['SECRET_KEY'] = 'fduttrredfghrew'
class User:
    def __init__(self):
        print("user model")

#display all users
    @staticmethod
    @token_required
    def allUsers():
        token = jwt.encode({
                #'email':_email,
                'expiration':str(datetime.now() + timedelta(seconds=120))
            },
            application.config['SECRET_KEY'])

        sql = "SELECT * FROM `user`"
        data = db.select(sql)
        response = jsonify(data)
        return response
       
#adding user
    @staticmethod
    def userAdd():
        try:
            _json = request.json
            _user_id = uuid.uuid4()
            print(_user_id)
            _first_name = _json['first_name']
            _last_name = _json['last_name']
            _telephone_number = _json['telephone_number']
            _email = _json['email']
            _password = _json['password']
            _profile_picture = _json['profile_picture']

            phoneNumber = phonenumbers.parse(_telephone_number)
            check_phoneNumber = phonenumbers.is_possible_number(phoneNumber)
            if check_phoneNumber == False:
                return make_response(403, "Invalid phone number")
            check_user = get_user_detail(_email, _telephone_number)
            if len(check_user) > 0:
                return make_response(403, "User Already Exists")


            
            addUser_dict = {"user_id": _user_id, "first_name": _first_name, "last_name": _last_name, "telephone_number": _telephone_number, "email": _email, "password": _password, "profile_picture": _profile_picture}
            data = db.insert('user', **addUser_dict)
            create_user_wallet = UserWallet.createWallet(_user_id)
            response = jsonify({"status": "Added Successfully"})


            return response
        except Exception as e:
            print(e)
            response = jsonify({"message": str(e)})
            return response

#updating user
    @staticmethod
    def userUpdate():
        try:
            _json = request.json
            _first_name = _json['first_name']
            _last_name = _json['last_name']
            _telephone_number = _json['telephone_number']
            _email = _json['email']
            _password = _json['password']
            _profile_picture = _json['profile_picture']

            updateUser_dict = {"first_name": _first_name, "last_name": _last_name, "telephone_number": _telephone_number, "email": _email, "password": _password, "profile_picture": _profile_picture}
            data = db.insert('user', **updateUser_dict)
            response = jsonify({"status": "updated Successfully"})

            return response
        except Exception as e:
            print(e)
            response = jsonify({"message": str(e)})
            return response
            
#delete user

    def deleteUser():
        try:
            _json = request.json
            _userId = _json['user_id']
            sql = "DELETE FROM `user` WHERE user_id = '" + str(_userId) + "' "
            db.delete(sql)
            response = jsonify(100, "user deleted successfully")
            return response
        except Exception as e:
            print(e)
            response = jsonify(403, "failed to delete the user")
            return response



#login user
    @staticmethod
    @token_required
    def loginUser():
        try:
            _json = request.json
            _email = _json['email']
            _password = _json['password']

            check_user = get_user_details(_email, _password)

            if len(check_user) <= 0:
                data = make_response(403, "failed to log in")
                return data
                
            token = jwt.encode({
                'public_id': User.public_id,
                'expiration':str(datetime.now() + timedelta(seconds=120))
            },
            application.config['SECRET_KEY'])
            return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)

            #response = user_logged_response(100, "user loggedin successfully", check_user, Token)
            
            #return response
        
        except Exception as e:
            print(e)
            data = make_response(403, "failed to login user !!!")
            return data














#user details for register model
def get_user_details(telephone_number):
    sql = "SELECT * FROM user WHERE telephone_number = '" + telephone_number + "' "
    data = db.select(sql)
    return data

    # responses
def make_response(status, message):
    return jsonify({"message": message, "status": status})

    # user created response
def user_created_response(status, message, userId):
    return jsonify({"user_id": userId, "status": status, "message": message})

#def get_user_by_username(user_id):
    #sql = "SELECT * FROM user WHERE username = '" + user_id + "' "
    #data = db.select(sql)
    #urn data

#@staticmethod
#def make_response(status, message):
        #rsp = {'status': status, 'response': message}
        #if status == 100:
           # code = 200
        #elif status == 404:
            #code = 404
       # else:
           # code = 403
        #return jsonify(rsp), code

#@staticmethod
#def get_user_by_id(user_id):
        #sql = "select * FROM user WHERE user_id = '" + user_id + "' "
        #data = db.select(sql)
        #return data
        
        # user details based on register model
def get_user_detail(Email, telephone_number):
    sql = "SELECT * FROM `user` WHERE email = '" + Email + "' OR telephone_number = '" + telephone_number + "' "
    data = db.select(sql)
    return data

    # user logged in response
def user_logged_response(status, message, data,):
    return jsonify({"message": message, "data": data, "status": status,})

      #user details for login 
def get_user_details(Email, Password):
    sql = "SELECT * FROM `user` WHERE email = '" + Email + "' AND password = '" + Password + "' "
    data = db.select(sql)
    return data
