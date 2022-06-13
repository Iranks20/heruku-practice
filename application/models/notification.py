from abc import abstractstaticmethod
from flask import request, jsonify
from application.models.transaction import make_response
from helpers.db_helper import Database as db
from flaskext.mysql import MySQL
import uuid
import pymysql
from application.models.auth import token_required

#from application.libs.modal import Modal as md


class Notification:
    def __init__(self):
        print("notification model")

        #create notification
    @staticmethod
    @token_required
    def createNotification():
        try:
            _notification_id = uuid.uuid4()
            _json = request.json
            _message = _json['message']
            
            createNotification_dict = {"message": _message, "notification_id": _notification_id}
            data = db.insert('notification', **createNotification_dict)
            response = make_response(100, "notification statement created")
            return response

        except Exception as e:
            print(e)
            response = make_response(403, str(e))
            return response

    #display notification
    @staticmethod
    @token_required
    def all_notifications():
            sql = "SELECT * FROM `notification`"
            data = db.select(sql)
            response = jsonify(data)
            return response

    #delete notification
    @staticmethod
    def deleteNotification():
        try:
            _json = request.json
            _notificationId = _json['notification_id']
            sql = "DELETE FROM `notification` WHERE notification_id = '" + str(_notificationId) + "' "
            db.delete(sql)
            response = make_response(100, "notification deleted successfully")
            return response
        except Exception as e:
            print(e)
            response = make_response(403, "failed to delete the notification")
            return response






# responses
def make_response(status, message):
    return jsonify({"message": message, "status": status})



