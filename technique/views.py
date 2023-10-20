from django.shortcuts import render
import requests
import json
from django.core.paginator import Paginator





def home(request):
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
    return render(request, 'technique/home/mobile.html', context)