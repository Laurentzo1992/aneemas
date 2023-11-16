from modules_externe.imports import *
from technique.serializers import ComsitesSerializer

##################################################################################################
# Webmapping
##################################################################################################

def webmapp(request):
    sites = Comsites.objects.all()
    # Serialize infrastructures to JSON
    sites = list(sites.values())
    context = {'sites': sites}
    return render(request, 'technique/site/carte.html', context)



class ComsitesViewset(ModelViewSet):
    serializer_class = ComsitesSerializer
    def get_queryset(self):
        return Comsites.objects.all()


##################################################################################################
# Site 
##################################################################################################


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def site(request):
    sites = Comsites.objects.all().order_by('created')
    paginator = Paginator(sites, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/site/site.html', context)



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_site(request):
    if request.method=="POST":
        form = ComsitesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Ajour effectué !")
            return redirect('site')
        else:
            return render(request, 'technique/site/add.html', {"form":form})
    else:
        form = ComsitesForm()
        return render(request, 'technique/site/add.html', {"form":form})
    

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_site(request, id):
    site = Comsites.objects.get(id=id)
    if request.method == 'POST':
        form = ComsitesForm(request.POST, instance=site)
        if form.is_valid():
            form.save(id)
            messages.success(request, "Modification effectué avec susccès!")
            return redirect('site')
    else:
        form = ComsitesForm(instance=site)
    return render(request, 'technique/site/edit.html', {'site':site, 'form':form})



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def delete_site(request, id):
    site = Comsites.objects.get(id = id)
    site.delete()
    messages.success(request, 'supprimer avec susccès !')
    return HttpResponseRedirect(reverse("site"))



#########################################################################
# Fiche de enrolement
#########################################################################
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
 

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def syn_detail(request, identifiant):
    result = get_api_data_id_enrolement(FICHE_ENROLMENT_URL, identifiant)
    if result:
        return render(request, 'technique/enrolement/detail.html', {"result":result})
    else:
        return render(request, 'technique/enrolement/erreur.html', {'message': 'ID non trouvé'})

 

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    enrolements = Fichenrolements.objects.all().order_by('created')
    paginator = Paginator(enrolements, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/enrolement/enrolement.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def carte(request, id):
    result  = get_object_or_404(Fichenrolements, id=id)
    fiche = LigneTypeCarte.objects.filter(fiche=result)
    return render(request, 'technique/enrolement/carte.html', {'result': result, 'types_de_carte': types_de_carte})
    

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
    

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete(request, id):
    enrolement = Fichenrolements.objects.get(id = id)
    enrolement.delete()
    messages.success(request, 'supprimer avec susccès !')
    return HttpResponseRedirect(reverse("list_enrolement"))
  




#########################################################################
# Fiche guide guide autorité
#########################################################################
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index1(request):
    guides = Formguidautorites.objects.all().order_by('created')
    paginator = Paginator(guides, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/visite_activite/guide_fiche_liste.html', context)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def delete_guide(request, id):
    guide = Formguidautorites.objects.get(id = id)
    guide.delete()
    messages.success(request, 'supprimer avec susccès !')
    return HttpResponseRedirect(reverse("guide_fiche"))

#########################################################################
# Fiche viste
#########################################################################
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index2(request):
    vistes = Fichevisites.objects.all().order_by('created')
    paginator = Paginator(vistes, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/visite_activite/visite_fiche_liste.html', context)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
 

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def syn_detail_conv(request, identifiant):
    result = get_api_data_id_convention(FICHE_CONVENTION_URL, identifiant)
    if result:
        return render(request, 'technique/convention/detail.html', {"result":result})
    else:
        return render(request, 'technique/convention/erreur.html', {'message': 'ID non trouvé'})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index3(request):
    demandes = Demandeconventions.objects.filter(statut="demande").order_by('created')
    paginator1 = Paginator(demandes, 10)
    page_number1 = request.GET.get("page")
    page_obj1 = paginator1.get_page(page_number1)
    
    instructions = Demandeconventions.objects.filter(statut="instruction").order_by('created')
    paginator2 = Paginator(instructions, 10)
    page_number2 = request.GET.get("page")
    page_obj2 = paginator2.get_page(page_number2)
    
    
    
    signatures = Demandeconventions.objects.filter(statut="signature").order_by('created')
    paginator3 = Paginator(signatures, 10)
    page_number3 = request.GET.get("page")
    page_obj3 = paginator3.get_page(page_number3)
    
    
    conventions = Demandeconventions.objects.filter(statut="convention").order_by('created')
    paginator4 = Paginator(conventions, 10)
    page_number4 = request.GET.get("page")
    page_obj4 = paginator4.get_page(page_number4)
    
    
    nulls = Demandeconventions.objects.filter(statut="anuler").order_by('created')
    paginator5 = Paginator(nulls, 10)
    page_number5 = request.GET.get("page")
    page_obj5 = paginator5.get_page(page_number5)
    
    
    context = {"page_obj5":page_obj5, "page_obj1":page_obj1, "page_obj2":page_obj2, "page_obj3":page_obj3, "page_obj4":page_obj4}
    return render(request, 'technique/convention/index.html', context)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def instruire(request, id):
    instruction = Demandeconventions.objects.get(id=id)
    if instruction:
        instruction.statut = "instruction"
        # Mettre à jour les autres informations de livraison ici
        instruction.save()
        messages.success(request, "Votre demande passe à instruction")
        return HttpResponseRedirect(reverse("convention"))
    else:
        return render(request, 'technique/convention/index.html')
    
    
    
    
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def instruire_anull(request, id):
    instruction_anl = Demandeconventions.objects.get(id=id)
    if instruction_anl:
        instruction_anl.statut = "demande"
        # Mettre à jour les autres informations de livraison ici
        instruction_anl.save()
        messages.success(request, "Votre instruction est annulée ")
        return HttpResponseRedirect(reverse("convention"))
    else:
        return render(request, 'technique/convention/index.html')
    
    
    
    
    
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signature_anull(request, id):
    signature_anul = Demandeconventions.objects.get(id=id)
    if signature_anul:
        signature_anul.statut = "instruction"
        # Mettre à jour les autres informations de livraison ici
        signature_anul.save()
        messages.success(request, "Renvois pour instruction")
        return HttpResponseRedirect(reverse("convention"))
    else:
        return render(request, 'technique/convention/index.html')
 
 
 
    
    
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def signature_anull1(request, id):
    signature_anul = Demandeconventions.objects.get(id=id)
    if signature_anul:
        signature_anul.statut = "anuler"
        # Mettre à jour les autres informations de livraison ici
        signature_anul.save()
        messages.success(request, "Demande de convention annulée ")
        return HttpResponseRedirect(reverse("convention"))
    else:
        return render(request, 'technique/convention/index.html')
    
    
    
    
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def signature(request, id):
    signature = Demandeconventions.objects.get(id=id)
    if signature:
        signature.statut = "signature"
        # Mettre à jour les autres informations de livraison ici
        signature.save()
        messages.success(request, "Votre demande passe à la signature")
        return HttpResponseRedirect(reverse("convention"))
    else:
        return render(request, 'technique/convention/index.html')
   
   
   
   
    
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
def signe(request, id):
    signature = Demandeconventions.objects.get(id=id)
    if signature:
        signature.statut = "convention"
        # Mettre à jour les autres informations de livraison ici
        signature.save()
        messages.success(request, "Votre demande est  signe")
        return HttpResponseRedirect(reverse("convention"))
    else:
        return render(request, 'technique/convention/index.html')




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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





@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_convention1(request, id):
    convention = Demandeconventions.objects.get(id=id)
    if request.method == 'POST':
        form = DemandeconventionsForm(request.POST,request.FILES, instance=convention)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.statut = 'instruction'
            instance.save()
            messages.success(request, "Traitement effectué avec susccès!")
            return redirect('convention')
    else:
        form = DemandeconventionsForm(instance=convention)
    return render(request, 'technique/convention/edit1.html', {'convention':convention, 'form':form})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_convention2(request, id):
    convention = Demandeconventions.objects.get(id=id)
    if request.method == 'POST':
        form = DemandeconventionsForm(request.POST,request.FILES, instance=convention)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.statut = 'signature'
            instance.save()
            messages.success(request, "Traitement effectué avec susccès!")
            return redirect('convention')
    else:
        form = DemandeconventionsForm(instance=convention)
    return render(request, 'technique/convention/edit2.html', {'convention':convention, 'form':form})





@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_convention(request, id):
    convention = Demandeconventions.objects.get(id = id)
    convention.delete()
    messages.success(request, 'supprimer avec susccès !')
    return HttpResponseRedirect(reverse("convention"))





#########################################################################
# Fiche de accident - incident
#########################################################################


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
        
        nom_site = Comsites.objects.get(id=int(result['nom_site']))
        # Créez une instance de votre modèle avec les données de l'API
        fiche = Formincidents(
            identifiant=result['identifiant'],
            region = region,
            province = province,
            commune =result['commune'],
            nom_localite = result['nom_localite'],
            nom_site = nom_site,
            type_rapport = result['type_rapport'],
            date_incident = result['question5'],
            heure_incident = result['question6'],
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
 




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def syn_detail_acc(request, identifiant):
    result = get_api_data_id_accident(FICHE_ACCIDENT_URL, identifiant)
    if result:
        return render(request, 'technique/accident/detail.html', {"result":result})
    else:
        return render(request, 'technique/accident/erreur.html', {'message': 'ID non trouvé'})

 

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index4(request):
    incidents = Formincidents.objects.all().order_by('created')
    paginator = Paginator(incidents, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/accident/incident.html', context)


    

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
    

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_incident(request, id):
    incident = Formincidents.objects.get(id = id)
    incident.delete()
    messages.success(request, 'supprimer avec susccès !')
    return HttpResponseRedirect(reverse("incident"))




#########################################################################
# Fiche rapport d'activité
#########################################################################
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
 

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def syn_detail_rapp(request, identifiant):
    result = get_api_data_id_rapport(FICHE_RAPPORT_URL, identifiant)
    if result:
        return render(request, 'technique/rapport/detail.html', {"result":result})
    else:
        return render(request, 'technique/rapport/erreur.html', {'message': 'ID non trouvé'})

 

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index5(request):
    incidents = Rapactivites.objects.all().order_by('created')
    paginator = Paginator(incidents, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'technique/rapport/rapport.html', context)


    

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
    

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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




@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_rapport(request, id):
    rapport = Rapactivites.objects.get(id = id)
    rapport.delete()
    messages.success(request, 'supprimer avec susccès !')
    return HttpResponseRedirect(reverse("rapport"))



