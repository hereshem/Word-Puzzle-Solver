from django.http import HttpResponse
from django.shortcuts import render
import json

# Create your views here.
w = []
def get_words_from_file():
    if w: return w
    with open('words/words.txt') as fin:
        for l in fin: w.append(l.strip())
    print("reading file with words", len(w))
    return w

def check_letter(x,y):
    c = list(y)
    for i in x:
        if i in c: c.remove(i)
        else: return False
    return True

def find_words(number, chars):
    return list(filter(lambda x: len(x)==number and check_letter(x, chars), get_words_from_file()))

def home(request):
    data = {}
    if request.method == "POST":
        number = request.POST.get("number")
        chars = request.POST.get("chars")
        data["number"] = number
        data["chars"] = chars
        if chars and number and number.isdigit():
            data["words"] = find_words(int(number), chars.lower())
    return render(request, "words/index.html", data)

def api(request):
    data = {}
    chars = request.GET.get("chars")
    number = request.GET.get("length")
    if chars and number and number.isdigit():
        results = find_words(int(number), chars.lower())
        data["chars"] = chars
        data["length"] = number
        data["result_count"] = len(results)
        data["total_count"] = len(w)
        data["results"] = results
    else:
        data["error"] = True
        data["message"] = "'chars' and 'length' are compulsory fields"
    return HttpResponse(json.dumps(data), "application/json")
