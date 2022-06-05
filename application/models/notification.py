from abc import abstractstaticmethod
from flask import request, jsonify
from helpers.db_helper import Database as db
from flaskext.mysql import MySQL
#from application.libs.modal import Modal as md


class Notification:
    def __init__(self):
        print("notification model")

        #create notification
    @staticmethod
    def createNotification():
        try:
            _json = request.json
            _message = _json['message']
            _user_id = _json['user_id']
            
            createNotification_dict = {"message": _message, "user_id": _user_id}
            data = db.insert('notification', **createNotification_dict)
            response = jsonify(100, "notification statement created")
            return response

        except Exception as e:
            print(e)
            response = jsonify(403, str(e))
            return response

    #display notification
    @staticmethod
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
            response = jsonify(100, "notification deleted successfully")
            return response
        except Exception as e:
            print(e)
            response = jsonify(403, "failed to delete the notification")
            return response
