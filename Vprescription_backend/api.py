from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import nltk
import requests
# import os
# from nltk.tag.stanford import StanfordNERTagger

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#jar = os.path.join(BASE_DIR, 'stanford-ner.jar')
#model = os.path.join(BASE_DIR, 'english.all.3class.distsim.crf.ser.gz')


@csrf_exempt
@require_POST
def process(request):
    data_array = json.loads(request.body)
    #ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')
    name_array = {"medicines": [], "names": [], "ages": []}
    for text in data_array:
        sentence_array = nltk.sent_tokenize(text)
        for sentence in sentence_array:
            if sentence.find("medication") > -1:
                sentences = sentence.split("medication")
            else:
                sentences = sentence.split("Medication")
            if sentence.find("age") > -1:
                name_text = sentences[0].split("age")
                name_array["ages"].append(name_text[1])
            else:
                name_text = sentences[0].split("Age")
                name_array["ages"].append(name_text[1])
            if sentence.find("name") > -1:
                name_array["names"].append(name_text[0].split("name")[1])
            else:
                name_array["names"].append(name_text[0].split("Name")[1])
            word_array = nltk.word_tokenize(sentences[1])
            #print(ner_tagger.tag(word_array))
            for word in word_array:
                print(word.capitalize())
                r = requests.get("https://api.fda.gov/drug/ndc.json?search=generic_name:" + word.capitalize() + "&limit=1")
                if r.status_code == 200:
                    data = r.json()
                    if data["results"][0].get("brand_name", 0):
                        name_array["medicines"].append(data["results"][0]["brand_name"])

    return HttpResponse(json.dumps(name_array), content_type='application/json', status=201)
