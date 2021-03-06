# Generated by Django 3.1.4 on 2021-03-02 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userpage', '0012_post_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='content',
            new_name='answer',
        ),
        migrations.RemoveField(
            model_name='post',
            name='caption',
        ),
        migrations.AddField(
            model_name='post',
            name='question',
            field=models.TextField(default=''),
        ),
        migrations.CreateModel(
            name='PossibleAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('answers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userpage.post')),
                ('dislikes', models.ManyToManyField(blank=True, related_name='ans_dislike', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='ans_like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
