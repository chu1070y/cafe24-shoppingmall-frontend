"""shoppingmall_frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import shoppingmall.views as shoppingmall_views
import user.views as user_views
import admin.views as admin_views

urlpatterns = [
    path('shoppingmall/index', shoppingmall_views.index),
    path('shoppingmall/detail/<int:no>', shoppingmall_views.detail),
    path('shoppingmall/cart', shoppingmall_views.cart),
    path('shoppingmall/cart_del', shoppingmall_views.cart_del),
    path('shoppingmall/order', shoppingmall_views.order),

    path('shoppingmall/error404', shoppingmall_views.error404),

    path('user/login', user_views.login),
    path('user/join', user_views.join),
    path('user/checkId', user_views.checkId),
    path('user/info', user_views.info),
    path('user/logout', user_views.logout),

    path('manager/user', admin_views.user),
    path('manager/', admin_views.login),
    path('manager/login', admin_views.login),
    path('manager/logout', admin_views.logout),
    path('manager/product', admin_views.product),

    path('manager/categoryadd', admin_views.categoryadd),
    path('manager/lowlist', admin_views.lowlist),
    path('manager/productlist', admin_views.productlist),

    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
