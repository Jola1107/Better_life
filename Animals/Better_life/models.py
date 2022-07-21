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

    def __str__(self):
        return 'Profil użytkownika {}.'.format(self.user.username)



SEX = (
    (1, 'Żeńska'),
    (2, 'Męska'),
    (3, 'Nieznana')
)


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Animal(models.Model):
    name = models.CharField(max_length=64, blank=True)
    description = models.TextField()
    sex = models.IntegerField(choices=SEX)
    age = models.SmallIntegerField(null=True)
    weight = models.SmallIntegerField(null=True)
    breed = models.CharField(max_length=128, null=True)
    movie = models.URLField()
    is_adopted = models.BooleanField()
    created = models.DateField(auto_now_add=True)
    closed_date = models.DateField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Image(models.Model):
    title = models.CharField(max_length=24)
    path = models.ImageField(null=True, blank=True, upload_to='image/')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Message(models.Model):
    text = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)

    def __str__(self):
        return self.animal




