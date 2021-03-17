from django.shortcuts import render
from django.template.loader import render_to_string
from django.core import mail


def send_email(content):
    text = render_to_string('review_notification.html', content)
    connection = mail.get_connection()
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



