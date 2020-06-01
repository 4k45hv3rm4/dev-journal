from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import  post_save, post_delete
from django.urls import reverse
from django.dispatch import receiver
from django.conf import settings


def upload_location(instance, filename, *args, **kwargs):
    file_path = 'blog/{author_id}/{title}-{filename}'.format(author_id=str(instance.author.id), title=str(instance.title), filename=filename
        )
    return file_path


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('publish', 'Publish')
        )
    title    = models.CharField(max_length=250)
    slug     = models.CharField(max_length=250, unique=True)
    author   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image    = models.ImageField(upload_to=upload_location, null=True, blank=True)
    body     = models.TextField()
    publish  = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)
    status   = models.CharField(max_length=10,
                                choices=STATUS_CHOICES,
                                default="draft")

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'slug':self.slug })


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)



class Comment(models.Model):
    post    = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author  = models.OneToOneField(settings.AUTH_USER_MODEL, max_length=100, on_delete=models.CASCADE)
    email   = models.EmailField()
    body    = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update  = models.DateTimeField(auto_now = True)
    active  = models.BooleanField(default = True)


    class Meta:
        ordering = ('created',)
    def __str__(self):
        return 'comment by {} on {} '.format(self.author, self.post)




from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("users must have an emial address")
        if not username :
            raise ValueError("users must have an username")
        user  = self.model(
                email=self.normalize_email(email),
                username=username,
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
                email=self.normalize_email(email),
                password=password,
                username=username,
            )
        user.is_admin = True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
class Account(AbstractBaseUser):
    email                = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username             = models.CharField(max_length=30,unique=True)
    date_joined          = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login           = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin             = models.BooleanField(default=False)
    is_active            = models.BooleanField(default=True)
    is_staff             = models.BooleanField(default=False)
    is_superuser         = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = MyAccountManager()
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label ):
        return True

