from django.shortcuts import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from zipfile import ZipFile
import json
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    return render(request, "home.html")

def my_login(request):
    context = dict()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # --------------- เช็คว่า username, password มีอยู่ในข้อมูลหรือไม่ ----------------
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else: # ไม่มีอยู่ในข้อมูล
            context = {
                'username': username,
                'password': password,
                'error': "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้องกรุณากรอกอีกครั้ง"
            }
            return render(request, 'login.html', context)
        # -------------------------------------------------------------------------
        

    # -------- เมื่อมีการส่ง request next มา ----------
    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url
    # --------------------------------------------
    
    return render(request, 'login.html', context)

@login_required
def my_logout(request):
    logout(request)
    return redirect('login')

def my_register(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST.get('username'))
        except ObjectDoesNotExist:
            user = None
        if user:
            context = {
                'error': "กรุณาตั้ง username ใหม่",
                'sign_page': "sign_page",
                'username': request.POST.get('username'),
                'password': request.POST.get('password'),
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'email': request.POST.get('email')
            }
            return render(request, 'signup.html', context)
        else:
            user = User.objects.create_user(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email')
            )
            user.save()
            return redirect('login')

    return render(request, 'signup.html')

@login_required
def issue(request):
    return render(request, "issue001.html")

@login_required
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

        print('----------------- OUTPUT -------------------')
        context['root_dirs'] = root_dirs
        context['dirs'] = sub_dirs
        context['files'] = sub_files
        context['final_files'] = final_files


        files_sub = list()
        for i in sub_files[0]:
            files_sub.append(i[len(i)-1])
        json_befor = dict()
        json_befor[root_dirs[0]+'.json'] = {
            "type": sub_dirs[0][0],
            "child": files_sub
        }
        # ------------ กรณีมี Certificate ซ้อนกันอยู่ ----------------
        if len(final_files[0]) > 0:
            for i in range(len(sub_dirs[0])):
                if i < len(sub_files[0])-1:
                    list_tmp = sub_files[0][i][len(sub_files[0][i])-1].split('.')
                    json_befor[list_tmp[0]+'.json'] = {
                        "type": sub_dirs[0][i],
                        "child": []
                    }
            final_sub = list()
            for i in final_files[0]:
                final_sub.append(i[len(i)-1])
            list_tmp = files_sub[len(files_sub)-1].split('.')
            json_befor[list_tmp[0]+'.json'] = {
                "type": sub_dirs[0][len(sub_dirs[0])-1],
                "child": final_sub
            }
        else:
            for i in range(len(sub_dirs[0])):
                list_tmp = sub_files[0][i][len(sub_files[0][i])-1].split('.')
                json_befor[list_tmp[0]+'.json'] = {
                    "type": sub_dirs[0][i],
                    "child": []
                }


        json_after = json.dumps(json_befor)
        print(json_after) # JSON output Final


        return render(request, "issue002.html", context)
    else:
        return render(request, "issue002.html", context)

def issuing(request):
    return render(request, "issue003.html")