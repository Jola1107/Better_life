from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .forms import (LoginUserForm, ProfileForm, CategoryForm,
                    AnimalForm, MessageForm, ImageForm)

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model, authenticate, login, logout
User = get_user_model()
from .models import Profile, Animal, Message, Category, Image
from django.views.generic import FormView, CreateView, DeleteView, UpdateView, ListView
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# from django.conf import settings
# from mailchimp_marketing import Client
# from mailchimp_marketing.api_client import ApiClientError


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
            repeat_password = form.cleaned_data["repeat_password"]
            user = User.objects.filter(username=username)
            if user:
                form.add_error('username', "Użytkownik o takim loginie już istnieje")
                return render(request, self.template_name, {'form': form})
            elif password != repeat_password:
                form.add_error('password', "Hasła nie są takie same")
                return render(request, self.template_name, {'form': form})
            else:
                user = User.objects.create_user(password=password, email=email, username=username)

                Profile.objects.create(user=user, first_name=first_name,
                                       last_name=last_name, city=city,
                                       post_code=post_code, street=street,
                                       phone=phone)
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
                form.add_error('username', 'Popraw login lub hasło')
                return render(request, self.template_name, {'form': form})
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
        files = request.FILES.getlist('image')
        imageform = ImageForm()
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
                for i in files:
                    Image.objects.create(animal=animal, path=i)
                messages.success(request, "Dodano zwierzę do adopcji")
                context['animal'] = animal
            # context['message'] = 'Dodano zwierzę do adopcji'
            #     return redirect(request, 'adoption.html')
            else:
                print(form.errors)

        else:
            form = AnimalForm()
            imageform = ImageForm()
        return render(request, 'start.html', {'form': form, 'imageform': imageform})

# lista zwierząt do adopcji

class AnimalListView(ListView):
    model = Animal
    template_name = 'adoption.html'

# class AnimalListView(View):
#     def get(self, request):
#         animals = Animal.objects.all()
#         for animal in animals:
#             img = [image.path for image in animal.image_set.all()]
#             # animal.image = img.path in img
#             # image = Image.objects.get(animal=animal)
#             # if image.path:
#             context = {
#                 'animal': animal,
#                 'image': img,
#             }
#         return render(request, 'adoption.html', context)

# detail animal

class DetailAnimalView(View):
    def get(self, request, id):
        animal = Animal.objects.get(pk=id)

            # image = Image.objects.filter(animal=animal)
        context = {'animal': animal }
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
# class MessageView(FormView):
#     template_name = 'message.html'
#     form_class = MessageForm
#     success_url = '/'
#     def form_valid(self, form):
#         subject = 'Zapytanie o zwierzę do adopcji'
#         body = {
#             'text': form.cleaned_data['text'],
#             'email': form.cleaned_data['email'],
#             'phone': form.cleaned_data['phone'],
#             'animal': form.cleaned_data['animal']
#         }
#         message = body
#
#         try:
#             send_mail(subject, message, 'nana83@interia.pl', ['nana83@interia.pl'])
#         except BadHeaderError:
#             return HttpResponse('Invalid header found')
#
#         return redirect('start.html')

class MessageView(View):
    # template_name = 'message.html'
    # form_class = MessageForm
    def get(self, request, id):
        form = MessageForm()
        animal = Animal.objects.get(pk=id)
        owner = animal.user
        owner_email = owner.email
        # form = self.form_class()
        context = {'form': form}
        return render(request, 'message.html', context)

    def post(self, request, id):
            animal = Animal.objects.get(pk=id)
            owner = animal.user
            owner_email = owner.email
            form = MessageForm(request.POST)

            if form.is_valid():
                # cnx = {}
                text = form.cleaned_data['text']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                subject = 'Wiadomość adopcyjna'
                from_email = email
                to_email = [owner_email]
                text_content = """
                {}
                {}
                {}
                """.format(text, phone, email)

                html_c = get_template('message.html')
                d = {'text': text,
                     'email': email,
                     'phone': phone, }
                html_content = html_c.render(d)

                msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                msg.attach_alternative(html_content, 'detail_animal.html')
                msg.send()
            return render(request, 'detail_animal.html')

class ImageView(View):
    template_name = 'image.html'
    form_class = ImageForm

    def get(self, request, *args, id):
        animal = Animal.objects.get(pk=id)
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, id):
        animal = Animal.objects.get(pk=id)
        form = self.form_class(request.POST, request.FILES)
        context = {form:'form'}
        if form.is_valid():
            title = form.cleaned_data['title']
            path = form.cleaned_data['path']
            # animal = form.cleaned_data['animal']
            user = request.user
            if user.is_authenticated:
                image = Image.objects.create(title=title, path=path, animal=animal)
                # img = image.animal
                context = {'title': title, 'path': path, 'image': image}
        return render(request, 'start.html', context)



# class ImageView(CreateView):
#     model = Image
#     fields = ['title', 'path', 'animal']
#     template_name = 'image.html'
#     success_url = '/detail_animal'

# @ login_required


# def image_create(request):
#     if request.method == 'POST':
#         form = ImageForm(data=request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             new_item = form.save(commit=False)
#             new_item.user = request.user
#             new_item.save()
#             messages.success(request, 'Obraz został dodany')
#             return redirect(new_item.get_absolute_url())
#         else:
#             form = ImageForm(data=request.GET)
#
#         return render(request, 'detail_animal.html', {'section': 'images', 'form': form})

# subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
# text_content = 'This is an important message.'
# html_content = '<p>This is an <strong>important</strong> message.</p>'
# msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
# msg.attach_alternative(html_content, "text/html")
#

# # Mailchimp Settings
# api_key = settings.MAILCHIMP_API_KEY
# server = settings.MAILCHIMP_DATA_CENTER
# list_id = settings.MAILCHIMP_EMAIL_LIST_ID
#
# # Subscription Logic
# def subscribe(email, text, phone):
#     """
#      Contains code handling the communication to the mailchimp api
#      to create a contact/member in an audience/list.
#     """
#
#     mailchimp = Client()
#     mailchimp.set_config({
#         "api_key": api_key,
#         "server": server,
#     })
#
#     member_info = {
#         "email_address": email,
#         'text': text,
#         'phone': phone,
#         "status": "subscribed",
#     }
#
#     try:
#         response = mailchimp.lists.add_list_member(list_id, member_info)
#         print("response: {}".format(response))
#     except ApiClientError as error:
#         print("An exception occurred: {}".format(error.text))
#
#
# class MessageView(View):
#     # template_name = 'message.html'
#     # form_class = MessageForm
#     def get(self, request, id):
#         form = MessageForm()
#         animal = Animal.objects.get(pk=id)
#         owner = animal.user
#         owner_email = owner.email
#         # form = self.form_class()
#         context = {'form': form}
#         return render(request, 'message.html', context)
#
#     def post(self, request, id):
#         animal = Animal.objects.get(pk=id)
#         owner = animal.user
#         owner_email = owner.email
#         form = MessageForm(request.POST)
#
#         if form.is_valid():
#
#             text = form.cleaned_data['text']
#             email = form.cleaned_data['email']
#             phone = form.cleaned_data['phone']
#             subscribe(email, text, phone)
#             messages.success(request, 'Email wysłany. Dziękujemy!')
#
#         return render(request, 'detail_animal.html')