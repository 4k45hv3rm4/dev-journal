from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.urls import reverse
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('publish', 'Publish')
        )
    title    = models.CharField(max_length=250)
    slug     = models.CharField(max_length=250, unique=True)
    author   = models.ForeignKey(User, on_delete=models.CASCADE)
    image    = models.ImageField(upload_to="images/", null=True, blank=True)
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
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)
    author    = models.OneToOneField(User,on_delete=models.CASCADE)
    email   = models.EmailField()
    body    = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update  = models.DateTimeField(auto_now = True)
    active  = models.BooleanField(default = True)


    class Meta:
        ordering = ('created',)
    def __str__(self):
        return 'comment by {} on {} '.format(self.name, self.post)


class UserProfile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to="profile_images/", blank=True)

    def __str__(self):
        return self.user
