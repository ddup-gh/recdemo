from django.shortcuts import render, redirect,HttpResponse
from app import models
from django import views
from Demomain import RunModel
import json
import os

# Create your views here.
def logout(request):
    request.session.clear()
    return redirect('/login.html')

def login(request):
    message=""
    models.Img.objects.all().delete()
    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        c = models.User.objects.filter(user=user,pwd=pwd).count()
        # print(c,end="***\n")
        if c:
            request.session['is_login'] = True
            request.session['username'] = user
            return redirect('/index.html')
        else:
            message = "用户名或密码错误请重新输入！"

    return render(request,'login.html',{"msg": message})

def index(request):
    username = request.session.get('username')
    a=request.session['is_login']
    if username and a:
        return render(request ,"index.html", {'user':username})
    else:
        return redirect('/login.html')

def upload(request):
    print("upload...******")
    # 登录验证
    # if request.method == "GET":
    #     return redirect('/login.html')

    # username = request.session.get('username')
    # a=request.session['is_login']
    # if username and a:
    if True: # escape login
       # models.Img.objects.filter(id=12).delete()
        if request.method == 'GET':
            print("get...*******")
            img_list = models.Img.objects.all()
            return render(request, 'upload.html', {'img_list': img_list})
        elif request.method == "POST":
            print("post...*******")
            # upload = request.POST.get('upload')
            obj = request.FILES.get('upload')
            if obj != None:
                file_path = os.path.join('static', 'upload', obj.name)     #拼接路径
                f = open(file_path, 'wb')
                for chunk in obj.chunks():
                    f.write(chunk)
                f.close()
                models.Img.objects.create(path=file_path)
                if request.session['bodybg']=="":
                    request.session['bodybg'] = obj.name
                elif request.session['texture']=="":
                    request.session['texture'] = obj.name
            kw = request.POST.get('kw')
            kh = request.POST.get('kh')
            ks = request.POST.get('ks')
            if kw and kh and ks and request.session['texture']!="":
                kwidth = float(kw)
                kheight = float(kh)
                kscale = float(ks)
                print("kwwwwwww:",kwidth)
                print(request.session['texture'])
                obj = RunModel(kwidth, kheight, kscale, request.session['bodybg'], request.session['texture'])
                obj.main()
            return redirect('/upload.html')
    else:
        print("none...*******")
        return redirect('/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        userpwd = request.POST.get("userpwd")
        idd = models.User.objects.all().count()+1
        models.User.objects.create(id=idd, pwd=userpwd, user=username)
        return render(request ,"login.html")
    else:
        return render(request,'register.html')

def remove(request):
    request.session['bodybg']=""
    request.session['texture']=""
    models.Img.objects.all().delete()
    return redirect('/upload.html')
