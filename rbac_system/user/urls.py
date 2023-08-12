from django.contrib import admin
from django.urls import path, include
from . import views
from .views import UserLogin
from django.views.generic import TemplateView


urlpatterns = [
    # path("user/", UserLoginView.as_view(), name="user-post")
    path('', views.home, name='home'),
    path('login/', UserLogin, name='login'),
    path('add_user/', views.add_user, name='add_user'),
    path('add_api/', views.add_api, name='add_api'),
    path('remove_user/', views.remove_user, name='remove_user'),
    path('update_user/', views.update_user, name='update_user'),
    path('remove_api/', views.remove_api, name='remove_api'),
    path('update_api/', views.update_api, name='update_api'),
    path('view_api/', views.view_api, name='view_api'),
]
