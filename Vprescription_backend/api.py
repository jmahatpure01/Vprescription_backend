from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import nltk
import requests


@csrf_exempt
@require_POST
def process(request):
    text_array = json.loads(request.body)
    name_array = []
    for text in text_array:
        tokens = nltk.wordpunct_tokenize(text)
        for token in tokens:
            print(token)
            r = requests.get("https://api.fda.gov/drug/ndc.json?search=generic_name:" + token + "&limit=1")
            if r.status_code == 200:
                data = r.json()
                if data:
                    name_array.append(data["results"][0]["brand_name"])

    return HttpResponse(json.dumps(name_array), content_type='application/json', status=201)
