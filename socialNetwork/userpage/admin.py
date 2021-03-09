from django.contrib import admin
from . import models

admin.site.register(models.Post)
admin.site.register(models.Profile)
admin.site.register(models.StoryComment)
admin.site.register(models.PossibleAnswers)
