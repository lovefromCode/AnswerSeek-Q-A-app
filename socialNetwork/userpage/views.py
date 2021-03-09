from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Post, Profile
from django.contrib import messages
from .models import Post, Profile, StoryComment, PossibleAnswers


def userHome(request):
    # fetching post from database
    posts = Post.objects.order_by('-created_at').all()
    data = {
        'posts': posts,
    }
    return render(request, "userpage/homepage.html", data)


def userStory(request, ID):
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

    data = {
        'posts': posts,
        'isLiked': isLiked,
        'isDisliked': isDisliked,
        'comments': comments,
        'answers': answers,
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
