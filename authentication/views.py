from modules_externe.imports import *
from django.utils.translation import gettext as _


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    try:
        artisants = Cartartisants.objects.all().count()
        collecteurs = Demandeconventions.objects.filter(statut="convention").order_by('created').count()
        incidents = Formincidents.objects.filter(type_rapport="accident").count()
        # Récupérer les données venant du formulaire pour filtrer les dates
        if request.method == 'GET':
            date_depart = request.GET.get('date_depart')
            date_arrive = request.GET.get('date_arrive')
            type_rapport = request.GET.get('type_rapport')

        # Validation des dates (assurez-vous que vous avez des validations appropriées dans vos modèles)
        if date_depart and date_arrive:
            date_depart = Formincidents._meta.get_field('date_incident').to_python(date_depart)
            date_arrive = Formincidents._meta.get_field('date_incident').to_python(date_arrive)

        # Agréger les données par date
        resultats = Formincidents.objects.filter(date_incident__range=[date_depart, date_arrive], type_rapport=type_rapport)\
            .values('date_incident')\
            .annotate(total_hommes=Sum('vict_hom'))\
            .annotate(total_femmes=Sum('vict_fem'))\
            .annotate(total_enfants=Sum('vict_enf'))\
            .order_by('date_incident')

        # Créer des listes pour les données du graphique
        dates = [resultat['date_incident'] for resultat in resultats]
        total_hommes = [resultat['total_hommes'] for resultat in resultats]
        total_femmes = [resultat['total_femmes'] for resultat in resultats]
        total_enfants = [resultat['total_enfants'] for resultat in resultats]

        plt.switch_backend('AGG')
        plt.figure(figsize=(10, 4))

        # Créer les courbes d'évolution pour chaque série de données
        plt.plot(dates, total_hommes, marker='x', linestyle='dashed', color='#f7e80b', label='Hommes')
        plt.plot(dates, total_femmes, marker="3", linestyle='solid', color='#a44430', label='Femmes')
        plt.plot(dates, total_enfants, marker='$f$', linestyle='dashdot', color='#FFA500', label='Enfants')

        plt.xlabel("periode")
        plt.ylabel('Nombre total de victimes')
        plt.title('Évolution du nombre de victimes par cat de personne')
        plt.grid(True)
        # Ajouter une légende
        plt.legend()
        # Formatter l'axe x pour afficher les mois
        plt.gca().xaxis.set_major_locator(MonthLocator())
        plt.gca().xaxis.set_major_formatter(DateFormatter('%b'))
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        # Convertir l'image en base64 pour l'inclure dans le modèle
        chart = base64.b64encode(buffer.read()).decode('utf-8')

        context = {
            "date_arrive": date_arrive,
            "date_depart": date_depart,
            "artisants": artisants,
            "collecteurs": collecteurs,
            "incidents": incidents,
            "chart": chart,
        }

    except ValidationError as e:
        # Gérer l'erreur de validation des dates
        context = {
            "error_message": _('Erreur de validation des dates.'),
        }

    return render(request, 'authentication/home.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def bi(request):
    try:
        # Récupérer les données venant du formulaire pour filtrer les dates
        if request.method == 'POST':
            date_depart = request.POST.get('date_depart')
            date_arrive = request.POST.get('date_arrive')
        else:
            date_depart = request.GET.get('date_depart')
            date_arrive = request.GET.get('date_arrive')

        # Validation des dates (assurez-vous que vous avez des validations appropriées dans vos modèles)
        if date_depart and date_arrive:
            date_depart = Formincidents._meta.get_field('date_incident').to_python(date_depart)
            date_arrive = Formincidents._meta.get_field('date_incident').to_python(date_arrive)


        # Agréger les données par date
        resultats = Formincidents.objects.filter(date_incident__range=[date_depart, date_arrive], type_rapport='incident')\
            .values('date_incident')\
            .annotate(total_hommes=Sum('vict_hom'))\
            .annotate(total_femmes=Sum('vict_fem'))\
            .annotate(total_enfants=Sum('vict_enf'))\
            .order_by('date_incident')

        # Créer des listes pour les données du graphique
        dates = [resultat['date_incident'] for resultat in resultats]
        total_hommes = [resultat['total_hommes'] for resultat in resultats]
        total_femmes = [resultat['total_femmes'] for resultat in resultats]
        total_enfants = [resultat['total_enfants'] for resultat in resultats]

        plt.switch_backend('AGG')
        plt.figure(figsize=(10, 4))

        # Créer les courbes d'évolution pour chaque série de données
        plt.plot(dates, total_hommes, marker='o', linestyle='-', color='b', label='Hommes')
        plt.plot(dates, total_femmes, marker='o', linestyle='-', color='r', label='Femmes')
        plt.plot(dates, total_enfants, marker='o', linestyle='-', color='#FFA500', label='Enfants')

        plt.xlabel("Date d'incident")
        plt.ylabel('Nombre total de victimes')
        plt.title('Évolution du nombre total de victimes au fil du temps')

        # Ajouter une légende
        plt.legend('EFH')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Convertir l'image en base64 pour l'inclure dans le modèle
        chart = base64.b64encode(buffer.read()).decode('utf-8')

        context = {
            "date_arrive": date_arrive,
            "date_depart": date_depart,
            "chart": chart
        }

    except ValidationError as e:
        # Gérer l'erreur de validation des dates
        context = {
            "error_message": _('Erreur de validation des dates.'),
        }

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
        
        