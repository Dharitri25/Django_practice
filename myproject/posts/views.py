from django.shortcuts import render, redirect
from .models import Post, User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages

# post list
def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/post_list.html', {'posts': posts})


# post by slug
def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html', {'post': post})


# post by title
def post_page_by_title(request, title):
    post = Post.objects.get(title = title)
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


# delete post by id
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('post:list')


# update post by id
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = forms.CreatePost(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return render(request, 'posts/post_page.html', {'post': post})
    else:
        form = forms.CreatePost(instance=post)
    return render(request, 'posts/post_edit.html', {'post': post})


# get postname list
def postnames_list(request):
    posts = Post.objects.values_list("title", flat=True).order_by('-date')
    return render(request, '../templates/about.html', {"posts": posts})


# get user-posr list
def post_user_list(request):
    users = Post.objects.values_list('author', flat=True)
    userArr = []
    added_usernames = set()
    for user in users:
        userobj = User.objects.filter(id = user).first()
        if userobj:
            username = userobj.username
        if username not in added_usernames:
            total_posts = Post.objects.filter(author=user).count()
            context = {
                'userId': user,
                'user': username,
                'totalPosts': total_posts,
            }
            userArr.append(context)
            added_usernames.add(username)
    return render(request, '../templates/about.html', {"user_posts": userArr})


# get post according to searched title
def search_post_title(request, title):
    posts = Post.objects.filter(title__icontains = title).order_by('-date').values()
    return JsonResponse({'posts': list(posts)})


# get posts by username
def postsByUser(request, user):
    posts = Post.objects.filter(author = user).order_by('-date').values()
    #for json response
    # return JsonResponse({'posts': list(posts)}) 

    # for post page render with returned data
    return render(request, 'posts/post_list.html', {'posts': posts}) 


# delete posts user wise
def postsDeleteByUser(request, user):
    username = User.objects.filter(id = user).first()
    if username is None:
        return HttpResponse(404 , "user not found !")
    posts = Post.objects.filter(author = user)
    posts.delete()
    messages.success(request, f"All posts created by {username} deleted successfully.")
    return post_user_list(request)