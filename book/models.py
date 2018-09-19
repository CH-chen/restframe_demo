from django.db import models

# Create your models here.

class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    type_choice = ((1,"普通用户"),(2,"VIP"),(3,"SVIP"))
    user_type = models.IntegerField(choices=type_choice,default=1)

class UserToken(models.Model):
    token = models.CharField(max_length=128)
    userinfo = models.OneToOneField(to="UserInfo")
    def __str__(self):
        return self.token

class Publish(models.Model):
    name= models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    email = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    pub_date = models.DateField()
    publish = models.ForeignKey(to="Publish")
    authors = models.ManyToManyField(to="Author")

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    def __str__(self):
        return self.name