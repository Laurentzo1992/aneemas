from  django.urls import  path
from  . import views

urlpatterns = [
   #Url de la fiche de prelevement
    path('prelevement', views.index, name='prelevement'),
    path('prelevement/api_prelevement', views.api_prelevement, name='api_prelevement'),
    path('prelevement/syn_detail/<int:identifiant>', views.syn_prelevement, name='syn_prelevement'),
    path('prelevement/save_api_data_to_database/<int:identifiant>', views.save_api_data_to_database_prelevement, name='syn_prelevement'),
    path('prelevement/add', views.add_prelevement, name='add_prelevement'),
    path('prelevement/edit/<int:id>', views.edit_prelevement, name='edit_prelevement'),
    path('prelevement/delete/<int:id>', views.delete_prelevement, name='delete_prelevement'),
    
    
    
    # url de la fiche exploiation artisanale
    
    path('exploitation', views.exploitation, name='exploitation'),
    path('exploitation/api_exploitation', views.api_exploitation, name='api_exploitation'),
    path('exploitation/syn_detail/<int:identifiant>', views.syn_detail_exploitation, name='syn_detail_exploitation'),
    path('exploitation/save_api_data_to_database/<int:identifiant>', views.save_api_data_to_database_exploitation, name='save_api_data_to_database_exploitation'),
    path('exploitation/add', views.add_exploitation, name='add_exploitation'),
    path('exploitation/edit/<int:id>', views.edit_exploitation, name='edit_exploitation'),
    path('exploitation/delete/<int:id>', views.delete_exploitation, name='delete_exploitation'),
    
]
