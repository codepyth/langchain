from .forms import PostForm, CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
import openai
from .models import Post
from rest_framework.decorators import api_view
from rest_framework.response import Response
from langchaintry import config
from rest_framework import status
from rest_framework.exceptions import APIException


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('create_post')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return render(request, 'post_detail.html')   # Replace 'post_detail' with the URL name of your post detail page
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})



def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return render(request, 'post_detail.html', post_id=post_id)  # Replace 'post_detail' with the URL name of your post detail page
    else:
        form = CommentForm()
    return render(request, 'create_comment.html', {'form': form})



def post_detail(request):
    posts = Post.objects.all()
    # comments = posts.comments.all()
    return render(request, 'post_detail.html', {'posts': posts})

@api_view(['GET', 'POST'])
def quest_ans(request):
    data = request.data
    text = data['text'] if 'text' in data else None
    if text is not None:
        try:
            openai.api_key = config.OPEN_API_KEY
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=text,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7,
            )
            result = response.choices[0].text.strip()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException("Error occurred during processing: " + str(e))
    else:
        return Response({"message": "Enter valid text"}, status=status.HTTP_400_BAD_REQUEST)