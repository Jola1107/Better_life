from django import forms
from .models import User, Profile, Animal, Category, Image, Message
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator
from datetime import datetime, date

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')


class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=64)
    email = forms.CharField(widget=forms.EmailInput, validators=[EmailValidator()])
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")
        if password != repeat_password:
             raise ValidationError("Hasła nie są takie same")

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'city',
                  'post_code', 'street', 'phone', 'email')

SEX = (
    (1, 'Żeńska'),
    (2, 'Męska'),
    (3, 'Nieznana')
)

class AnimalForm(forms.Form):
    name = forms.CharField(label='imię:', max_length=64)
    description = forms.CharField(label='opis:', widget=forms.Textarea)
    sex = forms.ChoiceField(choices=SEX)
    age = forms.IntegerField(label='wiek:')
    weight = forms.IntegerField(label='waga:')
    breed = forms.CharField(label='rasa/w typie rasy:')
    movie = forms.CharField(validators=[URLValidator()], required=False, label='link do filmiku:')
    is_adopted = forms.BooleanField(label='czy adoptowany?', required=False)
    closed_date = forms.DateField(required=False, label='data adopcji:')
    created = forms.DateField(label='data dodania ogłoszenia:', initial=date.today)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='kategoria:')



class CategoryForm(forms.Form):
    name = forms.CharField(label='nazwa kategorii:')



class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['title', 'path']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'email', 'phone']


class LoginUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

