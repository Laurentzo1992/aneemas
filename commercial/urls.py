from  django.urls import  path
from  . import views

urlpatterns = [
   path('home', views.cours_or_by_api, name='home'),
]