import json

from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from shoppingmall_frontend.utils import RestAPI

rest_api = RestAPI()


def index(request):
    product_list = json.loads(rest_api.api_get("/api/product/mainlist"))
    return render(request, 'shoppingmall/index.html', {'product_list': product_list})


def detail(request, no=1):
    product_detail = json.loads(rest_api.api_get("/api/product/" + str(no)))
    print(product_detail)

    if product_detail['result'] == 'fail':
        return redirect('/shoppingmall/error404')

    return render(request, 'shoppingmall/product-detail.html', {'product_detail': product_detail['data']})


def error404(request):

    return render(request, 'shoppingmall/404.html')
