from  django.urls import  path
from  . import views

urlpatterns = [
    path('enrolement', views.index, name='list_enrolement'),
    path('enrolement/add', views.add, name='add_enrolement'),
    path('enrolement/edit/<int:id>', views.edit, name='edit_enrolement'),
    path('enrolement/delete/<int:id>', views.delete, name='delete_client'),
    path('envoyer_message', views.envoyer_message, name='message'),
    
]
