from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.posts_list, name="list"),
    path('<slug:slug>', views.post_page, name="page"),
    path('new-post/', views.post_new, name="post_new"),
    path('post-names/', views.postnames_list, name="postnames-list"),
    path('post_delete/<int:id>', views.post_delete, name="post_delete"),
    path('post_edit/<int:id>', views.post_edit, name="post_edit"),
    path('post_page_by_title/<str:title>', views.post_page_by_title, name="post_page_by_title"),
    path('post_user_list/', views.post_user_list, name="post_user_list"),
    path('search_post_title/<str:title>', views.search_post_title, name="search_post_title"),
    path('posts_by_user/<str:user>', views.postsByUser, name='posts_by_user'),
    path('posts_delete_by_user/<str:user>', views.postsDeleteByUser, name="posts_delete_by_user"),
]