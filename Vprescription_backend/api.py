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
            r = requests.get("https://www.practo.com/practopedia/api/v1/search?query=" + token + "&pincsode=560076")
            if r.status_code == 200:
                data = r.json()
                if data:
                    name_array.append(data[0]["display_text"])

    return HttpResponse(json.dumps(name_array), content_type='application/json', status=201)
