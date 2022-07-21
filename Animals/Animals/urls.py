"""Animals URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Better_life import views as ex_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # path('', include('main.urls')),
    path('', ex_views.StartView.as_view(), name='start'),
    path('login/', ex_views.LoginUserView.as_view(), name='login-user'),
    path('logout/', ex_views.LogoutView.as_view(), name='logout'),
    path('register/', ex_views.AddProfileUserView.as_view(), name='register'),
    path('add_animal/', ex_views.AddAnimalView.as_view(), name='add-animal'),
    path('message/<int:id>/', ex_views.MessageView.as_view(), name='message'),
    path('add_category/', ex_views.AddCategoryView.as_view(), name='add-category'),
    path('for_adoption/', ex_views.AnimalListView.as_view(), name='adoption'),
    path('detail_animal/<int:id>/', ex_views.DetailAnimalView.as_view(), name='detail-animal'),
    path('image/<int:id>/', ex_views.ImageView.as_view(), name='image'),
    # path('image/', image_create, name='image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
