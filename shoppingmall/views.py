import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from shoppingmall_frontend.utils import RestAPI, order_data, nomember_cart

rest_api = RestAPI()


def index(request):
    if 'nomember' not in request.session:
        request.session['nomember'] = ""

    product_list = json.loads(rest_api.api_get("/api/product/mainlist"))
    return render(request, 'shoppingmall/index.html', {'product_list': product_list})


def detail(request, no=1):
    product_detail = json.loads(rest_api.api_get("/api/product/" + str(no)))

    if product_detail['result'] == 'fail':
        return redirect('/shoppingmall/error404')

    return render(request, 'shoppingmall/product-detail.html',
                  {'product_detail': product_detail['data'],
                   'json': json.dumps(product_detail['data'])})


def error404(request):

    return render(request, 'shoppingmall/404.html')


def cart(request):
    request.session['nomember'] = nomember_cart(request)

    if request.method == "POST":
        # 로그인 하지 않은 경우
        if 'authuser' not in request.session:
            result = rest_api.api_post("/api/cart/add", json.dumps({
                'nomember_no': request.session['nomember']['no'],
                'product_detail_no': request.POST['product_detail_no'],
                'quantity': request.POST['quantity'],
            }))
        else:
            # 로그인 한 경우
            result = rest_api.api_post("/api/cart/add", json.dumps({
                'member_no': request.session['authuser']['no'],
                'product_detail_no': request.POST['product_detail_no'],
                'quantity': request.POST['quantity'],
            }))

        return HttpResponse(result, content_type='application/json')

    # 로그인 하지 않은 경우
    if 'authuser' not in request.session:
        cart_list = json.loads(rest_api.api_get("/api/cart/list", {
            "nomember_no": request.session['nomember']['no']
        }))
    else:
        # 로그인 한 경우
        cart_list = json.loads(rest_api.api_get("/api/cart/list", {
            "member_no": request.session['authuser']['no']
        }))

    return render(request, 'shoppingmall/cart.html', {'cart_list': cart_list})


def cart_del(request):
    rest_api.api_post("/api/cart/delete", request.POST['no'])
    return redirect('/shoppingmall/cart')


def order(request):
    result = ""
    request.session['nomember'] = nomember_cart(request)

    if request.method == "POST":
        data = order_data(request)
        result = json.loads(rest_api.api_post("/api/order/add", json.dumps(data)))

        if result['result'] == 'success':
            print(result)
            return render(request, 'shoppingmall/order_success.html', {'result': result['data']})

    if 'authuser' not in request.session:
        cart_list = json.loads(rest_api.api_get("/api/cart/list", {
            "nomember_no": request.session['nomember']['no']
        }))
    else:
        cart_list = json.loads(rest_api.api_get("/api/cart/list", {
            "member_no": request.session['authuser']['no']
        }))

    if len(cart_list['data']) == 0:
        return redirect('/shoppingmall/cart')

    return render(request, 'shoppingmall/order.html', {'cart_list': cart_list, 'result': result})


def order_success(request):
    return render(request, 'shoppingmall/order_success.html')
