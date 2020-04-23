from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from zipfile import ZipFile

# Create your views here.
def upload(request):
    context = dict()
    if request.method == "POST":
        uploaded_file = request.FILES["document"]
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        context['fileZip'] = uploaded_file.name

        root_dirs = list()
        dirs = list()
        files = list()

        zip_f = ZipFile(uploaded_file)
        for f in zip_f.namelist():
            zinfo = zip_f.getinfo(f)
            if zinfo.is_dir():
                r_dir = f.split('/')
                r_dir = r_dir[0]
                if r_dir not in root_dirs:
                    root_dirs.append(r_dir)


        for f in zip_f.namelist():
            zinfo = zip_f.getinfo(f)
            if(zinfo.is_dir()):
                num = 0
                for i in root_dirs:
                    if i+'/' == f:
                        num += 1
                if num == 0:
                    dirs.append(f)


        for f in zip_f.namelist():
            if '.' in f:
                files.append(f)
        
        
        context['root_dirs'] = root_dirs
        context['dirs'] = dirs
        context['files'] = files


    return render(request, "index.html", context)