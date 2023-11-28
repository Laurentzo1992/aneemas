from modules_externe.imports import *
from django.utils.translation import gettext as _
from modules_externe.module_sms import envoyer_message 



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    try:
        artisants = Cartartisants.objects.all().count()
        collecteurs = Demandeconventions.objects.filter(statut="convention").order_by('created').count()
        exploitants = Demandeconventions.objects.filter(statut="convention").order_by('created').count()
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
        chart_type = request.GET.get('chart_type')
        
        if chart_type == 'line':
            # Créer les courbes d'évolution pour chaque série de données
            plt.plot(dates, total_hommes, marker='x', linestyle='dashed', color='#f7e80b', label='Hommes')
            plt.plot(dates, total_femmes, marker="3", linestyle='solid', color='#a44430', label='Femmes')
            plt.plot(dates, total_enfants, marker='$f$', linestyle='dashdot', color='#FFA500', label='Enfants')

        elif chart_type == 'histogram':
            plt.bar(dates, total_hommes, color='#f7e80b', label='Hommes')
            plt.bar(dates, total_femmes, color='#a44430', label='Femmes')
            plt.bar(dates, total_enfants, color='#FFA500', label='Enfants')
            
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
            "exploitants":exploitants,
            "incidents": incidents,
            "chart": chart,
        }

    except ValidationError as e:
        # Gérer l'erreur de validation des dates
        context = {
            "error_message": _('Erreur de validation des dates.'),
        }

    return render(request, 'bunsess/index.html', context)




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def charts(request):
    if request.method == 'GET':
        date_depart = request.GET.get('date_depart')
        date_arrive = request.GET.get('date_arrive')
        statut = request.GET.get('statut')

        # Validation des dates (assurez-vous que vous avez des validations appropriées dans vos modèles)
        if date_depart and date_arrive:
            date_depart = Demandeconventions._meta.get_field('date_depot').to_python(date_depart)
            date_arrive = Demandeconventions._meta.get_field('date_depot').to_python(date_arrive)

            # Agréger les données par région
            resultats = Demandeconventions.objects.filter(date_depot__range=[date_depart, date_arrive], statut=statut)

            # Calculer le nombre de demandes par région
            demandes_par_region = resultats.values('region__nomreg').annotate(nombre_demandes=Count('id'))

            # Convertir les données en JSON
            chart_data = {
                'regions': [entry['region__nomreg'] for entry in demandes_par_region],
                'nombre_demandes': [entry['nombre_demandes'] for entry in demandes_par_region],
            }
            # Renvoyer les données JSON en réponse à la requête AJAX
            return JsonResponse(chart_data)

        else:
            # Gérer l'erreur de validation des dates
            context = {
                "error_message": _('Erreur de validation des dates.'),
            }
            return render(request, 'bunsess/charts.html', context)
    return render(request, 'bunsess/charts.html', context)




def rapportMort(request):
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        type_rapport = request.GET.get('type_rapport')

        # Validation des dates
        try:
            if start_date and end_date:
                start_date = Formincidents._meta.get_field('date_incident').to_python(start_date)
                end_date = Formincidents._meta.get_field('date_incident').to_python(end_date)
        except ValidationError as e:
            return JsonResponse({'error': str(e)})

        # Agréger les données par date
        resultats = Formincidents.objects.filter(date_incident__range=[start_date, end_date], type_rapport=type_rapport)\
            .values('date_incident')\
            .annotate(total_hommes=Sum('mort_hom'))\
            .annotate(total_femmes=Sum('mort_fem'))\
            .annotate(total_enfants=Sum('mort_enf'))\
            .order_by('date_incident')

        # Créer des listes pour les données du graphique
        dates = [resultat['date_incident'] for resultat in resultats]
        total_hommes = [resultat['total_hommes'] for resultat in resultats]
        total_femmes = [resultat['total_femmes'] for resultat in resultats]
        total_enfants = [resultat['total_enfants'] for resultat in resultats]

        # Créer un dictionnaire de données
        data = {
            'dates': dates,
            'total_hommes': total_hommes,
            'total_femmes': total_femmes,
            'total_enfants': total_enfants,
        }

        # Renvoyer la réponse JSON
        return JsonResponse(data)



  
  

































































@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def send_messages(request):
    if request.method == 'POST':
        numbers = request.POST.get('numbers')
        datas = request.POST.get('datas')

        #Convertissez les numéros en une liste
        dest = [num.strip() for num in numbers.split('\n') if num.strip()]

        
        # Assurez-vous que l'utilisateur est authentifié avant d'enregistrer le message
        if request.user.is_authenticated:
            envoyeur = request.user
        else:
            envoyeur = None

        # Appelez la fonction pour envoyer les messages
        result = envoyer_message(datas, *dest)

        # Enregistrez les données dans le modèle
        if result:
            message = Message.objects.create(
                phone_numbers=dest,
                message=datas,
                envoyeur = envoyeur
            )
            message.save()

            messages.success(request, 'Message envoyé avec succès')
            return redirect('bunsess:messages_archives')
            #return JsonResponse({'success': True, 'message': 'Message envoyé avec succès'})
        else:
            messages.error(request, 'Échec de l\'envoi du message')
            return redirect('bunsess:messages')
            #return JsonResponse({'success': False, 'message': 'Échec de l\'envoi du message'})

    return render(request, 'bunsess/form_basic.html')



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def messages_archives(request):
    saved_messages = Message.objects.all()
    return render(request, 'bunsess/tables.html', {'saved_messages': saved_messages})










 




         

        