import json

from django.shortcuts import render, redirect


# Create your views here.
from shoppingmall_frontend.utils import RestAPI

rest_api = RestAPI()


def login(request):
    if request.method == "POST":
        result = rest_api.api_post("/api/admin/login", json.dumps({'id': request.POST['id'], 'pw': request.POST['pw']}))
        result_body = json.loads(result)

        if result_body['result'] == 'fail':
            return render(request, 'admin/sign-in.html', {'fail': 'fail'})

        authadmin = result_body['data']
        request.session['authadmin'] = authadmin

        return redirect('/admin/user')

    return render(request, 'admin/sign-in.html')


def user(request):
    result = json.loads(rest_api.api_get("/api/user/list"))

    return render(request, 'admin/user.html', {'result': result})


def logout(request):
    del request.session['authadmin']
    return redirect('/shoppingmall/index')
