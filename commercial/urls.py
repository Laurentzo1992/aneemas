from  django.urls import  path
from  . import views

urlpatterns = [
   path('', views.cours_or_by_api, name='cours_or'),
]