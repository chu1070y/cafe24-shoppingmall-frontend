import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from shoppingmall_frontend.decorator import login_decorator
from shoppingmall_frontend.utils import RestAPI, product_result

rest_api = RestAPI()


def login(request):
    if request.method == "POST":
        result = rest_api.api_post("/api/admin/login", json.dumps({'id': request.POST['id'], 'pw': request.POST['pw']}))
        result_body = json.loads(result)

        if result_body['result'] == 'fail':
            return redirect('/manager/login?result=fail')

        authadmin = result_body['data']
        request.session['authadmin'] = authadmin

        return redirect('/manager/user')

    return render(request, 'manager/sign-in.html')


@login_decorator
def user(request):
    result = json.loads(rest_api.api_get("/api/user/list"))
    return render(request, 'manager/user.html', {'result': result})


def logout(request):
    del request.session['authadmin']
    return redirect('/manager/')


@login_decorator
def product(request):
    result = ''

    if request.method == "POST":
        data = product_result(request)
        print(data)
        result = json.loads(rest_api.api_post("/api/product/add", json.dumps(data)))

        if result['result'] == 'success':
            return redirect('/manager/productlist')

    category_list = json.loads(rest_api.api_get("/api/category/list"))

    return render(request, 'manager/product.html',
                  {'category_list': category_list, 'result': result})


@login_decorator
def productlist(request):
    product_list = json.loads(rest_api.api_get("/api/product/list"))

    return render(request, 'manager/productlist.html',
                  {'product_list': product_list})


@login_decorator
def categoryadd(request):
    parent = None
    if request.POST['parent'] != '0':
        parent = request.POST['parent']

    result = rest_api.api_post("/api/category/add",
                               json.dumps({'parent': parent, 'category_name': request.POST['category_name']}))

    return redirect('/manager/product')


@login_decorator
def lowlist(request):
    result = rest_api.api_get("/api/category/lowList", {'parent': request.GET['parent']})

    return HttpResponse(result, content_type='application/json')


@login_decorator
def order(request):
    order_list = json.loads(rest_api.api_get("/api/order/getOrder"))

    return render(request, 'manager/order.html',
                  {'order_list': order_list['data'], 'json': json.dumps(order_list['data'])})
