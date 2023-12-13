import datetime
from decimal import Decimal
from multiprocessing import Value
from urllib.parse import urlencode
from django.forms import CharField
from django.shortcuts import render, redirect, get_object_or_404
from authentication.serializers import UserSerializer
from commercial.forms import LingotAdminForm
from commercial.models import Facture, FactureProforma, FicheTarification, FicheTarification, Fichecontrol, Fournisseur, Lingot, LingotsDisponiblesPourVente, Payement, TransferedFicheTarification, Vente
from commercial.serializers import FactureSerializer, FicheTarificationSerializer, FichecontrolSerializer, PayementSerializer, VenteSerializer
from commercial.units import UnitConverter
from modules_externe.cours_or import get_data_by_url
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.template.loader import get_template, render_to_string
from paramettre.models import Regions
import json

from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import gettext as _

from django.db.models import Sum

from django.contrib.admin.views.decorators import staff_member_required

from sigips import settings  # Import the decorator
from dateutil import parser
import random
from django.db.models.functions import Coalesce
from django.db.models import Sum, F, FloatField, Case, When, Value
from num2words import num2words

def cours_or_by_api(request):
    context = {}
    # Appelez la fonction pour obtenir les données
    try:
        data = get_data_by_url()
        context = {"data": data}
    except:
        print("pas de données")

    return render(request, 'commercial/or.html', context)


def add_lingot(request, pk):
    fiche_control = FicheTarification.objects.get(id=pk)
    lingots = Lingot.objects.filter(fiche_control=fiche_control)
    form = LingotAdminForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            lingot = form.save(commit=False)
            lingot.fiche_control = fiche_control
            lingot.save()
        else:
            return render(request, "commercial/fichecontrol/partials/lingot_form.html", context={
                "form": form
            })

        context = {
            "form": form,
            "fiche_control": fiche_control,
            "lingots": lingots
        }

        return render(request, "commercial/lingot/add_lingot.html", context)


def update_lingot(request, pk):
    lingot = Lingot.objects.get(id=pk)
    form = LingotAdminForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("detail-lingot", pk=lingot.id)

    context = {
        "form": form,
        "lingot": lingot
    }

    return render(request, "commercial/lingot/partials/lingot_form.html", context)


def delete_lingot(request, pk):
    lingot = get_object_or_404(Lingot, id=pk)

    if request.method == "POST":
        lingot.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


def detail_lingot(request, pk):
    lingot = get_object_or_404(Lingot, id=pk)
    context = {
        "lingot": lingot
    }
    return render(request, "commercial/lingot/partials/lingot_detail.html", context)


def add_lingot_form(request):
    form = LingotAdminForm()
    context = {
        "form": form
    }
    return render(request, "commercial/lingot/partials/lingot_form.html")


def generate_dataset(size=20, min_value=5000000, max_value=60000000):
    return [random.randint(min_value, max_value) for _ in range(size)]

def get_stock_or_by_fournisseur():
    # Aggregate total_or_fin per fournisseur
    lingot_data = Lingot.objects.values('fournisseur__nom', 'fournisseur__prenom').annotate(
        total_or_fin=Coalesce(Sum('or_fin', output_field=FloatField()), Value(0, output_field=FloatField()))
    )
    
    # Extracting the labels and sums
    labels = []
    for d in lingot_data:
        labels += [
            str(d['fournisseur__nom']) + str(d['fournisseur__prenom'])
        ]
    sums = [float(data['total_or_fin']) for data in lingot_data]

    # Returning the data as JSON
    data = {'labels': labels, 'sums': sums}
    return data

def get_stock_or_by_type_fournisseur():
    # Aggregate total_or_fin per fournisseur
    lingot_data = Lingot.objects.values('fournisseur__type_fournisseur__libelle').annotate(
        total_or_fin=Coalesce(Sum('or_fin', output_field=FloatField()), Value(0, output_field=FloatField()))
    )

    

    
    # Extracting the labels and sums
    labels = ['Inconnu' if str(data['fournisseur__type_fournisseur__libelle']) == 'None' else str(data['fournisseur__type_fournisseur__libelle']) for data in lingot_data]
    sums = [float(data['total_or_fin']) for data in lingot_data]

    # Returning the data as JSON
    data = {'labels': labels, 'sums': sums}
    return data

def bi_data(request):
    fts = TransferedFicheTarification.objects.all()
    lgts = Lingot.objects.all()
    data11 = {
        "name": "or",
        "label": "Or par fournisseur",
        "labels": get_stock_or_by_fournisseur().get('labels'),
        "datasets": [
            {
                "period": "day",
                "label": "Or par fournisseur",
                "data": get_stock_or_by_fournisseur().get('sums'),
                "toal": 500,
                "fill": False
            }
        ]
    }

    data12 = {
        "name": "argent",
        "label": "Or par type fournisseur",
        "labels": get_stock_or_by_type_fournisseur().get('labels'),
        "datasets": [
            {
                "period": "day",
                "label": "Or par type fournisseur",
                "labels": [ft.numero for ft in fts],
                "data": get_stock_or_by_type_fournisseur().get('sums'),
                "toal": 500,
                "fill": False
            },
        ]
    }

    data13 = {
        "name": "impuretes",
        "label": "impuretes par fournisseur",
        "labels": [ft.numero for ft in fts],
        "datasets": [
            {
                "period": "day",
                "label": "Cold trading",
                "labels": [ft.numero for ft in fts],
                "data": [float(ft.total_price) for ft in fts],
                "toal": 500,
                "fill": False
            },
            {
                "period": "month",
                "label": "Comti trading",
                "data": generate_dataset(),
                "toal": 500,
                "fill": False
            },
            {
                "period": "day",
                "label": "Sonata mining",
                "data": generate_dataset(),
                "toal": 500,
                "fill": False
            },
        ]
    }

    data1 = {
        "name": "stock",
        "label": "Stock de metaux",
        "children": [data11, data12, data13],
        "labels": [
            "FTR00011-23",
            "FTR00010-23",
            "FTR00009-23",
            "FTR00012-23",
            "FTR00002-23",
            "FTR00011-23",
            "FTR00010-23",
            "FTR00009-23",
            "FTR00012-23",
            "FTR00002-23"
        ],
        "datasets": [
            {
                "period": "day",
                "label": "Or",
                "labels": [
                    "FTR00011-23",
                    "FTR00010-23",
                    "FTR00009-23",
                    "FTR00012-23",
                    "FTR00002-23"
                ],
                "data": [
                    2856865.0,
                    90489543.0,
                    204122.0,
                    5934413.0,
                    24558445.0,
                    50000000,
                ],
                "toal": 500,
            },
            {
                "period": "month",
                "label": "Argent",
                "data": [
                    57400288,
                    15500241,
                    27123384,
                    57457059,
                    15595446,
                    55358005,
                    39469444,
                ],
                "toal": 500,
            },
            {
                "period": "day",
                "label": "Impuretes",
                "data": [
                    21203336,
                    44603651,
                    53891767,
                    47422425,
                    14339439,
                    27040629,
                    15033455,
                    5275207,
                    36303758,
                ],
                "toal": 500,
            }
        ]
    }

    data2 = {
        "name": "ventes",
        "label": "Ventes",
        "labels": [ft.numero for ft in fts],
        "children": [data11, data12, data13],
        "datasets": [
            {
                "period": "day",
                "label": "Achat",
                "labels": [ft.numero for ft in fts],
                "data": [float(ft.total_price) for ft in fts],
                "toal": 500,
                "fill": False
            },
            {
                "period": "month",
                "label": "Vente",
                "data": generate_dataset(),
                "toal": 500,
                "fill": False
            },
            {
                "period": "day",
                "label": "Stock",
                "data": generate_dataset(),
                "toal": 500,
                "fill": False
            },
        ]
    }

    data3 = {
        "name": "achats",
        "label": "Achats",
        "labels": [ft.numero for ft in fts],
        "datasets": [
            {
                "period": "day",
                "label": "Achat",
                "labels": [ft.numero for ft in fts],
                "data": [float(ft.total_price) for ft in fts],
                "toal": 500,
                "fill": False
            },
            {
                "period": "month",
                "label": "Vente",
                "data": generate_dataset(),
                "toal": 500,
                "fill": False
            },
            {
                "period": "day",
                "label": "Stock",
                "data": generate_dataset(),
                "toal": 500,
                "fill": False
            },
            {
                "period": "paru",
                "label": "Par u",
                "labels": [ft.numero for ft in fts],
                "data": [float(ft.total_price) for ft in fts],
                "toal": 500,
                "fill": False
            },
            {
                "period": "parv",
                "label": "Par v",
                "data": generate_dataset(),
                "toal": 500,
                "fill": False
            },
            {
                "period": "pary",
                "label": "Par y",
                "data": generate_dataset(),
                "toal": 500,
                "fill": False
            },
        ]
    }

    context = {}
    data = [data1, data2, data3]

    if request.method == 'POST':
        path = request.POST.getlist('path[]', [])
    elif request.method == 'GET':
        path = request.POST.getlist('path[]', [])
    
    path = [int(p) for p in path] if path else None

    if not path or not isinstance(path, list) or len(path) == 0:
        return JsonResponse({'message': 'Invalid request1!'})
    
    

    
    children = None
    data_to_return = None
    for p in range(0, len(path)):
        if not data or not len(data) > 0 or path[p] > len(data)-1:
            break
        
        if isinstance(data, list):
            items = [i.get('label') for i in data]
            data_to_return = data[path[p]]
            if data_to_return.get('children') and len(data_to_return.get('children')) > 0:
                children = [c.get('label') for c in data[path[p]].get('children')]
                data = data_to_return.get('children')
            else:
                children = None
                break
        
    if data_to_return:
        if data_to_return.get('children'):
            data_to_return.pop('children')
        if children:
            data_to_return['children'] = children
        if items and len(items) > 0:
            data_to_return['items'] = items
        return JsonResponse(data_to_return, safe=False)
    else:
        return JsonResponse({}, safe=False)
    

def bi_view(request):
    return render(request, "commercial/admin/module_bi.html", {})


def lingots_disponibles_pour_vente_changelist(request):
    # Use the Lingot model's admin instance to get the changelist view
    from .adminsite import commercial_admin
    # Use the Lingot model's admin instance to get the changelist view
    lingot_admin = commercial_admin._registry[LingotsDisponiblesPourVente]

    # Create a copy of the LingotAdmin instance
    lingot_admin_copy = type(lingot_admin)(
        lingot_admin.model, commercial_admin,
    )

    # Override the change_list_template for this instance
    lingot_admin_copy.change_list_template = 'admin/commercial/lingotsdisponiblespourvente/change_list.html'

    # Call the changelist view with the modified instance
    response = lingot_admin_copy.changelist_view(request)

    return response


def fondre_lingot(request):
    # return render(request, "admin/change_list.html")

    from .adminsite import commercial_admin
    context = {
        # Use the name of the changelist view as the title
        'title': "model_admin.changelist_view.__name__",
        'app_label': "commercial",
        'opts': Lingot._meta,
        'app_list': settings.INSTALLED_APPS,
        'changelist_url': reverse(
            'gesco:commercial_lingot_changelist',
            current_app='commercial'
        ),
    }
    return render(request, 'admin/change_list.html', context)


def generate_fiche_control(request, pk):
    fiche_control = Fichecontrol.objects.get(id=pk)
    serializer = FichecontrolSerializer(fiche_control)
    # Load the HTML template
    context = serializer.data
    totals = \
        fiche_control.lingot_set.filter(pesee__actif=True)\
        .aggregate(poids_brut=Sum('pesee__poids_brut'),  poids_immerge=Sum('pesee__poids_immerge'))
    total = {
        "poids_brut": totals['poids_brut'],
        "poids_immerge": totals['poids_immerge'],
    }
    context['total'] = total
    context['user'] = request.user
    # return JsonResponse(serializer.data)
    return render(request, "commercial/fichecontrol/print/template2.html", context)


def generate_fiche_tarification(request, pk):
    fiche_tarification = FicheTarification.objects.get(id=pk)
    serializer = FicheTarificationSerializer(fiche_tarification)
    # Load the HTML template
    template = get_template('commercial/fichetarification/print/template.html')
    context = serializer.data

    # context['user'] = request.user
    context['cours'] = Decimal(round(Decimal(context['cours']), 4))
    lingots = Lingot.objects.filter(
        fichecontrol=fiche_tarification.fichecontrol)
    sum_price = sum(Decimal(lingot.price) for lingot in lingots)
    sum_poids = sum(Decimal(lingot.or_fin) for lingot in lingots)
    context['total_price'] = Decimal(round(Decimal(sum_price), 0))
    context['total_poids'] = Decimal(round(Decimal(sum_poids), 4))

    html_content = template.render(context)
    # return JsonResponse(context)
    return render(request, "commercial/fichetarification/print/template.html", context)

    html_string = render_to_string(
        'commercial/fichecontrol/print/template2.html', context, request=request)
    pdf = pdfkit.from_string(html_string, False)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'
    return response

    # Generate PDF using WeasyPrint
    return HttpResponse(HTML(string=html_content, base_url=request.build_absolute_uri()))
    pdf_file = HTML(string=html_content,
                    base_url=request.build_absolute_uri()).write_pdf()

    # Create HttpResponse with PDF content
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename=invoice.pdf'
    return response

def translate(value, cours_dollar):
    return round(Decimal(value)/Decimal(cours_dollar), 4)


def generate_facture(request, pk, template_file=None):

    if template_file is None:
        template_file = "admin/commercial/facture/print.html"

    facture = Facture.objects.get(id=pk)
    serializer = FactureSerializer(facture)
    context = serializer.data

    vente = Vente.objects.filter(facture=facture).first()
    context['user'] = UserSerializer(request.user).data
    context['vente'] = VenteSerializer(vente).data
    context['type_de_facture'] = facture.type_de_facture

    

    poids_g = {}
    prix_g = {}
    reduct_g = {}
    apayer_g = {}

     
    converter = UnitConverter()
    us = request.GET.getlist('u', None)
    context['units'] = us
    any_substance_reduced = None
    reduction_commercial = context['reduction_commercial']
    if reduction_commercial and Decimal(context['reduction_commercial']) > 0:
        reduction_commercial = Decimal(context['reduction_commercial'])
        reduct_g['xof'] = reduction_commercial
    else:
        reduction_commercial = None
    
    pourcentage_tva = context['pourcentage_tva']
    if pourcentage_tva and Decimal(context['pourcentage_tva']) > 0:
        pourcentage_tva = Decimal(context['pourcentage_tva'])
    else:
        pourcentage_tva = None
    

    cours_du_dollar = context['cours_du_dollar']
    if cours_du_dollar and Decimal(cours_du_dollar) > 0:
        cours_du_dollar = Decimal(cours_du_dollar)
        reduct_g['usd'] = translate(reduction_commercial, cours_du_dollar) if reduction_commercial else reduction_commercial
    else:
        context['cours_du_dollar'] = None

    cours_en_euro = context['cours_en_euro']
    if cours_en_euro and Decimal(cours_en_euro) > 0:
        cours_en_euro = Decimal(cours_en_euro)
        reduct_g['euro'] = translate(reduction_commercial, cours_en_euro) if reduction_commercial else reduction_commercial
    else:
        context['cours_en_euro'] = None

    t_poids = 0
    t_prix = 0
    key = 0
    for p in context.get('prix_des_substances', []):
        t_poids += Decimal(p['poids'])
        t_prix += Decimal(p['prix'])

        cours = {}
        reduct = {}
        reduct_calc = {}
        poids = {}
        prix = {}
        prix_xof = Decimal(p['prix']) if p['prix'] and Decimal(p['prix']) > 0 else p['prix']
        prix['xof'] = {'gram': prix_xof}
        if cours_du_dollar and Decimal(cours_du_dollar) > 0:
            prix['usd'] = {'gram': translate(prix_xof, cours_du_dollar)}

        if cours_en_euro and Decimal(cours_en_euro) > 0:
            prix['euro'] = {'gram': translate(prix_xof, cours_en_euro)}
        
        poids_gram = Decimal(p['poids']) if p['poids'] and Decimal(p['poids']) > 0 else  p['poids']
        poids['gram'] = poids_gram
        
        cours_de_substance = p['cours_de_substance']
        reduction = p['reduction_commercial']

        if cours_de_substance and Decimal(cours_de_substance) > 0:
            cours_de_substance = Decimal(cours_de_substance)
            cours['xof'] = {'gram': cours_de_substance}
            if cours_du_dollar and Decimal(cours_du_dollar) > 0:
                cours['usd'] = {'gram': translate(cours_de_substance, cours_du_dollar)}
            if cours_en_euro and Decimal(cours_en_euro) > 0:
                cours['euro'] = {'gram': translate(cours_de_substance, cours_en_euro)}

        if reduction and Decimal(reduction) > 0:
            any_substance_reduced = True
            reduction = Decimal(reduction)
            reduction_calculer_xof_gram = round(reduction * Decimal(p['poids']), 4)
            reduct_calc['xof'] = {'gram': reduction_calculer_xof_gram}
            reduct['xof'] = {'gram': reduction}
            if cours_du_dollar and Decimal(cours_du_dollar) > 0:
                reduct['usd'] = {'gram': translate(reduction, cours_du_dollar)}
                reduct_calc['usd'] = {'gram': translate(reduction_calculer_xof_gram, cours_du_dollar)}
            if cours_en_euro and Decimal(cours_en_euro) > 0:
                reduct['euro'] = {'gram': translate(reduction, cours_en_euro)}
                reduct_calc['euro'] = {'gram': translate(reduction_calculer_xof_gram, cours_en_euro)}
        
        if us and len(us) > 0:
            for u in us:
                if u in ["ounce", "ounce_troy"]:
                    prix['xof'][u] = converter.convert(prix_xof, 'gram', u) if prix_xof else prix_xof
                    poids[u] = converter.convert(poids_gram, 'gram', u) if poids_gram else poids_gram
                    if cours_de_substance and Decimal(cours_de_substance) > 0:
                        cours['xof'][u] = converter.convert(cours_de_substance, 'gram', u)
                        
                    if reduction and Decimal(reduction) > 0:
                        reduct['xof'][u] = converter.convert(reduct['xof']['gram'], 'gram', u)
                        reduct_calc['xof'][u] = converter.convert(reduct_calc['xof']['gram'], 'gram', u)

            if cours_du_dollar and Decimal(cours_du_dollar) > 0:
                cours_de_substance_dollar = translate(cours_de_substance, cours_du_dollar)
                # cours['usd'] = {'gram': cours_de_substance_dollar}
                reduction_dollar = translate(reduction, cours_du_dollar) if reduction and Decimal(reduction) > 0 else None

                # reduct['usd'] = {'gram': reduction_dollar}
                prix_dollar = translate(prix_xof, cours_du_dollar)
                prix['usd'] = {'gram': prix_dollar}
                if us and len(us) > 0:
                    for u in us:
                        if u in ["ounce", "ounce_troy"]:
                            if cours_de_substance and Decimal(cours_de_substance) > 0:
                                cours['usd'][u] = converter.convert(cours_de_substance_dollar, 'gram', u)
                                prix['usd'][u] = converter.convert(prix_dollar, 'gram', u)
                                if reduction_dollar:
                                    reduct['usd'][u] = converter.convert(reduct['usd']['gram'], 'gram', u)

            if cours_en_euro and Decimal(cours_en_euro) > 0:
                cours_de_substance_euro = translate(cours_de_substance, cours_en_euro)
                # cours['euro'] = {'gram': cours_de_substance_euro}
                reduction_euro = translate(reduction, cours_en_euro) if reduction and Decimal(reduction) > 0 else None
                # reduct['euro'] = {'gram': reduction_euro}
                prix_euro = translate(prix_xof, cours_en_euro)
                prix['euro'] = {'gram': prix_euro}
                if us and len(us) > 0:
                    for u in us:
                        if u in ["ounce", "ounce_troy"]:
                            if cours_de_substance and Decimal(cours_de_substance) > 0:
                                cours['euro'][u] = converter.convert(cours_de_substance_euro, 'gram', u)
                                prix['euro'][u] = converter.convert(prix_euro, 'gram', u)
                                if not reduction_euro is None:
                                    reduct['euro'][u] = converter.convert(reduct['euro']['gram'], 'gram', u)

        p['cours_de_substance'] = cours
        p['reduction_commercial'] = reduct
        p['reduction_commercial_calculated'] = reduct_calc
        p['poids'] = poids
        p['prix'] = prix
        key += 1
    
    montant_apres_reduction = t_prix
    if reduction_commercial:
        context['reduction_commercial'] = reduct_g
        reduction_commercial = Decimal(reduction_commercial)
        context['pourcentage_reduction'] = round(reduction_commercial/t_prix, 6)*100
        montant_apres_reduction -= reduction_commercial
    
    montant_tva = 0
    if pourcentage_tva:
        montant_tva = round(Decimal(montant_apres_reduction) * Decimal(pourcentage_tva) / 100, 4)
        context['montant_tva'] = {'xof': montant_tva}
        if cours_du_dollar and Decimal(cours_du_dollar) > 0:
            context['montant_tva']['usd'] = translate(montant_tva, cours_du_dollar)
        if cours_en_euro and Decimal(cours_en_euro) > 0:
            context['montant_tva']['euro'] = translate(montant_tva, cours_en_euro)

    apayer = montant_apres_reduction + Decimal(montant_tva)
    apayer_g['xof'] = apayer
    if cours_du_dollar and Decimal(cours_du_dollar) > 0:
        apayer_g['usd'] = translate(apayer, cours_du_dollar)
    if cours_en_euro and Decimal(cours_en_euro) > 0:
        apayer_g['euro'] = translate(apayer, cours_en_euro)
        
        
    prix_g['xof'] = t_prix
    if cours_du_dollar and Decimal(cours_du_dollar) > 0:
        prix_g['usd'] = translate(t_prix, cours_du_dollar)

    if cours_en_euro and Decimal(cours_en_euro) > 0:
        prix_g['euro'] = translate(t_prix, cours_en_euro)
    
    
    poids_g['gram'] = t_poids
    if us and len(us) > 0:
        for u in us:
            if u in ["ounce", "ounce_troy"]:
                poids_g[u] = converter.convert(t_poids, 'gram', u)

    
    context['prix'] = prix_g
    context['apayer'] = apayer_g
    context['poids'] = poids_g
    context['any_substance_reduced'] = any_substance_reduced

    if pourcentage_tva or reduction_commercial:
        to_letterize = round(apayer)
    else:
        to_letterize = round(prix_g['xof'])
    t_letter = num2words(to_letterize, lang='fr')
    t_letter = t_letter[:1].upper() + t_letter[1:]

    context['total_letter'] = t_letter
    

    # return JsonResponse(context)
    return render(request, template_file, context)

def view_facture(request, pk):
    # return JsonResponse({'me': None})
    return generate_facture(request, pk, template_file="admin/commercial/facture/view.html")

def generate_recu_payement_achat(request, pk):
    # Use get_object_or_404 for better error handling
    paiement = get_object_or_404(Payement, id=pk)
    fiche_tarification = get_object_or_404(
        FicheTarification, id=paiement.fichetarification.pk)

    # Retrieve paiement_precedent
    paiement_precedent = Payement.objects.filter(
        fichetarification=paiement.fichetarification, created__lt=paiement.created)
    total_precedent = sum(py.montant for py in paiement_precedent)
    total_price = sum(
        lingot.price for lingot in fiche_tarification.fichecontrol.lingot_set.all())
    # Serialize objects directly in the context
    context = {
        'fichetarification': FicheTarificationSerializer(fiche_tarification).data,
        'paiement': PayementSerializer(paiement).data,
        'paiement_precedents': PayementSerializer(paiement_precedent, many=True).data,
        'total_precedent': total_precedent,
        'reste_initial': total_price - total_precedent,
        'reste_actuel': total_price - total_precedent - paiement.montant,
        'total_payer': total_precedent + paiement.montant,
        'reste_total': total_price - (total_precedent + paiement.montant)
    }

    # Load the HTML template
    template = get_template('commercial/fichetarification/print/template.html')
    html_content = template.render(context)

    # If you want to return JSON response
    # return JsonResponse(context)

    return render(request, "commercial/print/recu_payement_achat.html", context)

    html_string = render_to_string(
        'commercial/fichecontrol/print/template2.html', context, request=request)
    pdf = pdfkit.from_string(html_string, False)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'
    return response

    # Generate PDF using WeasyPrint
    return HttpResponse(HTML(string=html_content, base_url=request.build_absolute_uri()))
    pdf_file = HTML(string=html_content,
                    base_url=request.build_absolute_uri()).write_pdf()

    # Create HttpResponse with PDF content
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename=invoice.pdf'
    return response


@staff_member_required
def commercial_payement_archiver_view(request, object_id):
    # Your logic to set the 'archived' field to True for the Payement object
    payement = Payement.objects.get(pk=object_id)
    payement.archived = True
    payement.save()

    # Redirect back to the index of Payement in the admin
    return redirect(reverse('gesco:commercial_payement_changelist'))


@staff_member_required
def commercial_tarification_transferer(request, object_id):
    # Your logic to set the 'archived' field to True for the Payement object
    tarification = FicheTarification.objects.get(pk=object_id)
    tarification.transferer = True
    tarification.save()

    # Redirect back to the index of Payement in the admin
    # params = {'transferer__exact': 0}
    # url_with_params = reverse('gesco:commercial_transferedfichetarification_changelist') + '?' + urlencode(params)
    return redirect(reverse('gesco:commercial_transferedfichetarification_changelist'))


@staff_member_required
def commercial_tarification_changelist(request, object_id):

    # Redirect back to the index of Payement in the admin
    # params = {'transferer__exact': 0}
    # url_with_params = reverse('gesco:commercial_transferedfichetarification_changelist') + '?' + urlencode(params)
    return redirect(reverse('gesco:commercial_fichetarification_changelist') + "/?transferer__exact=0")
