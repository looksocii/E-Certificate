import os
import zipfile
from os.path import pardir


# Create your tests here.
def find():
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if (os.path.join(root, name) == ".\\test.zip"):
                print("Found!", os.path.join(root, name))
                return os.path.join(root, name)
        for name in dirs:
            if (os.path.join(root, name) == ".\\test.zip"):
                print("Found!", os.path.join(root, name))
                return os.path.join(root, name)

def Extract():
    data = zipfile.ZipFile(find(),'r')
    ## read zipfile
    filedata = []
    for i in data.infolist():
        filedata.append(i.filename)
    print(filedata)
    ## read zipfile
    data.extractall()
    data.printdir()
Extract()
