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





