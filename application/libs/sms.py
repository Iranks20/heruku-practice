from flask_mail import Mail, Message
from application import application

application.config['MAIL_SERVER'] = 'smtp.gmail.com'
application.config['MAIL_PORT'] = 465
application.config['MAIL_USERNAME'] = 'irankundainnocent673@gmail.com'
application.config['MAIL_PASSWORD'] = 'kvsx gotx szbx srgv'
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True

mail = Mail(application)

def send(OTP, RECEIVER):
    msg = Message('EREMIT LTD', sender = 'irankundainnocent673@gmail.com', recipients = [RECEIVER])
    msg.body = " the otp sent is " + str(OTP) + ". verify your email with this OTP!!!"
    mail.send(msg)
    return "otp sent to " + RECEIVER + " successfully"