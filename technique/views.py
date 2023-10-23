from django.shortcuts import render
import requests
import json
from django.core.paginator import Paginator
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
from twilio.rest import Client
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from technique.forms import *



""" def api(request):
    header = {"Authorization": "Token 042467621a23d8e5e19c16beaa86f7c315bd649e"}
    kobo = requests.get("https://kf.kobotoolbox.org/api/v2/assets/aKhBahvtHVg5PzzcYi3Nxb/data.json",headers=header)
    if kobo.status_code==200:
        print("ok")
        api_data = json.loads(kobo.content)
        results = api_data.get('results', [])
        for result in results:
            result['id'] = result.pop('_id')
            result['submitted_by'] = result.pop('_submitted_by')
        paginator = Paginator(results, 8)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {"page_obj":page_obj}
    else:
        print("la ressource n'est pas disponible")
    return render(request, 'technique/enrolement/enrolement.html', context) """


def index(request):
    enrolements = Fichenrolements.objects.all().order_by('created')
    paginator = Paginator(enrolements, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/enrolement/enrolement.html', context)



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





def delete_client(request, id):
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



            



