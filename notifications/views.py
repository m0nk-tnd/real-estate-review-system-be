from django.template.loader import render_to_string
from django.core import mail

connection = mail.get_connection()


def send_email(content, notification_type, subject):
    from .models import NotificationTemplate
    template = NotificationTemplate.objects.get(type=notification_type)
    email_template = template.email_template
    text = render_to_string(email_template, content)
    connection.open()
    email = mail.EmailMessage(
        subject,
        text,
        'from@example.com',
        ['to1@example.com'],
        connection=connection,
    )
    email.send()
    connection.close()
