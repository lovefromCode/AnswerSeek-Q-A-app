# Generated by Django 3.1.7 on 2021-03-02 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0011_storycomment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(default=''),
        ),
    ]
