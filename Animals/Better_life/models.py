from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    post_code = models.CharField(max_length=10)
    street = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    email = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.CASCADE)



SEX = (
    (1, 'Female'),
    (2, 'Male'),
    (3, 'Undefined')
)


class Category(models.Model):
    name = models.CharField(max_length=64)


class Animal(models.Model):
    name = models.CharField(max_length=64, blank=True)
    description = models.TextField()
    sex = models.IntegerField(choices=SEX)
    movie = models.URLField()
    is_adopted = models.BooleanField()
    created = models.DateTimeField()
    closed = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Image(models.Model):
    title = models.CharField(max_length=24)
    path = models.ImageField()
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)

class Message(models.Model):
    text = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)




