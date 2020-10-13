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
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name='home'),
    path("qrcode", views.qrcodes, name='qrcode'),
    path("contact", views.contact, name='contact'),
    path("urlshort", views.urlShort, name='urlshort'),
    path('speed_test', views.speed_test, name='speed_test'),
    path('speed_test_result', views.speed_test, name='speed_test_result'),
    path('ipcheck', views.ipcheck, name='ipcheck'),
    path('iplocation', views.ipcheck, name='iplocation'),
    path('whoisdomain', views.domain_check, name='whoisdomain'),
    path('img_to_text', views.img_to_text, name='img_to_text'),
    path('pdf_to_txt', views.pdf_to_txt, name='pdf_to_txt'),
    path('signup', views.signup, name='signup'),
    path('login', views.handlelogin, name='login'),
    path('logout', views.handlelogout, name='logout'),
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
        name="password_reset_complete"),
    path('web_tech', views.web_tech, name='web_tech'),




    

]

