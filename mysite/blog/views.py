from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Post, Comment, UserProfile
from django.views.generic import (ListView)
from django.utils import timezone
from .forms import UserForm, UserProfileForm, PostForm, CommentForm

def index(request):
    return render(request, "base.html", {})

def post_list(request):
    obj = Post.objects.filter(status="publish")
    return render(request, "blog/post_list.html", {'obj':obj})


def create_post(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())
    context = {
    'form':form
    }
    return render(request, "blog/post_form.html", context)


def post_detail(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    context = {
    'obj':obj}
    return render(request, "blog/post_detail.html",context)

