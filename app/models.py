from django.db import models
models.CharField()
# Create your models here.

class User(models.Model):
    user=models.CharField(max_length = 32)
    pwd=models.CharField(max_length = 32)

class Img(models.Model):
    path = models.CharField(max_length=128)
