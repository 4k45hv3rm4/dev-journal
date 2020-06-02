from django import forms
from blog.models import Post, Comment, Account
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account
from django.contrib.auth import authenticate

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text = 'Required. Add a valid email address')
    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')


class AccountAuthenticationForm(forms.ModelForm):
    password  = forms.CharField(label= 'Password', widget=forms.PasswordInput)

    class Meta:
        model  =  Account
        fields =  ('email', 'password')

    def clean(self):
        if self.is_valid():

            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')

class AccountUpdateform(forms.ModelForm):
    class Meta:
        model  = Account
        fields = ('email', 'username')
    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk = self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError("Email '%s' already in use." %email)
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk = self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError("Username '%s' already in use." % username)


class PostForm(forms.ModelForm):
    class Meta():
        model   = Post
        fields  = ('title', 'body', 'status', 'image','tags')
        widgets = {
                   'title':forms.TextInput(attrs={'class':'textinputclass'}),
                   'body':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }


    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in (self.fields['title'],self.fields['body'],self.fields['status']):
            field.widget.attrs.update({'class': 'form-control '})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})

class CommentForm(forms.ModelForm):
    class Meta():
        model    = Comment
        fields   = ('body',)
        widgets  = {
            'body':forms.Textarea(attrs={'class':'editable medium-editor-textarea '})

        }



class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image','status', 'body', 'tags']
    def save(self, commit=False):
        blog_post = self.instance
        blog_post.title = self.cleaned_data['title']
        blog_post.body  = self.cleaned_data['body']
        blog_post.status = self.cleaned_data['status']

        if self.cleaned_data['image']:
            blog_post.image = self.cleaned_data['image']
        if commit:
            blog_post.save()
        return blog_post


class SearchForm(forms.Form):
    query = forms.CharField()
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs.update({'class': 'form-control '})

