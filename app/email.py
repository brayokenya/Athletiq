from flask_mail import Message
from flask import render_template
from . import mail


def mail_message(subject,template,to,**kwargs):
    sender_email = 'seniordev41@gmail.com'
    email = Message(subject, sender=sender_email, recipients=[to])
    email.html = render_template(template + ".html",**kwargs)
    mail.send(email)

def request_status(subject,template,to,**kwargs):
    sender_email = 'seniordev41@gmail.com'
    email = Message(subject, sender=sender_email, recipients=[to])
    email.html = render_template(template + ".html",**kwargs)
    mail.send(email)