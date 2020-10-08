from django.shortcuts import render,HttpResponse
from datetime import datetime
from home.models import Contact
from home.models import ImageUpload
from django.contrib import messages
from qrcode import *
import pyshorteners
from pytube import YouTube
import os
import speedtest
import math
import socket
import re
import json
from urllib.request import urlopen
import whois
from PIL import Image
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

url_yt = ''

def ytb_down(request):
    return render(request, 'ytb_main.html')

def yt_download(request):
    global url_yt
    url_yt = request.GET.get('url_yt')
    #created object for know which video download ..
    try:
        obj = YouTube(url_yt)
        resolutions = []
        strm_all = obj.streams.filter(progressive=True, file_extension='mp4')
        for i in strm_all:
            resolutions.append(i.resolution)
            resolutions = list(dict.fromkeys(resolutions))
            embed_link = url_yt.replace("watch?v=", "embed/")
            return render(request, 'yt_download.html', {'rsl': resolutions, 'embd': embed_link, 'url_yt': url_yt})
    except:
        return render(request, 'contact.html')



def download_complete(request, res):
    global url_yt
    homedir = os.path.expanduser("~")
    dirs = homedir + '/Downloads'
    print(f'DIRECT :', f'{dirs}/Downloads')
    if request.method == "POST":
        yt = YouTube(url_yt)
        yt.streams.get_by_resolution(res).download(homedir + '/Downloads')
        return render(request, 'download_complete.html')
    else:
        return render(request, 'index.html')

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
    



