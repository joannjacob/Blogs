# Generated by Django 2.0.4 on 2018-04-09 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180409_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]