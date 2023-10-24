from  django.urls import  path
from  . import views

urlpatterns = [
    path('enrolement', views.index, name='list_enrolement'),
    path('enrolement/api_data', views.api_enrolement, name='api_enrolement'),
    path('syn_detail/<int:id>', views.syn_detail, name='syn_detail'),
    path('syn/<int:id>', views.save_api_data_to_database, name='syn'),
    path('enrolement/add', views.add, name='add_enrolement'),
    path('enrolement/edit/<int:id>', views.edit, name='edit_enrolement'),
    path('enrolement/delete/<int:id>', views.delete, name='delete_client'),
    path('carte', views.carte, name="carte"),
    path('envoyer_message', views.envoyer_message, name='message'),
    
]
