from flask import jsonify, json
from werkzeug.utils import secure_filename
from helpers.db_helper import Database as db

@staticmethod
def get_user_by_id(user_id):
        sql = "SELECT * FROM user WHERE user_id = '" + user_id + "' "
        data = db.select(sql)
        return data

@staticmethod
def make_response(status, message):
        rsp = {'status': status, 'response': message}
        if status == 100:
            code = 200
        elif status == 404:
            code = 404
        else:
            code = 403
        return jsonify(rsp), code

def make_this_response(status, message):
    rsp = {'status': status, 'response': message}
    if status == 100:
        code = 200
    elif status == 404:
        code = 404
    else:
        code = 403
    return jsonify(rsp), code
 
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except Exception as e:
        return False
    return True

def is_valid(request):
    if request is None:
        return False
    return True

def return_data(status, message):
    return {'status': status, 'response': message}  
