from django.template.loader import render_to_string
from django.core import mail


def send_email_notifications():
    from .models import Notification
    notifications = Notification.objects.filter(sent=False)
    connection = mail.get_connection()
    for notification in notifications:
        _send_one_notification(notification, connection)
    connection.close()


def _send_one_notification(notification, connection):
    template = notification.template
    notification.sent = True
    notification.save()
    email_template = template.email_template
    text = render_to_string(email_template, notification.data)
    connection.open()
    email = mail.EmailMessage(
        template.subject,
        text,
        'from@example.com',
        ['to1@example.com'],
        connection=connection,
    )
    email.send()
