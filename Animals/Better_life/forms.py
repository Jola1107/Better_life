from django import forms
from .models import User, Profile, Animal, Category, Image, Message
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')


class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=64)
    email = forms.CharField(widget=forms.EmailInput)
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



class AnimalForm(forms.ModelForm):

    class Meta:
        model = Animal
        fields = ('name', 'description', 'sex', 'movie',
                  'is_adopted', 'created', 'closed')


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('title', 'path')


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('text', 'email', 'phone')


class LoginUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# register user
# class AddProfileUserForm(forms.Form):
#     first_name = forms.CharField(max_length=64)
#     last_name = forms.CharField(max_length=64)
#     city = forms.CharField(max_length=64)
#     post_code = forms.CharField(max_length=10)
#     street = forms.CharField(max_length=64)
#     phone = forms.CharField(max_length=16)
#     email = forms.CharField(max_length=64)
#     username = forms.CharField(max_length=64)
#     password = forms.CharField(widget=forms.PasswordInput)