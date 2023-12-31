from threading import Thread
from flask import current_app
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(**msg)


def send_email(subject, recipients, text_body, html_body, sender=None, attachments=None, sync=False):
    msg = dict(subject=subject, sender=sender, receivers=recipients, text=text_body, html=html_body)
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(**msg)
    else:
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

