import requests
import json
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from authentication.serializers import UserRegistrationSerializer, UserSerializer, UserLoginSerilizer
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from technique.forms import *
from modules_externe.api_enrolment import get_data_by_api_enrolement, get_api_data_id_enrolement
from modules_externe.api_convention import get_data_by_api_convention, get_api_data_id_convention
from modules_externe.api_accident import get_data_by_api_accident, get_api_data_id_accident
from modules_externe.api_rapport import get_data_by_api_rapport, get_api_data_id_rapport
from modules_externe.api_url import FICHE_ENROLMENT_URL, FICHE_CONVENTION_URL, FICHE_ACCIDENT_URL, FICHE_RAPPORT_URL



#########################################################################
# Fiche de enrolement
#########################################################################

def get_api_enrolement(request):
    #recuperer les données de l'api 
    data = get_data_by_api_enrolement(FICHE_ENROLMENT_URL)
    #recuperer les données existant dans la base de données
    existing_ids = Fichenrolements.objects.values_list('identifiant', flat=True)
    #Filtrer les données qui existent pas dans la base
    new_data = [item for item in data if item['identifiant'] not in existing_ids]
    paginator = Paginator(new_data, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/enrolement/api_data.html', context)



def save_api_data_to_database(request, identifiant):
    # Vérifiez si l'identifiant existe déjà dans la base de données
    if Fichenrolements.objects.filter(identifiant=identifiant).exists():
        messages.error(request, "Données déjà synchronisées !")
        return redirect('list_enrolement')
    
    # Obtenir l'élément de l'API en fonction de l'ID
    result = get_api_data_id_enrolement(FICHE_ENROLMENT_URL, identifiant)

    if result:
        # Créez une instance de votre modèle avec les données de l'API
        fiche = Fichenrolements(
            identifiant=result['identifiant'],
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
        
        for type_carte_api_id in result['type_carte']:
            type_carte_id = Typecarte.objects.get(id=type_carte_api_id)
            LigneTypeCarte.objects.create(carte=type_carte_id, fiche=fiche)

        # Redirigez vers la page liste des enrolments
        messages.success(request, "Données enregistrées avec succès !")
        return redirect('list_enrolement')
    else:
        # Gérer le cas où l'ID spécifié n'est pas trouvé
        messages.error(request, "ID non trouvé !")
        return redirect('api_enrolement')
 


def syn_detail(request, identifiant):
    result = get_api_data_id_enrolement(FICHE_ENROLMENT_URL, identifiant)
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
    result  = get_object_or_404(Fichenrolements, id=id)
    fiche = LigneTypeCarte.objects.filter(fiche=result)
    return render(request, 'technique/enrolement/carte.html', {'result': result, 'types_de_carte': types_de_carte})
    


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
    enrolement.delete()
    messages.success(request, 'supprimer avec susccès !')
    return HttpResponseRedirect(reverse("list_enrolement"))
  




#########################################################################
# Fiche guide guide autorité
#########################################################################

def index1(request):
    guides = Formguidautorites.objects.all().order_by('created')
    paginator = Paginator(guides, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/visite_activite/guide_fiche_liste.html', context)


def add_guide(request):
    if request.method=="POST":
        form = FormguidautoritesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Ajour effectué !")
            return redirect('guide_fiche')
        else:
            return render(request, 'technique/visite_activite/add_guide.html', {"form":form})
    else:
        form = FormguidautoritesForm()
        return render(request, 'technique/visite_activite/add_guide.html', {"form":form})



def edit_guide(request, id):
    guide = Formguidautorites.objects.get(id=id)
    if request.method == 'POST':
        form = FormguidautoritesForm(request.POST, instance=guide)
        if form.is_valid():
            form.save(id)
            messages.success(request, "Modification effectué avec susccès!")
            return redirect('guide_fiche')
    else:
        form = FormguidautoritesForm(instance=guide)
    return render(request, 'technique/visite_activite/edit_guide.html', {'guide':guide, 'form':form})


     
def delete_guide(request, id):
    guide = Formguidautorites.objects.get(id = id)
    guide.delete()
    messages.success(request, 'supprimer avec susccès !')
    return HttpResponseRedirect(reverse("guide_fiche"))

#########################################################################
# Fiche viste
#########################################################################

def index2(request):
    vistes = Fichevisites.objects.all().order_by('created')
    paginator = Paginator(vistes, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/visite_activite/visite_fiche_liste.html', context)


def add_visite(request):
    if request.method=="POST":
        form = FichevisitesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Ajour effectué !")
            return redirect('visite_fiche')
        else:
            return render(request, 'technique/visite_activite/add_visite.html', {"form":form})
    else:
        form = FichevisitesForm()
        return render(request, 'technique/visite_activite/add_visite.html', {"form":form})



def edit_visite(request, id):
    viste = Fichevisites.objects.get(id=id)
    if request.method == 'POST':
        form = FichevisitesForm(request.POST, instance=viste)
        if form.is_valid():
            form.save(id)
            messages.success(request, "Modification effectué avec susccès!")
            return redirect('visite_fiche')
    else:
        form = FichevisitesForm(instance=viste)
    return render(request, 'technique/visite_activite/edit_visite.html', {'viste':viste, 'form':form})





def delete_visite(request, id):
    viste = Fichevisites.objects.get(id = id)
    if request.method=='POST':
        viste.delete()
        messages.success(request, 'supprimer avec susccès !')
        return redirect("visite_fiche")
    return render(request, 'technique/visite_activite/delete_visite.html', {"viste":viste})






#########################################################################
# Fiche de demande convention
#########################################################################


def api_enrolement_conv(request):
    #recuperer les données de l'api 
    data = get_data_by_api_convention(FICHE_CONVENTION_URL)
    #recuperer les données existant dans la base de données
    existing_ids = Demandeconventions.objects.values_list('identifiant', flat=True)
    #Filtrer les données qui existent pas dans la base
    new_data = [item for item in data if item['identifiant'] not in existing_ids]
    paginator = Paginator(new_data, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/convention/api_data.html', context)



def save_api_data_to_database_conv(request, identifiant):
    # Vérifiez si l'identifiant existe déjà dans la base de données
    if Demandeconventions.objects.filter(identifiant=identifiant).exists():
        messages.error(request, "Données déjà synchronisées !")
        return redirect('convention')
    
    # Obtenir l'élément de l'API en fonction de l'ID
    result = get_api_data_id_convention(FICHE_CONVENTION_URL, identifiant)

    if result:
        region1 = Regions.objects.get(id=int(result['com_region1']))
        province1 = Provinces.objects.get(id=int(result['com_province1']))
        
        region2 = Regions.objects.get(id=int(result['com_region2']))
        province2 = Provinces.objects.get(id=int(result['com_province2']))
        # Créez une instance de votre modèle avec les données de l'API
        demande = Demandeconventions(
            identifiant=result['identifiant'],
            nombre_hectare=result['q2'],
            localite=result['localite_demande'],
            region=region1,
            province=province1,
            commune=result['commune1'],
            identifiaction=result['q4'],
            demande=result['q5'],
            nom_demandeur=result['nom_personne'],
            ref_piece=result['ref'],
            localite_demandeur=result['nom_localite2'],
            region_demandeur=region2,
            province_demandeur=province2,
            commune_demandeur=result['commune2'],
            pays = result['q14'],
            telephone = result['telephone'],
            email = result['question18'],
            site_web =  result['question19'],
            substances = result['substance1'],
            docs = result['question26'],
            point = result['point'],
            pointforme = result['question35'] ,
            nom_convntion = result['question34'] ,
            date_depot = result['question45'],
            heure_depot = result['question46'],
            deposant = result['question47'],
            statut = "demande"
            
        )

        # Enregistrez l'instance dans la base de données
        demande.save()
        
        for type_autorisation_api_id in result['type_autorisation']:
            type_autorisation_id = Typautorisations.objects.get(id=type_autorisation_api_id)
            LigneTypeAutorisation.objects.create(autorisation=type_autorisation_id, demande=demande)
            

        # Redirigez vers la page liste des enrolments
        messages.success(request, "Données enregistrées avec succès !")
        return redirect('convention')
    else:
        # Gérer le cas où l'ID spécifié n'est pas trouvé
        messages.error(request, "ID non trouvé !")
        return redirect('api_enrolement_conv')
 


def syn_detail_conv(request, identifiant):
    result = get_api_data_id_convention(FICHE_CONVENTION_URL, identifiant)
    if result:
        return render(request, 'technique/convention/detail.html', {"result":result})
    else:
        return render(request, 'technique/convention/erreur.html', {'message': 'ID non trouvé'})



def index3(request):
    demandes = Demandeconventions.objects.all().order_by('created')
    paginator = Paginator(demandes, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    #context = {"demandes":demandes}
    context = {"page_obj":page_obj}
    return render(request, 'technique/convention/index.html', context)


def instruire(request, id):
    instruction = Demandeconventions.objects.get(id=id)
    if instruction:
        instruction.statut = "instruction"
        # Mettre à jour les autres informations de livraison ici
        instruction.save()
        messages.success(request, "Votre demande passe à l'etape instruction")
        return HttpResponseRedirect(reverse("convention"))
    else:
        return render(request, 'technique/convention/index.html')


def add_convention(request):
    if request.method=="POST":
        form = DemandeconventionsForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.statut = "demande"
            instance.save()
            messages.success(request, "Ajour effectué !")
            return redirect('convention')
        else:
            return render(request, 'technique/convention/add.html', {"form":form})
    else:
        form = DemandeconventionsForm()
        return render(request, 'technique/convention/add.html', {"form":form})



def edit_convention(request, id):
    convention = Demandeconventions.objects.get(id=id)
    if request.method == 'POST':
        form = DemandeconventionsForm(request.POST,request.FILES, instance=convention)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.statut = "demande"
            instance.save()
            messages.success(request, "Modification effectué avec susccès!")
            return redirect('convention')
    else:
        form = DemandeconventionsForm(instance=convention)
    return render(request, 'technique/convention/edit.html', {'convention':convention, 'form':form})




def delete_convention(request, id):
    convention = Demandeconventions.objects.get(id = id)
    convention.delete()
    messages.success(request, 'supprimer avec susccès !')
    return HttpResponseRedirect(reverse("convention"))





#########################################################################
# Fiche de accident - incident
#########################################################################

def get_api_accident(request):
    #recuperer les données de l'api 
    data = get_data_by_api_accident(FICHE_ACCIDENT_URL)
    #recuperer les données existant dans la base de données
    existing_ids = Formincidents.objects.values_list('identifiant', flat=True)
    #Filtrer les données qui existent pas dans la base
    new_data = [item for item in data if item['identifiant'] not in existing_ids]
    paginator = Paginator(new_data, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/accident/api_data.html', context)



def save_api_data_to_database_acc(request, identifiant):
    # Vérifiez si l'identifiant existe déjà dans la base de données
    if Formincidents.objects.filter(identifiant=identifiant).exists():
        messages.error(request, "Données déjà synchronisées !")
        return redirect('incident')
    
    # Obtenir l'élément de l'API en fonction de l'ID
    result = get_api_data_id_accident(FICHE_ACCIDENT_URL, identifiant)

    if result:
        region = Regions.objects.get(id=int(result['com_region']))
        province = Provinces.objects.get(id=int(result['com_province']))
        # Créez une instance de votre modèle avec les données de l'API
        fiche = Formincidents(
            identifiant=result['identifiant'],
            region = region,
            province = province,
            commune =result['commune'],
            nom_localite = result['nom_localite'],
            nom_site = result['nom_site'],
            type_rapport = result['type_rapport'],
            date_incident = result['question5'],
            heure_incident = result['question6'],
            type = result['type'],
            zone = result['question'],
            lieu =  result['question14'],
            degres = result['question7'],
            implication = result['question8'],
            personne_implique = result['question9'],
            equipement_implique = result['question10'],
            description = result['question11'],
            cause = result['question12'],
            action_corrective = result['question13'],
            mesure_de_securite = result['question14'],
            vict_hom = result['vict_hom'],
            vict_fem = result['vict_fem'],
            vict_enf = result['vict_enf'],
            mort_hom = result['mort_hom'],
            mort_fem = result['mort_fem'],
            mort_enf = result['mort_enf'],
            
        )

        # Enregistrez l'instance dans la base de données
        fiche.save()

        # Redirigez vers la page liste des enrolments
        messages.success(request, "Données enregistrées avec succès !")
        return redirect('incident')
    else:
        # Gérer le cas où l'ID spécifié n'est pas trouvé
        messages.error(request, "ID non trouvé !")
        return redirect('api_accident')
 


def syn_detail_acc(request, identifiant):
    result = get_api_data_id_accident(FICHE_ACCIDENT_URL, identifiant)
    if result:
        return render(request, 'technique/accident/detail.html', {"result":result})
    else:
        return render(request, 'technique/accident/erreur.html', {'message': 'ID non trouvé'})

 


def index4(request):
    incidents = Formincidents.objects.all().order_by('created')
    paginator = Paginator(incidents, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/accident/incident.html', context)


    


def add_incident(request):
    if request.method=="POST":
        form = FormincidentsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Ajour effectué !")
            return redirect('incident')
        else:
            return render(request, 'technique/accident/add.html', {"form":form})
    else:
        form = FormincidentsForm()
        return render(request, 'technique/accident/add.html', {"form":form})
    


def edit_incident(request, id):
    incident = Formincidents.objects.get(id=id)
    if request.method == 'POST':
        form = FormincidentsForm(request.POST, instance=incident)
        if form.is_valid():
            form.save(id)
            messages.success(request, "Modification effectué avec susccès!")
            return redirect('incident')
    else:
        form = FormincidentsForm(instance=incident)
    return render(request, 'technique/accident/edit.html', {'incident':incident, 'form':form})





def delete_incident(request, id):
    incident = Formincidents.objects.get(id = id)
    incident.delete()
    messages.success(request, 'supprimer avec susccès !')
    return HttpResponseRedirect(reverse("incident"))







#########################################################################
# Fiche rapport d'activité
#########################################################################

def get_api_rapport(request):
    #recuperer les données de l'api 
    data = get_data_by_api_rapport(FICHE_RAPPORT_URL)
    #recuperer les données existant dans la base de données
    existing_ids = Rapactivites.objects.values_list('identifiant', flat=True)
    #Filtrer les données qui existent pas dans la base
    new_data = [item for item in data if item['identifiant'] not in existing_ids]
    paginator = Paginator(new_data, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/rapport/api_data.html', context)



def save_api_data_to_database_rapp(request, identifiant):
    # Vérifiez si l'identifiant existe déjà dans la base de données
    if Rapactivites.objects.filter(identifiant=identifiant).exists():
        messages.error(request, "Données déjà synchronisées !")
        return redirect('rapport')
    
    # Obtenir l'élément de l'API en fonction de l'ID
    result = get_api_data_id_rapport(FICHE_RAPPORT_URL, identifiant)

    if result:
        be = Burencadrements.objects.get(id=int(result['question1']))
        # Créez une instance de votre modèle avec les données de l'API
        activite = Rapactivites(
            identifiant=result['identifiant'],
            burencadrement_id = be,
            periode1 =result['question3'],
            periode2 = result['question3_001'],
            nbr_conv = result['question5'],
            nbr_cart_art = result['question6'],
            autre1 = result['question8'],
            nbr_site = result['question13'],
            nbr_commite = result['question14'],
            nbr_site_org =  result['question15'],
            nbr_coop = result['question16'],
            nbr_enf = result['question18'],
            mercure = result['question19'],
            cyanure = result['question20'],
            acide = result['question21'],
            borate = result['question22'],
            chaux = result['question23'],
            explosif = result['question24'],
            autre = result['question25'],
            nouveau_site = result['question16_001'],
            site_ferme = result['question17'],
            site_reactive = result['question18_001'],
            site_rehabilite = result['question19_001'],
            minerai = result['question21_001'],
            type_com = result['question22_001'],
            quantite = result['question23_001'],
            obs = result['obs'],
            
        )

        # Enregistrez l'instance dans la base de données
        activite.save()
        for type_cart_art_api in result['question7']:
            type_carte_id = Typecarte.objects.get(id=type_cart_art_api)
            LigneTypeRapactivitesCarte.objects.create(typecarte=type_carte_id, activite=activite)
        # Redirigez vers la page liste des enrolments
        messages.success(request, "Données enregistrées avec succès !")
        return redirect('rapport')
    else:
        # Gérer le cas où l'ID spécifié n'est pas trouvé
        messages.error(request, "ID non trouvé !")
        return redirect('api_rapport')
 


def syn_detail_rapp(request, identifiant):
    result = get_api_data_id_rapport(FICHE_RAPPORT_URL, identifiant)
    if result:
        return render(request, 'technique/rapport/detail.html', {"result":result})
    else:
        return render(request, 'technique/rapport/erreur.html', {'message': 'ID non trouvé'})

 


def index5(request):
    incidents = Rapactivites.objects.all().order_by('created')
    paginator = Paginator(incidents, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/rapport/rapport.html', context)


    


def add_rapport(request):
    if request.method=="POST":
        form = RapactivitesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Ajour effectué !")
            return redirect('rapport')
        else:
            return render(request, 'technique/rapport/add.html', {"form":form})
    else:
        form = RapactivitesForm()
        return render(request, 'technique/rapport/add.html', {"form":form})
    


def edit_rapport(request, id):
    rapport = Rapactivites.objects.get(id=id)
    if request.method == 'POST':
        form = RapactivitesForm(request.POST, instance=rapport)
        if form.is_valid():
            form.save(id)
            messages.success(request, "Modification effectué avec susccès!")
            return redirect('rapport')
    else:
        form = RapactivitesForm(instance=rapport)
    return render(request, 'technique/rapport/edit.html', {'rapport':rapport, 'form':form})





def delete_rapport(request, id):
    rapport = Rapactivites.objects.get(id = id)
    rapport.delete()
    messages.success(request, 'supprimer avec susccès !')
    return HttpResponseRedirect(reverse("rapport"))