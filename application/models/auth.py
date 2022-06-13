
from functools import wraps
from urllib import response
from flask import jsonify, request
import jwt
from application import application
from datetime import datetime


# requesting jwt token
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        data = request.headers.get('Authorization')
        token = str.replace(str(data), 'Bearer ', '')
        print(data)
        #token = request.args.get('token')
        if data == None:
            return jsonify({'Alert!': 'Token is missing!'})
        try:
            data = jwt.decode(token, application.config['SECRET_KEY'], algorithms=['HS256'])
            if data['expiration'] < str(datetime.now()):
                return jsonify({"status": "token expired"})
            #data = jwt.decode(token, application.config['SECRET_KEY'], algorithms=['HS256'])
        #except:
            #return jsonify({'Alert!': 'invalid token!'})
        except Exception as e:
            print(e)
            response = make_response(403, "wrong token filled")
            return response
        return func(*args, **kwargs)  
    return decorated






def make_response(status, message):
    return jsonify({"status":status, "message":message})
