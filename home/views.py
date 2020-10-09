from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login , logout 
from datetime import datetime
from django.contrib.auth.models import User
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
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\AA\\Desktop\\Django\\zohaib\static\\tesseract\\tesseract.exe'




data = None
url = None


# Create your views here.
def index(request):
    context = {"home": "active"}
    return render(request, 'index.html', context)

def qrcode(request):
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


def services(request):
    return render(request, 'services.html')

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
        dom = request.POST['dom']
        dom=whois.whois(dom)
        context={'dom':dom,'domain_name':dom["domain_name"][1],
        'creation_date':dom["creation_date"],
        'expiration_date':dom["expiration_date"],
        'registrar':dom["registrar"]}
        return render(request, 'whoisdomain.html',context)
    else:
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
        name = request.POST["name"]
        username = request.POST["uname"]
        email = request.POST["exampleInputEmail1"]
        password = request.POST["Password1"]
        myuser = User.objects.create_user(username,email,password)
        myuser.first_name =  name
        myuser.save()
        return redirect('login')

    else:
        return render(request, 'signup.html')


def handlelogin(request):
    if request.method == "POST":
        email = request.POST["exampleInputEmail1"]
        password = request.POST["Password1"]
    return render(request, 'login.html')


