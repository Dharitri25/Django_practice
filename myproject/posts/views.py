from django.shortcuts import render, redirect
from .models import Post
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.
def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html', {'post': post})

@login_required(login_url='/user/login/')
def post_new(request):
    if request.method == "POST":
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.save()
            return redirect('post:list')

    else:
        form = forms.CreatePost()
    return render(request, 'posts/post_new.html', {'form': form})