from django.template.loader import render_to_string
from django.core import mail

connection = mail.get_connection()


def send_email(content, notification_type):
    from .models import notification_templates
    text = render_to_string(notification_templates[notification_type], content)
    connection.open()
    email = mail.EmailMessage(
        'Review',
        text,
        'from@example.com',
        ['to1@example.com'],
        connection=connection,
    )
    email.send()
    connection.close()



