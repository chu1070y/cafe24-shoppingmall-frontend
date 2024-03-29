import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from shoppingmall_frontend.utils import RestAPI

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
        tel_home = request.POST['tel_home']
        gender = request.POST['gender']
        birthdate = request.POST['birthdate']

        if tel_home == "":
            tel_home = None

        if gender == "":
            gender = None

        if birthdate == "":
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


def checkId(request):
    result = rest_api.api_get("/api/user/checkId", {"id": request.GET['id']})

    return HttpResponse(result, content_type='application/json')
