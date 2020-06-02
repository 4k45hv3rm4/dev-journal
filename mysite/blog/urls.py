from django.urls import path
from blog.views import *

urlpatterns  = [
    path('register/',registration_view, name="register" ),
    path('logout/',logout_view, name="logout" ),
    path('login/',login_view, name="login" ),
    path('profile/',account_view, name="account" ),
    path("index/", index , name="about"),
    path("", post_list , name="post_list"),
    path("tag/<slug:tag_slug>/", post_list , name="post_list_by_tag"),
    # path("profile/", profile_page , name="user_profile"),
    path("create_profile/", create_profile , name="create_profile"),
    path("drafts/", draft_list, name="drafts"),
    path("update_profile/", update_user_profile , name="update_profile"),
    path("create/", create_post, name="create_post"),
    path('update/<str:slug>', post_update, name="post_update"),
    path('delete/<str:slug>', post_delete.as_view(), name="post_delete"),
    path('<str:slug>/' , post_detail,  name="post_detail"),

   ]
