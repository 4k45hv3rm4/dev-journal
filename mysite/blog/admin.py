from django.contrib import admin
from .models import Post, Comment, UserProfile



admin.site.register(Comment)
admin.site.register(UserProfile)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
