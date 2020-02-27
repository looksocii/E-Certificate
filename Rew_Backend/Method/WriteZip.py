import zipfile

# Create your views here.
def AddZip():
    z = zipfile.ZipFile("test.zip","w")
    z.write("stu1.pdf")
    z.write("stu2.pdf")
    z.printdir()
    z.close()
AddZip()