import json

from django.shortcuts import render

# Create your views here.
from shoppingmall_frontend.settings import MEDIA_ROOT
from shoppingmall_frontend.utils import RestAPI

rest_api = RestAPI()


def index(request):
    product_list = json.loads(rest_api.api_get("/api/product/mainlist"))
    return render(request, 'shoppingmall/index.html', {'product_list': product_list})
