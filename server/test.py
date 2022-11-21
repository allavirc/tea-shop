from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_date = models.DateField(auto_now_add=True)

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    created_date = models.DateField(auto_now_add=True)
    text = models.TextField()

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_date = models.DateField(auto_now_add=True)

class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    created_date = models.DateField(auto_now_add=True)

