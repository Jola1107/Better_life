from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .forms import (LoginUserForm, ProfileForm, CategoryForm,
                    AnimalForm, MessageForm)

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model, authenticate, login, logout
User = get_user_model()
from .models import Profile, Animal, Message, Category
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.core.mail import send_mail



#start view
class StartView(View):
    template_name = 'start.html'
    form_class = ProfileForm

    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)


# new user registration
class AddProfileUserView(View):
    template_name = 'add_profile_user.html'
    form_class = ProfileForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            city = form.cleaned_data['city']
            post_code = form.cleaned_data['post_code']
            street = form.cleaned_data['street']
            phone = form.cleaned_data['phone']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username)
            if user:
                form.add_error('username', "Użytkownik o takim loginie już istnieje")
            else:
                user = User.objects.create_user(first_name=first_name, password=password, email=email,
                                                last_name=last_name, username=username)

                Profile.objects.create(user=user, city=city, post_code=post_code, street=street, phone=phone)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return render(request, 'start.html', context)


#login of a registered user
class LoginUserView(View):
    template_name = 'login_user.html'
    form_class = LoginUserForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                form.add_error('username', 'Użytkowniek nie istnieje')
            elif password is None:
                form.add_error('password', 'Nieprawodłowe hasło')
            else:
                login(request, user)
        return render(request, 'start.html', context)

# logout for a registered user
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('start')


# add animal

class AddAnimalView(LoginRequiredMixin, View):
    # permission_required = 'auth.add_animal'

    template_name = 'add_animal.html'
    form_class = AnimalForm
    login_url = '/login/'
    redirect_field_name = 'start'


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'form': form}

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            sex = form.cleaned_data['sex']
            age = form.cleaned_data['age']
            weight = form.cleaned_data['weight']
            breed = form.cleaned_data['breed']
            movie = form.cleaned_data['movie']
            is_adopted = form.cleaned_data['is_adopted']
            created = form.cleaned_data['created']
            closed_date = form.cleaned_data['closed_date']
            category = form.cleaned_data['category']
            cat = Category.objects.get(name=category)
            user = request.user
            if user.is_authenticated:
            # user = authenticate(username=username)
            # if user is None:
            #     form.add_error('username', 'Użytkowniek nie istnieje')
            # else:
                animal = Animal.objects.create(name=name, description=description,
                                               sex=sex, age=age, weight=weight,
                                               breed=breed, movie=movie,
                                               is_adopted=is_adopted, created=created,
                                               closed_date=closed_date, category=cat, user=user)
            # Category.objects.create(animal=animal, name=cat)
            context['animal'] = animal
            context['message'] = 'Dodano zwierzę do adopcji'

        return render(request, 'start.html', context)

# lista zwierząt do adopcji

class AnimalListView(ListView):
    model = Animal
    template_name = 'adoption.html'


# detail animal

class DetailAnimalView(View):
    def get(self, request, id):
        animal = Animal.objects.get(pk=id)
        category = Category.objects.get(pk=id)
        user = User.objects.get(pk=id)

        context = {
            'animal': animal,
            'category': category,
            'user': user,
        }
        return render(request, 'detail_animal.html', context)


# add category
class AddCategoryView(View):
    template_name = 'add_category.html'
    form_class = CategoryForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {form:'form'}
        if form.is_valid():
            name = form.cleaned_data['name']
            category = Category.objects.create(name=name)
            context['category'] = category
        return render(request, 'start.html', context)



# send message
class MessageView(CreateView):
    template_name = 'message.html'
    form_class = MessageForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        emailSend = False
        form = self.form_class(request.POST)

        if form.is_valid():
            subject = "Wiadomość została wysłana"
            text = form.cleaned_data['text']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            animal = form.cleaned_data['animal']

            send_mail(subject, message=text, from_email='nana83@interia.pl', recipient_list=[email], fail_silently=False)
            emailSend = True
        else:
            form = MessageForm()

        return render(request, 'start.html', {form: 'form', emailSend:'emailSend'})


