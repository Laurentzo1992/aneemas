from modules_externe.imports import *
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserChangeForm


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
                return HttpResponseRedirect(reverse('bunsess:dashboard'))  # Redirection vers la page d'accueil
            else:
                messages.error(request, 'Identifiants invalides')
    return render(request, 'authentication/login.html')



def logout_user(request):
    logout(request)
    messages.warning(request, 'Deconnexion!')
    return redirect('login')
    


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name']



def userProfile(request):
    user_id = request.user.id
    profile = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        # Si le formulaire est soumis, instancier le formulaire avec les données du formulaire
        form = CustomUserChangeForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        # Si c'est une requête GET, pré-remplissez le formulaire avec les données actuelles du profil
        form = CustomUserChangeForm(instance=profile)
    context={"profile":profile,  'form': form,}
    return render(request, 'authentication/profile.html', context)




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
        
        