import flask

import os

from dotenv import load_dotenv
load_dotenv()


def fetch_json():
    _json = flask.request.json
    return _json


def mail_data():
    from api import db
    from flask_login import current_user
    from bson.objectid import ObjectId

    sender = db.find_one({"_id": ObjectId(current_user.get_id())})
    _json = fetch_json()
    recipients, subject, body = _json["to"], _json["subject"], _json["body"]
    return sender, recipients, subject, body
    
def flask_mailer():
    from flask_mail import Message
    from api import mail

    sender, recipients, subject, body = mail_data()
    msg = Message(subject=subject,
                 sender=sender,
                 recipients=[recipients],
                 body=body)
    try:
        mail.send(msg)
    except Exception:
        return flask.jsonify({"status":400, "message":"something went terribly wrong"})
    return flask.jsonify({"status":200, "message":"message sent successfully"})


def smpt_mailer():
    import smtplib, ssl

    sender, recipients, _, body = mail_data()
    context = ssl.create_default_context()
    with smtplib.SMTP(os.getenv('MAIL_SERVER'), os.getenv('MAIL_PORT')) as server:
        server.starttls(context=context)
        server.ehlo()
        server.login(sender, os.getenv('MAIL_PASSWORD'))
        server.sendmail(sender, recipients, str(body).strip())

        
def mailer_func(use_flask_mail=None):
    return smpt_mailer if not use_flask_mail else flask_mailer