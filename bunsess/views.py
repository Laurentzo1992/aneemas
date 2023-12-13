from modules_externe.imports import *
from django.utils.translation import gettext as _
from modules_externe.module_sms import envoyer_message 
from django.contrib.sessions.models import Session
from django.utils import timezone


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    try:
        collecteur_id = 5
        exploitant_id = 1
        artisants = Cartartisants.objects.all().count()
        #collecteurs = Demandeconventions.objects.filter(statut="convention").order_by('created').count()
        #exploitants = Demandeconventions.objects.filter(statut="convention").order_by('created').count()
        collecteurs = Demandeconventions.objects.filter(statut="convention", lignetypeautorisation__autorisation_id=collecteur_id).count()
        exploitants = Demandeconventions.objects.filter(statut="convention", lignetypeautorisation__autorisation_id=exploitant_id).count()

        incidents = Formincidents.objects.filter(type_rapport="incident").count()
        accidents = Formincidents.objects.filter(type_rapport="accident").count()
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
            "accidents": accidents,
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
    Carte = Fichenrolements.objects.all().count()
    Visites = Fichevisites.objects.all().count()
    Prelevements = Ficheprelevements.objects.all().count()
    Bureaux = Burencadrements.objects.all().count()
    Guides = Formguidautorites.objects.all().count()
    rapportActivites = Rapactivites.objects.all().count()
    Sites = Comsites.objects.all().count()
    
    active_sessions = Session.objects.filter(expire_date__gt=timezone.now())
    # Obtenez les identifiants uniques des utilisateurs actifs
    active_users_ids = [session.get_decoded().get('_auth_user_id') for session in active_sessions]
    # Filtrez les identifiants nuls (utilisateurs non authentifiés)
    active_users_ids = list(filter(None, active_users_ids))
    # Obtenez le nombre d'utilisateurs uniques actifs
    active_users_count = len(set(active_users_ids))
    
    # recuperation des types
    
    types = Typesites.objects.all()
    
    if request.method == 'GET':
        date_depart = request.GET.get('date_depart')
        date_arrive = request.GET.get('date_arrive')
        status = request.GET.get('statut')

        # Validation des dates (assurez-vous que vous avez des validations appropriées dans vos modèles)
        if date_depart and date_arrive:
            date_depart = Demandeconventions._meta.get_field('date_depot').to_python(date_depart)
            date_arrive = Demandeconventions._meta.get_field('date_depot').to_python(date_arrive)

            # Agréger les données par région
            resultats = Demandeconventions.objects.filter(date_depot__range=[date_depart, date_arrive], statut=status)

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
                "Carte":Carte,
                "Visites":Visites,
                "Prelevements":Prelevements,
                "Bureaux":Bureaux,
                "Guides":Guides,
                "rapportActivites":rapportActivites,
                "Sites":Sites,
                "active_users_count":active_users_count,
                "types":types
            }
            return render(request, 'bunsess/charts.html', context)
    return render(request, 'bunsess/charts.html')




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
    
    
    


def boadConvention(request):
    if request.method == 'GET':
        dep = request.GET.get('dep')
        arr = request.GET.get('arr')
        
        try:
            if dep and arr:
                dep = Demandeconventions._meta.get_field('date_signature').to_python(dep)
                arr = Demandeconventions._meta.get_field('date_signature').to_python(arr)
        except ValidationError as e:
            return JsonResponse({'error': str(e)})
        
        conventions = Demandeconventions.objects.filter(statut='convention', date_signature__range=[dep, arr]).prefetch_related ('type_autorisation')

        # Préparer les données pour le graphique
        data = {}
        for convention in conventions:
            types_autorisation = convention.type_autorisation.all()
            
            for type_autorisation in types_autorisation:
                type_autorisation_id = type_autorisation.id
                type_autorisation_libelle = type_autorisation.libelle

                if type_autorisation_id not in data:
                    data[type_autorisation_id] = {
                        'libelle': type_autorisation_libelle,
                        'count': 0
                    }

                data[type_autorisation_id]['count'] += 1

        # Convertir les données en listes pour les utiliser dans le template
        labels = [item['libelle'] for item in data.values()]
        counts = [item['count'] for item in data.values()]

        # Retourner les données JSON
        response_data = {
            "labels": labels,
            "counts": counts,
        }

        return JsonResponse(response_data)
    
    
    
    
def guideAutorite(request):
    if request.method == 'GET':
        d1 = request.GET.get('d1')
        d2 = request.GET.get('d2')
        type_site = request.GET.get('type_site')

        try:
            if d1 and d2:
                d1 = Formguidautorites._meta.get_field('date_visite').to_python(d1)
                d2 = Formguidautorites._meta.get_field('date_visite').to_python(d2)
        except ValidationError as e:
            return JsonResponse({'error': str(e)})

        guides = Formguidautorites.objects.filter(com_site__id=type_site, date_visite__range=[d1, d2])

        # Regroupement par type de site et comptage
        site_counts = {}
        for guide in guides:
            libelle = guide.com_site.libelle
            site_counts[libelle] = site_counts.get(libelle, 0) + 1

        # Retourner les données JSON
        response_data = {
            "labels": list(site_counts.keys()),
            "counts": list(site_counts.values()),
        }

        return JsonResponse(response_data)








  
  

































































@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def send_messages(request):
    if request.method == 'POST':
        numbers = request.POST.get('numbers')
        datas = request.POST.get('datas')

        # Convertissez les numéros en une liste
        dest = set([num.strip() for num in numbers.split(';') if num.strip()])

        # Assurez-vous que l'utilisateur est authentifié avant d'enregistrer le message
        envoyeur = request.user if request.user.is_authenticated else None

        # Appelez la fonction pour envoyer les messages
        destinataires_reussis = envoyer_message(datas, *dest)

        # Enregistrez les données dans le modèle pour les destinataires réussis
        for destinataire in destinataires_reussis:
            message = Message.objects.create(
                phone_numbers=destinataire,
                message=datas,
                envoyeur=envoyeur
            )
            message.save()

        if destinataires_reussis:
            messages.success(request, 'Message envoyé avec succès')
            return redirect('bunsess:messages_archives')
        else:
            messages.error(request, "Échec du message")
            return redirect('bunsess:messages')

    return render(request, 'bunsess/form_basic.html')







@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def messages_archives(request):
    saved_messages = Message.objects.all()
    return render(request, 'bunsess/tables.html', {'saved_messages': saved_messages})




class ExportConventionCSVView(View):
    
    def get(self, request, *args, **kwargs):
        conventions = Demandeconventions.objects.filter(statut='convention')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="convention.csv"'

        writer = csv.writer(response, delimiter=';')
        writer.writerow(['ID', 'num_ordre', 'nombre_hectare', 'commune', 'nom_demandeur', 'ref_piece'])

        for convention in conventions:
            writer.writerow([convention.id, convention.num_ordre, convention.nombre_hectare, convention.commune, convention.nom_demandeur, convention.ref_piece])

        return response
    
    
    
class ExportSitesCSVView(View):
    
    def get(self, request, *args, **kwargs):
        sites = Comsites.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sites.csv"'

        writer = csv.writer(response, delimiter=';')
        writer.writerow(['ID', 'code_site', 'date_creation', 'nom_site', 'typesite', 'statut'])

        for site in sites:
            # Vérifiez si typesite et statut sont None, remplacez-les par une chaîne vide
            typesite_libelle = site.typesite.libelle if site.typesite else ''
            statut_libelle = site.statut.libelle if site.statut else ''

            writer.writerow([site.id, site.code_site, site.date_creation, site.nom_site, typesite_libelle, statut_libelle])

        return response





 




         

        