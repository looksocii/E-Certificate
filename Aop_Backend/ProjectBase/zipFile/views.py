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
        sub_files = list()
        sub_dirs = list()
        final_files = list()

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
                files.append(f.split('/'))

        for f in root_dirs:
            list_f = list()
            list_d = list()
            for i in files:
                if f in i:
                    list_f.append(i)
            for i in dirs:
                if f in i:
                    list_d.append(i)
            sub_files.append(list_f)
            sub_dirs.append(list_d)

        for i in range(len(root_dirs)):
            list_tmp = list()
            if len(sub_dirs[i]) != len(sub_files[i]):
                for d in range(len(sub_files[i])):
                    if d >= len(sub_dirs[i])-1:
                        list_tmp.append(sub_files[i][d])
                final_files.append(list_tmp)
            else:
                final_files.append(list_tmp)

        for i in range(len(root_dirs)):
            if len(final_files[i]) != 0:
                list_tmp = list()
                for f in range(len(sub_files[i])):
                    tmp = sub_files[i][f]
                    if tmp in final_files[i]:
                        list_tmp.append(tmp)
                        print(tmp)
                for d in list_tmp:
                    sub_files[i].remove(d)

        context['root_dirs'] = root_dirs
        context['dirs'] = sub_dirs
        context['files'] = sub_files
        context['final_files'] = final_files


    return render(request, "index.html", context)