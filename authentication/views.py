from django.shortcuts import redirect, render
from authentication.models import UserManager, User
from authentication.serializers import UserRegistrationSerializer, UserSerializer, UserLoginSerilizer
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import  login, logout, authenticate
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from paramettre.models import Demandeconventions, Formincidents, Cartartisants
from django.contrib.auth.decorators import login_required
from  django.views.decorators.cache import cache_control
from django.shortcuts import render
from django_pandas.io import read_frame
import matplotlib.pyplot as plt
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    artisants = Cartartisants.objects.all().count()
    collecteurs = Demandeconventions.objects.filter(statut="convention").order_by('created').count()
    incidents = Formincidents.objects.filter(type_rapport="incident").count()
    context = {"artisants":artisants, "collecteurs":collecteurs, "incidents":incidents}
    return render(request, 'authentication/home.html', context)


def bi(request):
    
    type_rapport = Formincidents.objects.all()
    date_depart = request.GET.get('date_depart')
    date_arrive = request.GET.get('date_arrive')

    etats2 = Formincidents.objects.filter(type_rapport='accident', date_incident__range=(date_depart, date_arrive)).annotate(month=TruncMonth('date_incident')).values('month').annotate(total_victimes=Sum(F('vict_hom') + F('vict_fem') + F('vict_enf'))).order_by('month')
   
    etats = Formincidents.objects.filter(type_rapport='incident', date_incident__range=(date_depart, date_arrive)).annotate(month=TruncMonth('date_incident')).values('month').annotate(total_victimes=Sum(F('vict_hom') + F('vict_fem') + F('vict_enf'))).order_by('month')
    labels = [entry['month'] for entry in etats]
    print(labels)
    labels2 = [entry['month'] for entry in etats2]
    data = [entry['total_victimes'] for entry in etats]
    data2 = [entry['total_victimes'] for entry in etats2]

    barres = len(etats)
    context = {"type_rapport": type_rapport, "date_depart": date_depart, "date_arrive": date_arrive, "barres": barres, "etats": etats,  "etats2": etats2, "labels": labels,"labels2": labels2, "data": data, "data2": data2}

    # on reinitialise le filtre
    if 'reset' in request.GET:
        return redirect('bi')
    return render(request, 'authentication/bi/bi.html', context)



def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(
                request=request,
                username=username,
                password=password,
            )
            if user is not None:
                login(request, user)
                messages.success(request, 'connexion reussi!')
                return HttpResponseRedirect(reverse('home'))  # Redirection vers la page d'accueil
            else:
                messages.error(request, 'Identifiants invalides')
    return render(request, 'authentication/login.html')



def logout_user(request):
    logout(request)
    messages.warning(request, 'Deconnexion!')
    return redirect('login')
    



class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    
    def get_queryset(self):
        return User.objects.all()

    # Vue de connexion personnalisée
    def login_user(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        # Vérifiez les informations de connexion
        user = authenticate(request, email=email, password=password)
        
        if user:
            login(request, user)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': 'Connexion refusée veuillez verifer vos identifiants'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
class UserLogout(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Déconnexion de l'utilisateur
        logout(request)
        return Response({"message": "Déconnexion réussie."}, status=status.HTTP_200_OK)
    
         

""" class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegistrationSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST) """
        
        