# Generated by Django 3.1.4 on 2021-03-06 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0018_auto_20210306_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='userImage',
            field=models.ImageField(default='default/default.png', null=True, upload_to='Profiles'),
        ),
    ]
