from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from user.utils import RestAPI

rest_api = RestAPI()


def login(request):
    return render(request, 'user/login.html')


def join(request):
    return render(request, 'user/join.html')


def checkId(request, id=""):
    result = rest_api.api_get("/api/user/checkId", {"id": id})

    return HttpResponse(result, content_type='application/json')
