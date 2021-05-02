from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Post, Profile
from django.contrib import messages
from .models import Post, Profile, StoryComment, PossibleAnswers
import csv
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import random


#### --- for exporting data form database into csv format --- ####
def exportData(request):
    response = HttpResponse(content_type="text/csv")

    writer = csv.writer(response)
    writer.writerow(['UserName', 'Question', 'Answer',
                     'Created_at', 'Likes', 'Dislikes'])

    for post___ in Post.objects.all().values_list('user', 'question', 'answer', 'created_at', 'likes', 'dislikes'):
        writer.writerow(post___)

    response['Content-Disposition'] = 'attachment; filename="posts_.csv"'
    return response

# -------------------- #


def userHome(request):
    # fetching post from database
    posts = Post.objects.order_by('-created_at').all()

    all_choices = []
    for p in posts:
        all_choices.append(p.question)

    ########## --- Machine Learning part --- ###########
    data1 = pd.read_csv(
        "/Users/prashantmaitra/Downloads/posts.csv", encoding='latin1')

    tf = TfidfVectorizer(analyzer='word', ngram_range=(
        1, 3), min_df=0, stop_words='english')

    matrix = tf.fit_transform(data1['Answer'])

    cosine_similarities = linear_kernel(matrix, matrix)

    question = data1['Question']

    indices = pd.Series(data1.index, index=data1['Question']).drop_duplicates()

    idx = indices[random.choice(all_choices)]

    sim_scores = list(enumerate(cosine_similarities[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:31]

    question_indices = [i[0] for i in sim_scores]

    final_recommandation = question.iloc[question_indices].tolist()

    grandFinal = []
    for j in range(0, 4):
        grandFinal.append(final_recommandation[j])
        # print(grandFinal)

    ########### ---- Recommendation ends ---- ############
    data = {
        'posts': posts,
        'grandFinal': grandFinal,
    }
    return render(request, "userpage/homepage.html", data)



def userStory(request, ID):
    all_posts = Post.objects.order_by('-created_at').all()
    posts = Post.objects.get(pk=ID)
    answers = PossibleAnswers.objects.filter(post=posts)
    comments = StoryComment.objects.order_by('-created_at').filter(post=posts)

    if posts.likes.filter(id=request.user.id).exists():
        isLiked = True
    else:
        isLiked = False

    if posts.dislikes.filter(id=request.user.id).exists():
        isDisliked = True
    else:
        isDisliked = False

    all_choices = []
    for p in all_posts:
        all_choices.append(p.question)

    ########## --- Machine Learning part --- ###########
    data1 = pd.read_csv(
        "/Users/prashantmaitra/Downloads/posts.csv", encoding='latin1')

    tf = TfidfVectorizer(analyzer='word', ngram_range=(
        1, 3), min_df=0, stop_words='english')

    matrix = tf.fit_transform(data1['Answer'])

    cosine_similarities = linear_kernel(matrix, matrix)

    question = data1['Question']

    indices = pd.Series(data1.index, index=data1['Question']).drop_duplicates()

    idx = indices[random.choice(all_choices)]

    sim_scores = list(enumerate(cosine_similarities[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:31]

    question_indices = [i[0] for i in sim_scores]

    final_recommandation = question.iloc[question_indices].tolist()

    grandFinal = []
    for j in range(0, 4):
        grandFinal.append(final_recommandation[j])
        # print(grandFinal)

    ########### ---- Recommendation ends ---- ############

    data = {
        'posts': posts,
        'isLiked': isLiked,
        'isDisliked': isDisliked,
        'comments': comments,
        'answers': answers,
        'grandFinal': grandFinal,
    }
    return render(request, 'userpage/userAnswers.html', data)


def delPost(request, ID):
    # every post have a unique identity
    post_ = Post.objects.filter(pk=ID)
    post_.delete()
    messages.info(request, "Post Deleted")
    return redirect('/')


def userProfile(request, username):
    user = User.objects.filter(username=username).first()
    if user:
        profile = Profile.objects.get(user=user)
        total_post = count_posts(user)
        allStory = getStory(user)

        data = {
            'user_obj': profile,
            'allStory': allStory,
            'total_post': total_post,
        }
    else:
        return HttpResponse("NO SUCH USER.......")

    return render(request, 'userpage/userProfile.html', data)


def getStory(user):
    post_obj = Post.objects.filter(user=user)
    imgList = []
    for post in post_obj:
        imgList.append(post)
    return imgList

def count_posts(user):
    post_obj = Post.objects.filter(user=user)
    c = 0
    for post in post_obj:
        c += 1   
    return c

def post(request):
    return render(request, 'userpage/postingQues.html')


def postDone(request):
    if request.method == 'POST':
        user = request.user
        question = request.POST['question']
        answer = request.POST['answer']

        # if question has already asked.
        if(Post.objects.filter(question=question).exists()):
            messages.warning(request, "Question already exits. please ask another")
            return render(request, 'userpage/postingQues.html')
        else:
            post_obj = Post(user=user, question=question,
                            answer=answer)
            post_obj.save()
            messages.success(request, "We Showed Them!!!")
            return redirect("/")
    else:
        messages.error(request, "Something went Wrong :(")
        return render(request, 'userpage/postingQues.html')


def like(request, ID):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    isLiked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        isLiked = False
    else:
        post.likes.add(request.user)
        isLiked = True

    posts = Post.objects.get(pk=ID)
    answers = PossibleAnswers.objects.filter(post=posts)
    data = {
        'posts': posts,
        'isLiked': isLiked,
        'answers': answers,
    }
    return render(request, 'userpage/userAnswers.html', data)



def dislike(request, ID):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    isDisliked = False
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
        isDisliked = False
    else:
        post.dislikes.add(request.user)
        isDisliked = True

    posts = Post.objects.get(pk=ID)
    answers = PossibleAnswers.objects.filter(post=posts)
    data = {
        'posts': posts,
        'isDisliked': isDisliked,
        'answers': answers,
    }
    return render(request, 'userpage/userAnswers.html', data)


def commentPost(request, ID):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        post = Post.objects.get(id=ID)
        comment_obj = StoryComment(comment=comment, user=user, post=post)
        comment_obj.save()
        messages.success(request, "comment posted successfully")

    return redirect(f"/ss/{post.id}")


def answerPost(request, ID):
    if request.method == 'POST':
        answer = request.POST.get('myans')
        user = request.user
        post = Post.objects.get(id=ID)
        answer_obj = PossibleAnswers(answers=answer, user=user, post=post)
        answer_obj.save()
        messages.success(request, "answer posted successfully")

    return redirect(f"/ss/{post.id}")


def searchPost(request):
    query = request.GET['qr']
    if len(query) > 70:
        allpost = Post.objects.none()
    else:
        post_ans = Post.objects.order_by('-created_at').filter(answer__icontains=query)
        post_ques = Post.objects.order_by('-created_at').filter(question__icontains=query)
        allpost = post_ans | post_ques

    data = {
        'allpost': allpost,
        'query': query,
    }

    return render(request, 'userpage/searchPage.html', data)


def editProfile(request, username):
    user = User.objects.filter(username=username).first()
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        name = request.POST['name']
        image = request.FILES["image"]

        profile.bio = name
        profile.userImage = image
        profile.save()

    return redirect(f"/profile/{user}")
