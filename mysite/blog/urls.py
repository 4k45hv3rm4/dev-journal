from django.urls import path
from blog.views import *

urlpatterns  = [
    path("", index , name="index"),
    path("list/", post_list , name="post_list"),
    path("create/", create_post, name="create_post"),
    path('<str:slug>/' , post_detail,  name="post_detail"),
    ]
