
from flask import Response, request, jsonify, session
#import application
from helpers.db_helper import Database as db
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
import hashlib
from random import randint
from application.libs.sms import send

application.config['SECRET_KEY'] = 'a6d4c1d6828549b6ada2d94ef4aeb9a1'
class User:
    def __init__(self):
        print("user model")

#display all users
    @staticmethod
    @token_required
    def allUsers():
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
            _first_name = _json['first_name']
            _last_name = _json['last_name']
            _telephone_number = _json['telephone_number']
            _email = _json['email']
            _password = _json['password']
            _profile_picture = _json['profile_picture']

            #hashing password
            hash_password = hashlib.sha256(str(_password).encode('utf-8')).hexdigest()

            #password_hash = db.column(db.strinf(128))
            #@property
            #def password(self):
                #raise AttributeError('pass is not readable')
            #@password.setter
            #def password(self,password):
                #self.password_hash = generate_password_hash(password)
            #def verify_password(self, password):
                #return check_password_hash(self.password_hash, password)
            


            phoneNumber = phonenumbers.parse(_telephone_number)
            check_phoneNumber = phonenumbers.is_possible_number(phoneNumber)
            if check_phoneNumber == False:
                return make_response(403, "Invalid phone number")
            check_user = get_user_detail(_email, _telephone_number)
            if len(check_user) > 0:
                return make_response(403, "User Already Exists")

            otp_generated = randint(0000,9999)
            status = 'pending'
            otp_sent = send(otp_generated, _email)

            addUser_dict = {"user_id": _user_id, "first_name": _first_name, "last_name": _last_name, "telephone_number": _telephone_number, "email": _email, "password": hash_password, "profile_picture": _profile_picture, "status": status, "otp": otp_generated}
            data = db.insert('user', **addUser_dict)

            response = make_response(100, otp_sent)
            #create_user_wallet = UserWallet.createWallet(_user_id)
            #response = jsonify({"status": " user Added Successfully"})


            return response
        except Exception as e:
            print(e)
            response = make_response(403, "invalid data types")
            #response = jsonify({"message": str(e)})
            return response


            #verifying the otp
    @staticmethod
    def verifyOTP(): 
        try:
            _json = request.json
            _email = _json['email']
            _requested_otp = _json['otp']

            check_user = get_user_by_email(_email)
            if len(check_user) <= 0:
                response = make_response (403, "wrong email")
                return response

            otp = check_user[0]['otp']
            if _requested_otp != otp:
                response = make_response(403, "invalid OTP")
                return response
            status = 'Active'
            _user_id = check_user[0]['user_id']

            updatedUser_dict = {"status": status}
            db.Update('user', "user_id  =  '" + str(_user_id) + "'", **updatedUser_dict)

            create_user_wallet = UserWallet.createWallet(_user_id)
            userData = get_user_details_by_id(_user_id)

            token = jwt.encode({
                'email': _email,
                'expiration': str(datetime.now() + timedelta(seconds=120))
            },
                application.config['SECRET_KEY'])

            response = user_created_response(100, userData, token)
            return response

        except Exception as e:
            print(e)
            return make_response(404, str(e))

#updating user
    @staticmethod
    @token_required
    def userUpdate():
        try:
            _json = request.json
            _userId = _json['user_id']
            _first_name = _json['first_name']
            _last_name = _json['last_name']
            _telephone_number = _json['telephone_number']
            _email = _json['email']
            _password = _json['password']
            _profile_picture = _json['profile_picture']

            #hash password
            hash_password = hashlib.sha256(str(_password).encode('utf-8')).hexdigest()
            #print(hash_password)

            updateUser_dict = {"first_name": _first_name, "last_name": _last_name, "telephone_number": _telephone_number, "email": _email, "password": hash_password, "profile_picture": _profile_picture}
            db.Update('user', "user_id  =  '" + str(_userId) + "'", **updateUser_dict)
            response = make_response(100, "updated Successfully")

            return response
        except Exception as e:
            print(e)
            response = make_response(403, "failed to update")
            #response = jsonify({"message": str(e)})
            return response
            
#delete user
    @token_required
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
    def loginUser():
        try:
            _json = request.json
            _email = _json['email']
            _password = _json['password']

            # hash password
            hash_password = hashlib.sha256(str(_password).encode('utf-8')).hexdigest()
            check_user = get_user_details(_email, hash_password)
            

            if len(check_user) <= 0:
                data = make_response(403, "credentials entered are wrong")
                return data
            userId = check_user[0]['user_id']
            status = check_user[0]['status']
            
            if status != 'Active':
                response = make_response(403, "first verify your otp")
                return response
            userData = get_user_details_by_id(userId)
            token = jwt.encode({
                'email': _email,
                'expiration': str(datetime.now() + timedelta(seconds=120))
            },
                application.config['SECRET_KEY'])
            response = user_logged_response(100, "user logged in successfully", userData, token)
            
            return response
        
        except Exception as e:
            print(e)
            data = make_response(403, "can't log in a user")
            return data

    # get user details by id
    @staticmethod
    @token_required
    def getUserDetailsById():
        try:
            _json = request.json
            _user_id = _json['user_id']

            data = get_user_details_by_id(_user_id)
            
            if len(data) <= 0:
                response = make_response(403, "No such user")
                return response

            response = jsonify(data)
            return response
        except Exception as e:
            print(e)
            response = make_response(403, "failed to pull user with specific ID")
            return response












#user details for register model
#def get_user_details(telephone_number):
    #sql = "SELECT * FROM user WHERE telephone_number = '" + telephone_number + "' "
    #data = db.select(sql)
    #return data

    # responses
def make_response(status, message):
    return jsonify({"message": message, "status": status})

    # user created response
def user_created_response(status, message, token):
    return jsonify({"status": status, "message": message, "token":token})

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
def user_logged_response(status, message, data, token):
    return jsonify({"message": message, "data": data, "status": status, "token": token})

      #user details for login 
def get_user_details(Email, Password):
    sql = "SELECT * FROM `user` WHERE email = '" + Email + "' AND password = '" + Password + "' "
    data = db.select(sql)
    return data

#get user by email
def get_user_by_email(email):
    sql = "SELECT * FROM `user` WHERE email = '" + str(email) + "' "
    data = db.select(sql)
    return data

# get user details by id
def get_user_details_by_id(userId):
    sql = "SELECT * FROM `user` WHERE user_id = '" + str(userId) + "' "
    result = db.select(sql)
    data = [
        {
            "first_name": result[0]['first_name'], 
            "last_name": result[0]['last_name'], 
            "email": result[0]['email'],
            "telephone_number": result[0]['telephone_number'],
            "user_id": result[0]['user_id'],
            "status": result[0]['status'],
            "date_time": result[0]['date_time']
        }
        ]
    return data

# get user data without password, otp
def get_mod_userdetail(Email, Telephone_number):
    sql = "SELECT * FROM `user` WHERE email = '" + Email + "' OR telephone_number = '" + Telephone_number + "' "
    result = db.select(sql)
    data = [
        {
            "first_name": result[0]['first_name'], 
            "last_name": result[0]['last_name'], 
            "email": result[0]['email'],
            "telephone_number": result[0]['telephone_number'],
            "user_id": result[0]['user_id'],
            "status": result[0]['status'],
            "date_time": result[0]['date_time']
        }
        ]
    return data
