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
from twilio.rest import Client
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from technique.forms import *
from modules_externe.cours_or import get_data_by_api, get_api_data_id
from modules_externe.api_url import FICHE_ENROLMENT_URL



def api_enrolement(request):
    data = get_data_by_api(FICHE_ENROLMENT_URL)
    paginator = Paginator(data, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/enrolement/api_data.html', context)




def save_api_data_to_database(request, id):
    # Obtenir l'élément de l'API en fonction de l'ID
    result = get_api_data_id(FICHE_ENROLMENT_URL, id)

    if result:
        # Créez une instance de votre modèle avec les données de l'API
        fiche = Fichenrolements(
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
        if Fichenrolements.objects.filter(identifiant=id).exists():
            fiche.save()
            type_cartes = []
        
            for type_carte_name in result['type_carte']:
                type_carte, created = Typecarte.objects.get_or_create(libelle=type_carte_name)
                type_cartes.append(type_carte)
            
            for type_carte in type_cartes:
                LigneTypeCarte.objects.create(carte=type_carte, fiche=fiche)
            # Redirigez vers la page liste des enrolments
            messages.success(request, "Données enregistrées avec succès !")
            return redirect('list_enrolement')
        
        else:
            messages.error(request, "données déja synchronisé !")
        
    else:
        # Gérer le cas où l'ID spécifié n'est pas trouvé
        messages.error(request, "ID non trouvé !")
        return redirect('api_enrolement')
        





def syn_detail(request, id):
    result = get_api_data_id(FICHE_ENROLMENT_URL, id)
    if result:
        return render(request, 'technique/enrolement/detail.html', {"result":result})
    else:
        return render(request, 'technique/enrolement/erreur.html', {'message': 'ID non trouvé'})

 


def index(request):
    enrolements = Fichenrolements.objects.all().order_by('created')
    paginator = Paginator(enrolements, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/enrolement/enrolement.html', context)



def carte(request, id):
    pk = get_object_or_404(Fichenrolements, id=id)
    result = LigneTypeCarte.objects.filter(fiche_id=pk)
    return HttpResponseRedirect('list_enrolement')



def add(request):
    if request.method=="POST":
        form = EnrolementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Ajour effectué !")
            return redirect('list_enrolement')
        else:
            return render(request, 'technique/enrolement/add.html', {"form":form})
    else:
        form = EnrolementForm()
        return render(request, 'technique/enrolement/add.html', {"form":form})
    


def edit(request, id):
    enrolement = Fichenrolements.objects.get(id=id)
    if request.method == 'POST':
        form = EnrolementForm(request.POST, instance=enrolement)
        if form.is_valid():
            form.save(id)
            messages.success(request, "Modification effectué avec susccès!")
            return redirect('list_enrolement')
    else:
        form = EnrolementForm(instance=enrolement)
    return render(request, 'technique/enrolement/edit.html', {'enrolement':enrolement, 'form':form})





def delete(request, id):
    enrolement = Fichenrolements.objects.get(id = id)
    if request.method=='POST':
        enrolement.delete()
        messages.success(request, 'supprimer avec susccès !')
        return redirect("list_enrolement")
    return render(request, 'technique/enrolement/delete.html', {"enrolement":enrolement})
     





def envoyer_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        destinataire = request.POST.get('destinataire')

        # Initialiser le client Twilio
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        # Envoyer le message
        message = client.messages.create(
            body=message,
            from_='+18159348590', 
            to=destinataire
        )

        return redirect('home')

    return render(request, 'technique/enrolement/message.html')



            



