# Generated by Django 3.2.8 on 2021-10-07 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_confirmed',
            field=models.BooleanField(default=False, help_text='Designates whether the user has verified the email address.', verbose_name='email verified'),
        ),
    ]
