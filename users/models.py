from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now
from django.contrib.auth.models import User


# Create your models here.


class Issuse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_text = models.TextField()
    report_image = models.ImageField(null=True, blank=True, upload_to='mydocs/images/')

    def __str__(self):
        return self.user.username
        



class Portfolio(models.Model):
    name = models.CharField(max_length=50)
    posision = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    phone2 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Services(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Projects(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    link = models.CharField(max_length=500)

    def __str__(self):
        return self.title



class Experience(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.title

class Certificates(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    imagelink = models.CharField(max_length=500, null=True, blank=True)
    filelink = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title