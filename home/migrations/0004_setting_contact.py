# Generated by Django 3.2 on 2021-05-18 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_setting_smtppassword'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='contact',
            field=models.TextField(blank=True),
        ),
    ]
