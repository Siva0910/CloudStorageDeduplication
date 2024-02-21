from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class MyFileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=120)
    file = models.FileField()
    file_hash = models.CharField(max_length=64)
    upload_time = models.DateTimeField(auto_now_add=True)


class FileHash(models.Model):
    file_hash = models.CharField(max_length=64)
    count = models.IntegerField(default=1)
