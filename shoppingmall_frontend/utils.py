import datetime
import uuid

import requests

from shoppingmall_frontend.settings import MEDIA_ROOT


class RestAPI:

    def __init__(self):
        self.url = "http://localhost:8080/shoppingmall"
        self.headers = {
            'content-type': "application/json"
        }

    def api_get(self, url, param=""):
        destination = self.url + url
        response = requests.get(destination, params=param)
        return response.text

    def api_post(self, url, data=""):
        destination = self.url + url
        response = requests.post(destination, data=data, headers=self.headers)
        return response.text


def product_result(request):
    data = request.POST
    img = request.FILES
    print(data)

    change_data = {'name': data.get('name'),
                   'code': product_code(),
                   'description': data.get('description'),
                   'show_product': data.get('show_product'),
                   'price': data.get('price'),
                   'sale_price': data.get('sale_price'),
                   'productDetailList': [],
                   'productImgList': [],
                   'categoryList': [],
                   'optionList': []
                   }

    product_detail_form = {'option_code': '',
                           'add_price': '',
                           'stock_num': '',
                           'stock_use': ''
                           }

    # 재고 - 미완성 재고개수등 다른 것도 넣어야함... 옵션과 같이 해야함
    for detail in data.get('stock_use'):
        product_detail_form['stock_use'] = detail

    # 이미지
    if img.get('mainImg') is not None:
        main_file = img.get('mainImg')
        main_filename = uuid_filename(main_file._name)
        product_img_form = {'filename': main_filename, 'img_type': 'main'}

        file_upload(main_file, main_filename)
        change_data['productImgList'].append(product_img_form)

    if img.get('addImg') is not None:
        add_files = img.getlist('addImg')

        for add_file in add_files:
            add_filename = uuid_filename(add_file._name)
            product_img_form = {'filename': add_filename, 'img_type': 'add'}

            file_upload(add_file, add_filename)
            change_data['productImgList'].append(product_img_form)

    change_data['productDetailList'].append(product_detail_form)

    # 카테고리
    categorylist = []
    for category_no in data.getlist('category_no'):
        if category_no == '없음':
            continue
        categorylist.append(category_no)
    change_data['categoryList'] = categorylist

    return change_data


def uuid_filename(filename):
    return str(uuid.uuid4()) + "-" + filename


def file_upload(main_file, main_filename):
    fp = open('%s/%s' % (MEDIA_ROOT, main_filename), 'wb')
    for chunk in main_file.chunks():
        fp.write(chunk)
    fp.close()


def product_code():
    code = "p0"
    code += str(datetime.datetime.today().year)
    code += str(datetime.datetime.today().month)
    code += str(datetime.datetime.today().day)
    code += str(datetime.datetime.today().hour)
    code += str(datetime.datetime.today().minute)
    code += str(datetime.datetime.today().second)
    code += str(datetime.datetime.today().microsecond)

    return code
