# Generated by Django 3.1.6 on 2021-04-13 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0010_notification_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='receiver',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
