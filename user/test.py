import requests


def my_django_view():
    r = requests.get('http://localhost:8080/shoppingmall/api/user/checkId', params={"id": id})
    print(r)
    print(r.text)

    return "성공";


my_django_view()