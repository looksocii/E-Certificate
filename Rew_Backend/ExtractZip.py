import os
import zipfile
from os.path import pardir
from django.test import TestCase
from django.utils.archive import extract


# Create your tests here.
def find():
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if (os.path.join(root, name) == ".\pytthon.zip"):
                print("Found!", os.path.join(root, name))
                return os.path.join(root, name)
        for name in dirs:
            if (os.path.join(root, name) == ".\pytthon.zip"):
                print("Found!", os.path.join(root, name))
                return os.path.join(root, name)

def AddZip():
    data = zipfile.ZipFile(find(),'r')
    data.extractall()
    data.printdir()
    # data = data.read("tests.py")
    # print(data)
AddZip()
