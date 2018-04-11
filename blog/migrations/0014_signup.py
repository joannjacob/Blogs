# Generated by Django 2.0.4 on 2018-04-09 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0013_delete_signup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('emailid', models.CharField(default='', max_length=100, unique=True)),
                ('mobile', models.CharField(default='', max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
