from django.contrib import admin
from .models import Client, Article, Comment, Hashtag

# Register your models here.
@admin.register(Client, Article, Comment, Hashtag)
class FeedAdmin(admin.ModelAdmin):
    pass
