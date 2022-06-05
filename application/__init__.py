from email.mime import application
from flask import Flask, redirect, request
from helpers.db_helper import DB as DB_CON

application = Flask(__name__)
application.config['SECRET_KEY'] = 'your secret key'

