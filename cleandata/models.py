from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from collectdata.models import BaseData
# Create your models here.


class CleanData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    clean_file = models.FileField(verbose_name="clean_file", upload_to='mydocs/')  
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
