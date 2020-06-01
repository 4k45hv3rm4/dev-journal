#imports
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView
from django.http import HttpResponseRedirect
from mysite.settings import LOGIN_REDIRECT_URL
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import (
            Post,
            Comment,
            Account
        )

from django.shortcuts import (
            render,
            get_object_or_404,
            redirect
        )
from .forms import (
            PostForm,
            CommentForm,
            UpdatePostForm,
            SearchForm
        )
from django.contrib.auth import (
            authenticate,
            logout ,
            login
        )
from operator import attrgetter
from django.shortcuts import render,redirect
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateform
from .models import Post


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email    = form.cleaned_data.get('email')
            raw_pass = form.cleaned_data.get('password1')
            account = authenticate(email=email, password = raw_pass)
            login(request, account)
            return redirect('post_list')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, "blog/register.html", context)


def logout_view(request):
    logout(request)
    return redirect("post_list")



def  login_view(request):
    context = {}

    user = request.user

    if user.is_authenticated:
        return redirect("post_list")
    if request.POST:
        form    = AccountAuthenticationForm(request.POST)
        email   = request.POST.get('email')
        password = request.POST.get('password')
        user =  authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect("post_list")
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form

    return render(request, "blog/login.html", context)



def account_view (request):
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    if request.POST:
        form = AccountUpdateform(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
    else:
        form  = AccountUpdateform(
            initial={
            'email':request.user.email,
            'username':request.user.username,
            }
        )
    context['account_form']=form
    blog_posts = Post.objects.filter(author=request.user)
    context['blog_posts']=blog_posts
    return render(request, "blog/userprofile.html", context)

def must_authenticate(request):
    return render(request, "blog/must_authenticate.html",{})


# About
def index(request):

    return render(request, "base.html", {})

# list of posts
def post_list(request):
    obj = Post.objects.filter(status="publish")
    query = ""
    context={}
    if request.GET:
        query = request.GET.get('q', '')
        print(query)
        context['query'] = str(query)
    obj = sorted(get_blog_queryset(query), key=attrgetter('updated'), reverse=True)
    context['obj']  = obj
    return render(request, "blog/post_list.html", context)



# User logout
@login_required(login_url=LOGIN_REDIRECT_URL)
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('post_list'))


@login_required(login_url=LOGIN_REDIRECT_URL)
# create new post
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


# detail for a particular post
def post_detail(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    comments = obj.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
    # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid() :
        # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
        # Assign the current post to the comment
            new_comment.author=request.user
            new_comment.post = obj

        # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {
    'obj':obj,
    'comments': comments,
    'new_comment': new_comment,
    'comment_form': comment_form}
    return render(request, "blog/post_detail.html",context)

@login_required(login_url=LOGIN_REDIRECT_URL)
# update a particular post
def post_update(request, slug):
    context = {}
    user  = request.user
    post = get_object_or_404(Post, slug=slug)
    if request.method=='POST':
        form = UpdatePostForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "updated"
            post = obj
            return HttpResponseRedirect(post.get_absolute_url())


    form = UpdatePostForm(
    initial={
    'title':post.title,
    'body':post.body,
    'image':post.image
    })

    context['form'] = form
    return render(request, "blog/post_update.html", context)

# delete a particular post
class post_delete(LoginRequiredMixin,DeleteView):
    model = Post
    template_name="blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")

@login_required(login_url=LOGIN_REDIRECT_URL)
def profile_page(request):

    obj = get_object_or_404(UserProfile, user=request.user)
    print(obj.about)
    return render(request, 'blog/userprofile.html', {'obj':obj})

@login_required(login_url=LOGIN_REDIRECT_URL)
def create_profile(request):
    form = UserProfileForm()
    if request.method=="POST":
        form = UserProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return HttpResponseRedirect("/blog/profile/")
    else:
        form = UserProfileForm()
    return render(request, 'blog/userprofileform.html', {'form':form})


@login_required(login_url=LOGIN_REDIRECT_URL)
def update_user_profile(request):

    userobj = get_object_or_404(UserProfile, user=request.user)
    theuser = get_object_or_404(User, username=request.user.username)
    if request.method=="POST":

        user_form = EditUserForm(data=request.POST, instance=request.user)
        profile_form = UpdateUserProfile(data=request.POST,files=request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            p_form = profile_form.save(commit=False)
            p_form.save()
            return HttpResponseRedirect("/blog/profile")

    profile_form = UpdateUserProfile(
        initial={

        'about':userobj.about,
        'picture':userobj.picture,
        })
    user_form = EditUserForm(
        initial = {
        'email': theuser.email,
        'username':theuser.username
        })
    return render(request, "blog/userprofileupdate.html", {'user_form':user_form, 'profile_form':profile_form})



def draft_list(request):
    obj = Post.objects.filter(author=request.user).filter(status="draft")
    return render(request, "blog/draft_list.html",{'obj':obj})




def get_blog_queryset(query=None):
    queryset = []
    queries=  query.split(" ")
    for q in queries :
        posts = Post.objects.filter(
            Q(title__icontains=q)|
            Q(body__icontains=q)
        ).distinct().filter(status="publish")
        for post in posts:
            queryset.append(post)
    return list(set(queryset))
