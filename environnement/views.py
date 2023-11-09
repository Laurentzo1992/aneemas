import requests
import json
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
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
from paramettre.models import *
from environnement.forms import *
from modules_externe.api_exploitation import get_data_by_api_exploitation, get_api_data_id_exploitation
from modules_externe.api_prelevement import get_data_by_api_prelevement, get_api_data_id_prelevement
from modules_externe.api_url import FICHE_PRELEVEMENT_URL, FICHE_SUVI_EXPLOIATION_URL
from django.contrib.auth.decorators import login_required
from  django.views.decorators.cache import cache_control 


#########################################################################
# Fiche de prelevement
#########################################################################
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def api_prelevement(request):
    #recuperer les données de l'api 
    data = get_data_by_api_prelevement(FICHE_PRELEVEMENT_URL)
    #recuperer les données existant dans la base de données
    existing_ids = Ficheprelevements.objects.values_list('identifiant', flat=True)
    #Filtrer les données qui existent pas dans la base
    new_data = [item for item in data if item['identifiant'] not in existing_ids]
    paginator = Paginator(new_data, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'environnement/prelevement/api_data.html', context)




   


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def save_api_data_to_database_prelevement(request, identifiant):
    
    if Ficheprelevements.objects.filter(identifiant=identifiant).exists():
        messages.error(request, "Données déjà synchronisées !")
        return redirect('api_prelevement')
    # Obtenir l'élément de l'API en fonction de l'ID
    result = get_api_data_id_prelevement(FICHE_PRELEVEMENT_URL, identifiant)

    if result:
        #Créez une instance de votre modèle avec les données de l'API
        fiche = Ficheprelevements(
            identifiant=result['identifiant'],
            date_prelevement = result['date_prelev'],
            commune = result['commune'],
            #point_prelevement =result['point'],
            coordonnees = result['coordonnees'],
            coordonnees_manu = result['coordonnees_manu'],
            lieu = result['lieu'],
            motif = result['motif'],
            quantite = result['quantite'],
            nombre_flacons_verre = result['nb_facons_v'],
            nombre_flacons_plastique = result['nb_facons_p'],
            type_nature_echant = result['type_nature_echantillon'],
            conductivite = result['mis_conductivite'],
            ph = result['mis_ph'],
            tds =result['mis_tds'],
            oxigene_dissous = result['mis_oxigene_dissous'],
            turbidite = result['mis_turbidite'],
            #bruit = result['mis_bruits'],
            #odeur = result['mis_odeur'],
            #lumiere = result['mis_lumiere'],
            nom_preleveur = result['nom_personne1'],
            nom_personnes_commandiaire = result['nom_personne2'],
            adresse_personnes_commandiaire = result['adresse'],
            
        )
        # Enregistrez l'instance dans la base de données
        fiche.save()
        messages.success(request, "Données enregistrées avec succès !")
        return redirect('prelevement')
        
        
    else:
        # Gérer le cas où l'ID spécifié n'est pas trouvé
        messages.error(request, "ID non trouvé !")
        return redirect('api_prelevement')
        

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def syn_prelevement(request, id):
    result = get_api_data_id_prelevement(FICHE_PRELEVEMENT_URL, id)
    if result:
        return render(request, 'environnement/prelevement/detail.html', {"result":result})
    else:
        return render(request, 'environnement/prelevement/erreur.html', {'message': 'ID non trouvé'})

 

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    prelevements = Ficheprelevements.objects.all().order_by('created')
    paginator = Paginator(prelevements, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'environnement/prelevement/prelevement.html', context)




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_prelevement(request):
    if request.method=="POST":
        form = FicheprelevementsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Ajour effectué !")
            return redirect('prelevement')
        else:
            return render(request, 'environnement/prelevement/add.html', {"form":form})
    else:
        form = FicheprelevementsForm()
        return render(request, 'environnement/prelevement/add.html', {"form":form})
    

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_prelevement(request, id):
    prelevement = Ficheprelevements.objects.get(id=id)
    if request.method == 'POST':
        form = FicheprelevementsForm(request.POST, instance=prelevement)
        if form.is_valid():
            form.save()
            messages.success(request, "Modification effectué avec susccès!")
            return redirect('prelevement')
    else:
        form = FicheprelevementsForm(instance=prelevement)
    return render(request, 'environnement/prelevement/edit.html', {'prelevement':prelevement, 'form':form})




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_prelevement(request, id):
    prelevement = Ficheprelevements.objects.get(id = id)
    prelevement.delete()
    messages.success(request, 'supprimer avec susccès !')
    return HttpResponseRedirect(reverse("prelevement"))

     



#######################################################################################
# Fiche de suivie des exploitation artisanale
#######################################################################################
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def api_exploitation(request):
    #recuperer les données existant dans la base de données
    data = get_data_by_api_exploitation(FICHE_SUVI_EXPLOIATION_URL)
    existing_ids = Fichexpminieres.objects.values_list('identifiant', flat=True)
    #Filtrer les données qui existent pas dans la base
    new_data = [item for item in data if item['identifiant'] not in existing_ids]
    paginator = Paginator(new_data, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'environnement/exploitation/api_data.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def save_api_data_to_database_exploitation(request, identifiant):
    
    if Fichexpminieres.objects.filter(identifiant=identifiant).exists():
        messages.error(request, "Données déjà synchronisées !")
        return redirect('api_exploitation')
    # Obtenir l'élément de l'API en fonction de l'ID
    result = get_api_data_id_exploitation(FICHE_SUVI_EXPLOIATION_URL, identifiant)

    if result:
        # Créez une instance de votre modèle avec les données de l'API
        fiche = Fichexpminieres(
            identifiant=result['id'],
            nom=result['nom'],
            prenom=result['prenom'],
            date=result['date'],
            localite=result['localite'],
            telephone=result['telephone'],
            telephone2=result['telephone2'],
            quittance=result['quittance'],
            engagement=result['engagement'],
            num_carte=result['num_carte'],
            observation=result['observation'],
            ref_piece=result['ref_piece']
        )
        # Enregistrez l'instance dans la base de données
        fiche.save()
        
        messages.success(request, "Données enregistrées avec succès !")
        return redirect('exploitation')
        
    else:
        # Gérer le cas où l'ID spécifié n'est pas trouvé
        messages.error(request, "ID non trouvé !")
        return redirect('api_exploitation')
        

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def syn_detail_exploitation(request, identifiant):
    result = get_api_data_id_exploitation(FICHE_SUVI_EXPLOIATION_URL, identifiant)
    if result:
        return render(request, 'environnement/exploitation/detail.html', {"result":result})
    else:
        return render(request, 'environnement/exploitation/erreur.html', {'message': 'ID non trouvé'})



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def exploitation(request):
    exploitations = Fichexpminieres.objects.all().order_by('created')
    paginator = Paginator(exploitations, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'environnement/exploitation/exploitation.html', context)



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_exploitation(request):
    if request.method=="POST":
        form = FichexpminieresForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Ajour effectué !")
            return redirect('exploitation')
        else:
            messages.success(request, "formuliare invalide !")
            return render(request, 'environnement/exploitation/add.html', {"form":form})
    else:
        form = FichexpminieresForm()
        return render(request, 'environnement/exploitation/add.html', {"form":form})
    

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_exploitation(request, id):
    exploitation = Fichexpminieres.objects.get(id=id)
    if request.method == 'POST':
        form = FichexpminieresForm(request.POST, instance=exploitation)
        if form.is_valid():
            form.save(id)
            messages.success(request, "Modification effectué avec susccès!")
            return redirect('exploitation')
    else:
        form = FichexpminieresForm(instance=exploitation)
    return render(request, 'environnement/exploitation/edit.html', {'exploitation':exploitation, 'form':form})




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_exploitation(request, id):
    exploitation = Fichexpminieres.objects.get(id = id)
    exploitation.delete()
    messages.success(request, 'supprimer avec susccès !')
    return HttpResponseRedirect(reverse("exploitation"))