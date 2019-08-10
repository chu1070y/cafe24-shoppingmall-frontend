import datetime
import json
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

    # 재고 및 옵션
    # 옵션을 사용하지 않고 재고만 사용할 경우
    test = json.loads(data.get('test'))

    if test['stock_use'] == '1':
        product_detail_form['stock_use'] = test['stock_use']
        product_detail_form['stock_num'] = test['stock_num']
        change_data['productDetailList'].append(product_detail_form)

    if test['option_use'] == '1':

        for option_detail in test['optionList']:
            option_detail['optionDetailList'] = [
                {'detail_name': value} for value in option_detail['optionDetailList'].split(',')
            ]

        change_data['optionList'] = test['optionList']

        change_data['productDetailList'] = [item for item in test['productDetailList'] if item is not None]

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

    # 카테고리
    for category_no in data.getlist('category_no'):
        if category_no == '없음':
            continue
        category_form = {'category_no': int(category_no)}
        change_data['categoryList'].append(category_form)

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
