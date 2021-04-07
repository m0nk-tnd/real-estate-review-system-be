from django.template.loader import render_to_string
from django.core import mail

connection = mail.get_connection()


def send_email(notification):
    from .models import NotificationTemplate
    template = NotificationTemplate.objects.get(type=notification.template.type)
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
    connection.close()
