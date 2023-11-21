from urllib.parse import urlencode
from django.shortcuts import render, redirect, get_object_or_404
from commercial.forms import LingotAdminForm
from commercial.models import FicheTarification, Fichecontrol, Lingot, Payement, TransferedFicheTarification
from commercial.serializers import FichecontrolSerializer
from modules_externe.cours_or import get_data_by_url

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.template.loader import get_template, render_to_string
from django.shortcuts import render
from modules_externe.cours_or import get_data_by_url
from django.http import JsonResponse
from django.http import JsonResponse
from paramettre.models import Regions
import json

from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from django.db.models import Sum

from django.contrib.admin.views.decorators import staff_member_required  # Import the decorator






def cours_or_by_api(request):
    context = {}
    # Appelez la fonction pour obtenir les données
    try:
        data = get_data_by_url()
        context = {"data":data}
    except:
        print("pas de données")
   
    return render(request, 'commercial/or.html', context)

def add_lingot(request, pk):
    fiche_control = Fichecontrol.objects.get(id=pk)
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

def paiement(request):
    return render(request, "commercial/tabs.html")


def fondre_lingot(request, object_id):
    return render(request, "commercial/tabs.html")


def generate_fiche_control(request, pk):
    fiche_control = Fichecontrol.objects.get(id=pk)
    serializer = FichecontrolSerializer(fiche_control)
    # Load the HTML template
    template = get_template('commercial/fichecontrol/print/template2.html')
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
    html_content = template.render(context)
    # return JsonResponse(serializer.data)
    return render(request, "commercial/fichecontrol/print/template2.html", context)
    
    html_string = render_to_string('commercial/fichecontrol/print/template2.html', context, request=request)
    pdf = pdfkit.from_string(html_string, False)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'
    return response

    
    # Generate PDF using WeasyPrint
    return HttpResponse(HTML(string=html_content, base_url=request.build_absolute_uri()))
    pdf_file = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf()

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
