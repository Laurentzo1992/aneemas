from  django.urls import  path
from  . import views

urlpatterns = [
   #Url de la fiche de prelevement
    path('prelevement', views.index, name='prelevement'),
    path('prelevement/api_prelevement', views.api_prelevement, name='api_prelevement'),
    path('prelevement/syn_detail', views.syn_detail, name='syn_detail'),
    path('prelevement/save_api_data_to_database', views.save_api_data_to_database, name='save_api_data_to_database'),
    path('prelevement/add', views.add, name='add'),
    path('prelevement/edit/<int:id>', views.edit, name='edit'),
    path('prelevement/delete/<int:id>', views.delete, name='delete'),
    
]
