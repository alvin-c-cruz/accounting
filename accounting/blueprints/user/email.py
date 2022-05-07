from flask_mail import Message
from accounting import mail


def send_email(app, to, subject, html):
    msg = Message(
        subject=subject,
        recipients=[to],
        html=html,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )

    mail.send(msg)
