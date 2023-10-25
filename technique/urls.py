from  django.urls import  path
from  . import views

urlpatterns = [
    #Url de la fiche d'enrolment
    path('enrolement', views.index, name='list_enrolement'),
    path('enrolement/api_data', views.api_enrolement, name='api_enrolement'),
    path('syn_detail/<int:id>', views.syn_detail, name='syn_detail'),
    path('syn/<int:id>', views.save_api_data_to_database, name='syn'),
    path('enrolement/add', views.add, name='add_enrolement'),
    path('enrolement/edit/<int:id>', views.edit, name='edit_enrolement'),
    path('enrolement/delete/<int:id>', views.delete, name='delete_enrolement'),
    path('carte', views.carte, name="carte"),
    
    #Url de la fiche de viste et guide autorite et rapport d'activité
    path('guide_autorite', views.index1, name='guide_fiche'),
    path('guide_autorite/add', views.add_guide, name='add_guide'),
    path('guide_autorite/edit/<int:id>', views.edit_guide, name='edit_guide'),
    path('guide_autorite/delete/<int:id>', views.delete_guide, name='delete_guide'),
    
    
    
    #Url de la fiche de viste et guide autorite et rapport d'activité
    path('visite', views.index2, name='visite_fiche'),
    path('visite/add', views.add_visite, name='add_visite'),
    path('visite/edit/<int:id>', views.edit_visite, name='edit_visite'),
    path('visite/delete/<int:id>', views.delete_visite, name='delete_visite'),
    
    
    
    #Url de la fiche de demande de convention
    path('convention', views.index3, name='convention'),
    path('convention/add', views.add_convention, name='add_convention'),
    path('convention/edit/<int:id>', views.edit_convention, name='edit_convention'),
    path('convention/delete/<int:id>', views.delete_convention, name='delete_convention'),
    
    
]
