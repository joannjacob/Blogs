# Generated by Django 2.0.4 on 2018-04-09 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180409_1757'),
    ]

    operations = [
        migrations.RenameField(
            model_name='signup',
            old_name='email',
            new_name='emailid',
        ),
    ]
