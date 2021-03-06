from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login , logout 
from datetime import datetime
from django.contrib.auth.models import User
from .forms import UserForm
from home.models import Contact
from home.models import ImageUpload
from django.contrib import messages
from qrcode import *
import pyshorteners
import os
import speedtest
import math
import socket
import re
import json
from urllib.request import urlopen
import whois
import builtwith
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'https://softappstool.herokuapp.com//static//tesseract//tesseract.exe'




data = None
url = None


# Create your views here.
def index(request):
    context = {"home": "active"}
    return render(request, 'index.html', context)

def qrcodes(request):
    global data
    if request.method == 'POST':
        data = request.POST['data']
        img = make(data)
        img.save("static/qrcode.png")
        return render(request, 'qrcode.html', {'data':data})
    else:
        return render(request, 'qrcode.html')



def urlShort(request):
    global url
    if request.method == 'POST':
        url = request.POST['url']
        url = pyshorteners.Shortener().tinyurl.short(url)
        return render(request, 'urlshort.html', {'url':url})
    else:
        return render(request, 'urlshort.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, 'Form has been Submitted')
    return render(request, 'contact.html')


def speed_test(request):
    if request.method == "POST":
        speed =speedtest.Speedtest()
        download = speed.download()
        download=download/1000000
        download="{:.2f}".format(download)
        upload = speed.upload()
        upload = upload/1000000
        upload = "{:.2f}".format(upload)
        ping = speed.results.ping
        ping = math.floor(ping)
        return render(request, 'speed_test_result.html', {'download':download,'upload':upload,'ping':ping})
    return render(request, 'speed_test.html')


def ipcheck(request):
    if request.method == "POST":
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        url = 'http://ipinfo.io/?token=9e871c2d81ddc5'
        response = urlopen(url)
        data = json.load(response)
        IP=data['ip']
        org=data['org']
        city = data['city']
        country=data['country']
        region=data['region']
        location=data['loc']
        postal=data['postal']
        timezone=data['timezone']
        return render(request, 'iplocation.html', {'hostname':hostname, 'ip_address':ip_address,'IP':IP ,'region': region ,'country':country, 'city':city, 'org': org,'location':location,'postal':postal,'timezone':timezone})
    return render(request, 'ipcheck.html')


def domain_check(request):
    if request.method == "POST":
        try:
            domainn = request.POST['dom']
            dom=whois.whois(domainn)
            context={'dom':domainn,'domain_name':dom["domain_name"][1],
            'creation_date':dom["creation_date"],
            'expiration_date':dom["expiration_date"],
            'registrar':dom["registrar"]}
            return render(request, 'whoisdomain.html',context)
        except TypeError:
            messages.error(request, 'Please Enter a Valid Domain')
    return render(request, 'whoisdomain.html')


def img_to_text(request):
    if request.method == "POST":
        p = request.FILES['img']
        im = Image.open(p)
        text = pytesseract.image_to_string(im)
        length = len(text)
        words = len(text.split()) 
        return render(request, 'img_to_text.html',{'text':text,'length':length,'words':words})
    else:
        return render(request, 'img_to_text.html')
    

def pdf_to_txt(request):
    if request.method == "POST":
        p = request.FILES['pdf']
        # file_path = 'C:\\Users\\AA\\Desktop\\sample.pdf'
        pdf = PdfFileReader(p)
        with open('static/yourtxt.txt', 'w') as f:
            for page_num in range(pdf.numPages):
                # print('Page: {0}'.format(page_num))
                pageObj = pdf.getPage(page_num)
        
                try: 
                    txt = pageObj.extractText()
                    # print(''.center(100, '-'))
                except:
                    pass
                else:
                    f.write('\n')
                    f.write(''.center(100, '-'))
                    f.write('\n')
                    f.write('Page {0}\n'.format(page_num+1))
                    f.write(txt)
            f.close()
        return render(request, 'pdf_to_txt.html',{'f':f})
    else:
        return render(request, 'pdf_to_txt.html')


def signup(request):
    if request.method == "POST":
        form1 = UserForm(request.POST)
        if form1.is_valid():
            username = form1.cleaned_data['username']
            first_name = form1.cleaned_data['first_name']
            last_name = form1.cleaned_data['last_name']
            email = form1.cleaned_data['email']
            password = form1.cleaned_data['password']
            
            User.objects.create_user(username=username,email=email, first_name=first_name, last_name=last_name, password=password,)
            return HttpResponseRedirect('/login')
    else:
        form1 = UserForm()
    return render(request, 'signup.html',{'frm':form1})
    


def handlelogin(request):
    if request.method == "POST":
        username = request.POST['username']
        loginpassword = request.POST['loginpass']
        
        user = authenticate(username=username, password=loginpassword)

        if user is not None:
            login(request, user)
            return redirect('/')
        else: 
            messages.error(request, "Credentials do not match, Try again")
    return render(request, 'login.html')

    

def handlelogout(request):
    logout(request)
    return redirect('login')



def web_tech(request):
    if request.method == "POST":
        web_technology = request.POST['web_tech']
        check_website = builtwith.parse(web_technology)
        # for key,value in check_website.items():
        #     result_web = key+':'+','.join(value) 
        return render(request, 'web_tech.html',{"check_website":check_website,'web_technology':web_technology})
                    
    return render(request, 'web_tech.html')
    


        


