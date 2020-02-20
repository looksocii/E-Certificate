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
    if request.method == "POST":
        uploaded_file = request.FILES["document"]
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        print(uploaded_file.name)
        ExtractZip(uploaded_file.name)
    return render(request, "upload.html")

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
    data.extractall(path="FileUnZiped")
    data.printdir()
    # data = data.read("tests.py")
    # print(data)