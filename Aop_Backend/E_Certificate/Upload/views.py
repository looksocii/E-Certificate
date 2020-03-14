from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
import os
import zipfile
from os.path import pardir
from django.test import TestCase
from django.utils.archive import extract

class Home(TemplateView):
    template_name = 'base.html'

def upload(request):
    context = dict()
    data = ['00001', '00002', '00003', '00004', '00005', '00006', '00007', '00008', '00009']
    context = {
        'data': data
    }
    # if request.method == "POST":
    #     uploaded_file = request.FILES["document"]
    #     print(uploaded_file)
    #     fs = FileSystemStorage()
    #     fs.save(uploaded_file.name, uploaded_file)
    #     print(uploaded_file.name)
    #     context['fileZip'] = ExtractZip(uploaded_file.name)

    return render(request, "drag_and_drop.html", context)

def find(fileZip):
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if (os.path.join(name) == fileZip):
                print("Found!", os.path.join(root, name))
                return os.path.join(root, name)
        for name in dirs:
            if (os.path.join(name) == fileZip):
                print("Found!", os.path.join(root, name))
                return os.path.join(root, name)

def ExtractZip(fileZip):
    data = zipfile.ZipFile(find(fileZip),'r')
    ## read zipfile
    filedata = []
    for i in data.infolist():
        filedata.append(i.filename)
    print(filedata)
    ## read zipfile
    data.extractall(path="FileUnZiped")
    data.printdir()
    # data = data.read("tests.py")
    # print(data)
    return filedata