# Generated by Django 3.1.7 on 2021-03-01 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0009_auto_20210301_0619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storycomment',
            name='parent',
        ),
    ]
