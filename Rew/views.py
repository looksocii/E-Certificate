from django.shortcuts import render
import zipfile

# Create your views here.
def AddZip():
    z = zipfile.ZipFile("pytthon.zip","w")
    z.write("tests.py")
    z.write("models.py")
    z.printdir()
    z.close()
AddZip()