from django.urls import path, include
from  . import views
from rest_framework import routers
# Ici nous créons notre routeur
router = routers.SimpleRouter(trailing_slash=False)

#router.register(r'users', UserViewset, basename='users'),

app_name = "bunsess"

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("charts/", views.charts, name="charts"),
    path("rapportMort/", views.rapportMort, name="rapportMort"),
    path("boadConvention/", views.boadConvention, name="boadConvention"),
    path("guideAutorite/", views.guideAutorite, name="guideAutorite"),
    path("messages/", views.send_messages, name="messages"),
    path("messages_archives/", views.messages_archives, name="messages_archives"),
    path('api/', include((router.urls, 'app_name_bi')))
]


