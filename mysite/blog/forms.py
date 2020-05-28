from django import forms
from blog.models import Post, Comment, UserProfile
from django.contrib.auth.models import User



class PostForm(forms.ModelForm):
    class Meta():
        model   = Post
        fields  = ('title', 'body', 'status', 'image')
        widgets = {
                   'title':forms.TextInput(attrs={'class':'textinputclass'}),
                   'body':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }



class CommentForm(forms.ModelForm):
    class Meta():
        model    = Comment
        fields   = ('author','body')
        widgets  = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'body':forms.Textarea(attrs={'class':'editable medium-editor-textarea '})

        }

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in (self.fields['username'],self.fields['password'],self.fields['email']):
            field.widget.attrs.update({'class': 'form-control '})
    class Meta:
        model = User
        fields=('username','email','password')

class UserProfileForm():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['website'].widget.attrs.update({'class': 'form-control '})
        self.fields['picture'].widget.attrs.update({'class': 'form-control-file'})
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
