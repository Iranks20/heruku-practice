from flask import Blueprint, request, jsonify, json
from application.models.user import User
import hashlib
#from application.libs.modal import Modal as md

bp_app = Blueprint('mod_user', __name__)


#display all users
@bp_app.route('/all_users', methods=['GET'])
def getUsers():
    data = User.allUsers()
    return data


# adding a user
@bp_app.route('/add_user', methods=['POST'])
def add_user():
    data = User.userAdd()
    return data

  # update a user
@bp_app.route('/update_user', methods=['POST'])
def update_user():
    data = User.userUpdate()
    return data  

#delete user
@bp_app.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = User.deleteUser()
    return data

  # user login
@bp_app.route("/login_user", methods=["POST"])
def login_user():
    data = User.loginUser()
    return data

# verify otp
@bp_app.route("/verify_otp", methods=['POST'])
def verify_otp():
    data = User.verifyOTP()
    return data

#get user details by id
@bp_app.route('/get_user_by_id', methods=['POST'])
def get_user_by_id():
    data = User.getUserDetailsById()
    return data


  