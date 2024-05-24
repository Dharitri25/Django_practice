from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.posts_list, name="list"),
    path('<slug:slug>', views.post_page, name="page"),
    path('new-post/', views.post_new, name="post_new"),
]

