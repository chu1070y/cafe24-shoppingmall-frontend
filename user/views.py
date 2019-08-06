import json

from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from user.utils import RestAPI

rest_api = RestAPI()


def info(request):
    return render(request, 'user/info.html')


def logout(request):
    del request.session['authuser']
    return redirect('/shoppingmall/index')


def login(request):
    if request.method == "POST":
        result = rest_api.api_post("/api/user/login", json.dumps({'id': request.POST['id'], 'pw': request.POST['pw']}))
        result_body = json.loads(result)

        if result_body['result'] == 'fail':
            return render(request, 'user/login.html', {'fail': 'fail'})

        authuser = result_body['data']
        print(result_body['data'])
        request.session['authuser'] = authuser

        return redirect('/shoppingmall/index')

    return render(request, 'user/login.html')


def join(request):

    if request.method == "POST":

        if request.POST['tel_home'] == "":
            tel_home = None

        if request.POST['gender'] == "":
            gender = None

        if request.POST['birthdate'] == "":
            birthdate = None

        result = rest_api.api_post("/api/user/registerMember", json.dumps({
            "id": request.POST['id'],
            'pw': request.POST['pw'],
            'name': request.POST['name'],
            'email': request.POST['email'],
            'tel_home': tel_home,
            'tel_phone': request.POST['tel_phone'],
            'gender': gender,
            'birthdate': birthdate
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
