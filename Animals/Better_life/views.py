from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .forms import LoginUserForm, ProfileForm
from django.contrib.auth import get_user_model, authenticate, login, logout
User = get_user_model()



#start view
class StartView(View):
    template_name = 'start.html'
    # form_class = LoginUserForm
    form_class = ProfileForm

    def get(self, request):
        # form1 = self.form_class()
        form = self.form_class()
        # context1 = {'form1': form1}
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
                form.add_error('login-user', "Login istnieje")
            else:
                user = User.objects.create_user(first_name=first_name, password=password, email=email,
                                                last_name=last_name, city=city, post_code=post_code,
                                                street=street, phone=phone, username=username)
                login(request, user)

        return render(request, self.template_name, context)


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
            else:
                login(request, user)
        return render(request, self.template_name, context)

# logout for a registered user
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login-user')


