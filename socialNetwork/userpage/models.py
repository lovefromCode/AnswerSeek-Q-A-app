from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(default='')
    answer = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_like', blank=True)
    dislikes = models.ManyToManyField(
        User, related_name='blog_dislike', blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return str(self.user)


class PossibleAnswers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    answers = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='ans_like', blank=True)
    dislikes = models.ManyToManyField(
        User, related_name='ans_dislike', blank=True)

    def __str__(self):
        return f"answer-{self.pk}"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    userImage = models.ImageField(
        upload_to="Profiles", default="default/default_pic.jpg")
    bio = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.user)


# What we need to define a comment modal
    # - comment
    # - user (one user can do multiple comments)
    # - post (one past have multiple comments)
    # - parent (parent of perticular comment. If ther is no parent then null)
    # - created_at
class StoryComment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment-{self.pk} by {self.user}"
