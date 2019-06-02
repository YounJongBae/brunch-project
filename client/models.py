from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Hashtag(models.Model):
    name = models.CharField(
    max_length=10,
    verbose_name="해쉬태그"
    )

    def __str__(self):
        return self.name

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=30,
        verbose_name = "닉네임"
    )

    def __str__(self):
        return self.name

class Article(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    TECH = 'TECH'
    TRAVEL = 'TRAVEL'
    HEALTH = 'HEALTH'
    CULTURE = 'CULTURE'
    CATEGORY_CHOICES = (
        (TECH, 'IT·기술'),
        (TRAVEL, '여행'),
        (HEALTH, '건강·운동'),
        (CULTURE, '음악·예술·책'),
    )
    title = models.CharField(
        max_length=50,
        verbose_name="글제목"
    )
    subtitle = models.CharField(
        max_length=70,
        verbose_name="소제목"
    )
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        verbose_name="카테고리"
    )
    content = models.TextField(
        verbose_name="내용"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    hashtag = models.ManyToManyField(Hashtag)

    class Meta:
         ordering = ['-created_at']

    def __str__(self):
        return self.title



class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        related_name="article_comment",
        on_delete=models.CASCADE
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    content = models.CharField(
        max_length=200,
        verbose_name="댓글내용"
    )

    def __str__(self):
        return "{}에 댓글 : {}".format(self.article.title, self.content)
