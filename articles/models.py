from django.db import models
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Article(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    content = models.TextField("내용")
    image = models.ImageField("이미지", upload_to='%Y/%m/')
    created_at = models.DateTimeField("생성 시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정 시간", auto_now=True)
    likes = models.ManyToManyField(
        User, related_name='like_articles', blank=True)
    stars = models.PositiveIntegerField(
        '별점', validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField("내용", max_length=50)
    created_at = models.DateTimeField("생성 시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정 시간", auto_now=True)

    def __str__(self):
        return self.content
