"""zohaib URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from home import views  

urlpatterns = [
    path("", views.index, name='home'),
    path("qrcode", views.qrcode, name='qrcode'),
    path("services", views.services, name='services'),
    path("contact", views.contact, name='contact'),
    path("urlshort", views.urlShort, name='urlshort'),
    path('speed_test', views.speed_test, name='speed_test'),
    path('speed_test_result', views.speed_test, name='speed_test_result'),
    path('ipcheck', views.ipcheck, name='ipcheck'),
    path('iplocation', views.ipcheck, name='iplocation'),
    path('whoisdomain', views.domain_check, name='whoisdomain'),
    path('img_to_text', views.img_to_text, name='img_to_text'),
    path('pdf_to_txt', views.pdf_to_txt, name='pdf_to_txt'),
    

]

