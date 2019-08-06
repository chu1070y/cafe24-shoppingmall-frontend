import json

from django.shortcuts import render, redirect


# Create your views here.
from user.views import rest_api


def login(request):
    if request.method == "POST":
        result = rest_api.api_post("/api/admin/login", json.dumps({'id': request.POST['id'], 'pw': request.POST['pw']}))
        result_body = json.loads(result)

        if result_body['result'] == 'fail':
            return render(request, 'admin/sign-in.html', {'fail': 'fail'})

        authuser = result_body['data']
        print(result_body['data'])
        request.session['authuser'] = authuser

        return redirect('/admin/user')

    return render(request, 'admin/sign-in.html')


def user(request):
    return render(request, 'admin/user.html')
