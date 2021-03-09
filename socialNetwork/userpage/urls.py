from django.urls import path
from . import views

urlpatterns = [
    path('', views.userHome, name='userHome'),
    path("search", views.searchPost, name='searchPost'),
    path('ss/<int:ID>', views.userStory, name='userStory'),
    path('post', views.post, name='post'),
    path('postDone', views.postDone, name='postDone'),
    path("delete/<int:ID>", views.delPost, name='delPost'),
    path("like/<int:ID>", views.like, name='like'),
    path("dislike/<int:ID>", views.dislike, name='dislike'),
    path("comment/<int:ID>", views.commentPost, name='commentPost'),
    path("answer/<int:ID>", views.answerPost, name='answerPost'),
    path("profile/<str:username>", views.userProfile, name='user_profile'),
    path("editprofile/<str:username>", views.editProfile, name='editProfile'),
]
