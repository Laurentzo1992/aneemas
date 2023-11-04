from  django.urls import  path
from  .views import *
from django.urls import path, include
from .adminsite import commercial_admin

urlpatterns = [
   path('home', cours_or_by_api, name='home'),
   path(r'jet/', include('jet.urls', 'jet')),  # Django JET URLS
   path(r'jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')), # Django JET dashboard URLS
   path(r'gesco/', commercial_admin.urls),
   path('commercial/lingot/<pk>/add/', add_lingot, name='create-lingot'),
   path('commercial/lingot/<pk>/details/', detail_lingot, name="detail-lingot"),
   path('commercial/lingot/<pk>/update/', update_lingot, name="update-lingot"),
   path('commercial/lingot/<pk>/delete/', delete_lingot, name="delete-lingot"),
   path('commercial/create-lingot-form/', add_lingot_form, name='add-lingot-form'),

   path('commercial/fiche-control/<pk>/generate/', generate_fiche_control, name='generate-fiche-control'),
]