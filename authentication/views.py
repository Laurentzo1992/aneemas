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
from paramettre.models import Demandeconventions




def home(request):
    convs = Demandeconventions.objects.filter(statut="demande").order_by('created').count()
    conv_sigs = Demandeconventions.objects.filter(statut="convention").order_by('created').count()
    conv_anuls = Demandeconventions.objects.filter(statut="anuler").order_by('created').count()
    conventions = Demandeconventions.objects.filter(statut="convention").order_by('created')[:5]
    context = {"conventions":conventions, "convs":convs, "conv_sigs":conv_sigs, "conv_anuls":conv_anuls}
    return render(request, 'authentication/home.html', context)



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
        
        