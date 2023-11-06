from django.urls import path, include
from  . import views
from rest_framework import routers
from authentication.views import UserViewset, UserLogout
# Ici nous créons notre routeur
router = routers.SimpleRouter(trailing_slash=False)
# Puis lui déclarons une url basée sur le mot clé ‘category’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/article/’
router.register(r'users', UserViewset, basename='users'),


urlpatterns = [
    path('',  views.login_page, name='login'),
    path('home', views.home, name='home'),
    path('logout_user',  views.logout_user, name='logout_user'),
    path('api/login/', UserViewset.as_view({'post': 'login_user'}), name='user-login'),
    path('api/logout/', UserLogout.as_view(), name='user-logout'),
    path('api/', include((router.urls, 'app_name')))  # Il faut bien penser à ajouter les urls du router dans la liste des urls disponibles.

]


