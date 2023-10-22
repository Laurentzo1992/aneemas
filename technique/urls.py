from  django.urls import  path
from  . import views

urlpatterns = [
    path('donnees', views.donnees, name='donnees'),
    path('envoyer_message', views.envoyer_message, name='message'),
    
]
