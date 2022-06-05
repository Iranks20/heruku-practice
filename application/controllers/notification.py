
from flask import Blueprint, request, jsonify, json
from application.models.notification import Notification
#from application.libs.modal import Modal as md

bp_app = Blueprint('mod_notification', __name__)

#create notification 
@bp_app.route('/create_notification', methods=['POST'])
def create_notification():
    data = Notification.createNotification()
    return data

    #display notifcation
@bp_app.route('/all_notifications', methods=['GET'])
def getNotifications():
    data = Notification.all_notifications()
    return data

    #deletenotification
@bp_app.route('/delete_notification', methods=['DELETE'])
def delete_notification():
    data = Notification.deleteNotification()
    return data  