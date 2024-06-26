from django.urls import path, include
from rest_framework import routers
from  . import views
from technique.views import *


router = routers.SimpleRouter()
router.register('sites', ComsitesViewset, basename='sites')
router.register('statut', StatutsitesViewset, basename='statut')
router.register('types', TypesitesViewset, basename='types')
router.register('regions', RegionsViewset, basename='regions')

urlpatterns = [
    # gestion site
    path('site', views.site, name='site'),
    path('webmapp', views.webmapp, name='webmapp'),
    path('api/', include(router.urls)),
    path('site/add', views.add_site, name='add_site'),
    path('site/edit/<int:id>', views.edit_site, name='edit_site'),
    path('site/delete/<int:id>', views.delete_site, name='delete_site'),
    
    
    #Url de la fiche d'enrolment
    path('enrolement', views.index, name='list_enrolement'),
    path('enrolement/api_data', views.get_api_enrolement, name='api_enrolement'),
    path('syn_detail/<int:identifiant>', views.syn_detail, name='syn_detail'),
    path('syn/<int:identifiant>', views.save_api_data_to_database, name='syn'),
    path('enrolement/add', views.add, name='add_enrolement'),
    path('enrolement/edit/<int:id>', views.edit, name='edit_enrolement'),
    path('enrolement/delete/<int:id>', views.delete, name='delete_enrolement'),
    path('carte', views.carte, name="carte"),
    
    # Url de la fiche de guide autorite
    path('guide_autorite/api_data', views.get_api_guide, name='api_guide'),
    path('guide_autorite/syn_detail/<int:identifiant>', views.syn_detail_guide, name='syn_detail_guide'),
    path('guide_autorite/syn/<int:identifiant>', views.save_api_data_to_database_guide, name='save_api_data_to_database_guide'),
    path('guide_autorite', views.index1, name='guide_fiche'),
    path('guide_autorite/add', views.add_guide, name='add_guide'),
    path('guide_autorite/edit/<int:id>', views.edit_guide, name='edit_guide'),
    path('guide_autorite/delete/<int:id>', views.delete_guide, name='delete_guide'),
    
    
    
    #Url de la fiche de viste
    # path('visite', views.index2, name='visite_fiche'),
    # path('visite/add', views.add_visite, name='add_visite'),
    # path('visite/edit/<int:id>', views.edit_visite, name='edit_visite'),
    # path('visite/delete/<int:id>', views.delete_visite, name='delete_visite'),
    
    
    
    #Url de la fiche de demande de convention
    path('convention/api_data', views.api_enrolement_conv, name='api_enrolement_conv'),
    path('convention/syn_detail/<int:identifiant>', views.syn_detail_conv, name='syn_detail_conv'),
    path('convention/syn/<int:identifiant>', views.save_api_data_to_database_conv, name='syn1'),
   
    path('convention', views.index3, name='convention'),
    path('instruire/<int:id>', views.instruire, name='instruire'),
    path('instruire_anull/<int:id>', views.instruire_anull, name='instruire_anull'),
    path('signature_anull/<int:id>', views.signature_anull, name='signature_anull'),
    path('signature_anull1/<int:id>', views.signature_anull1, name='signature_anull1'),
    path('signature/<int:id>', views.signature, name='signature'),
    path('signe/<int:id>', views.signe, name='signe'),
    path('convention/add', views.add_convention, name='add_convention'),
    path('convention/edit/<int:id>', views.edit_convention, name='edit_convention'),
    path('convention/edit1/<int:id>', views.edit_convention1, name='edit_convention1'),
    path('convention/edit2/<int:id>', views.edit_convention2, name='edit_convention2'),
    path('convention/delete/<int:id>', views.delete_convention, name='delete_convention'),
    
    
    
    #Url de la fiche de rapport d'accident et incident
    path('incident/api_data', views.get_api_accident, name='api_accident'),
    path('incident/syn_detail/<int:identifiant>', views.syn_detail_acc, name='syn_detail_acc'),
    path('incident/syn/<int:identifiant>', views.save_api_data_to_database_acc, name='syn2'),
    path('incident', views.index4, name='incident'),
    path('incident/add', views.add_incident, name='add_incident'),
    path('incident/edit/<int:id>', views.edit_incident, name='edit_incident'),
    path('incident/delete/<int:id>', views.delete_incident, name='delete_incident'),
    
    
    #Url de la fiche de rapport d'activité
    path('rapport/api_data', views.get_api_rapport, name='api_rapport'),
    path('rapport/syn_detail/<int:identifiant>', views.syn_detail_rapp, name='syn_detail_rapp'),
    path('rapport/syn/<int:identifiant>', views.save_api_data_to_database_rapp, name='syn3'),
    path('rapport', views.index5, name='rapport'),
    path('rapport/add', views.add_rapport, name='add_rapport'),
    path('rapport/edit/<int:id>', views.edit_rapport, name='edit_rapport'),
    path('rapport/delete/<int:id>', views.delete_rapport, name='delete_rapport'),

    
]
