import json

from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from user.utils import RestAPI

rest_api = RestAPI()


def login(request):
    return render(request, 'user/login.html')


def join(request):

    if request.method == "POST":
        result = rest_api.api_post("/api/user/registerMember", json.dumps({
            "id": request.POST['id'],
            'pw': request.POST['pw'],
            'name': request.POST['name'],
            'email': request.POST['email'],
            'tel_home': request.POST['tel_home'],
            'tel_phone': request.POST['tel_phone'],
            'gender': request.POST['gender'],
            'birthdate': request.POST['birthdate']
        }))

        result_body = json.loads(result)
        if result_body['result'] == 'fail':

            return render(request, 'user/join.html', {'result': result})
        elif result_body['data'] == '중복 아이디':
            return render(request, 'user/join.html', {'result': result})
        return render(request, 'user/login.html')

    return render(request, 'user/join.html')


def checkId(request, id=""):
    result = rest_api.api_get("/api/user/checkId", {"id": request.GET['id']})

    return HttpResponse(result, content_type='application/json')
