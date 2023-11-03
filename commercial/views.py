from django.shortcuts import render, redirect, get_object_or_404
from commercial.forms import LingotForm
from commercial.models import Fichecontrol, Lingot
from commercial.serializers import FichecontrolSerializer
from modules_externe.cours_or import get_data_by_url

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.template.loader import get_template, render_to_string
from django.shortcuts import render
from modules_externe.cours_or import get_data_by_url




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
    form = LingotForm(request.POST or None)
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
    form = LingotForm(request.POST or None)

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
    form = LingotForm()
    context = {
        "form": form
    }
    return render(request, "commercial/lingot/partials/lingot_form.html", context)

def generate_fiche_control(request, pk):
    fiche_control = Fichecontrol.objects.get(id=pk)
    serializer = FichecontrolSerializer(fiche_control)
    # Load the HTML template
    template = get_template('commercial/fichecontrol/print/template2.html')
    context = serializer.data
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